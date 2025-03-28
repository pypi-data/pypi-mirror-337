import json
import math
import traceback
from typing import Callable, Tuple
from pyproj import Proj
from PySide2.QtCore import QPointF

from ..BaseTool import BaseTool
from ..public.line.LineBase import LineBase
from ..public.line.LinePointGetter import LinePointGetter
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialog as pgd


class PileNumberDataSaver(BaseTool):
    def export(self, mode: str, data: dict, file_path: str):
        # 桩号数据
        pile_number_data: dict = {}
        for direction in data:
            try:
                if mode == "link":
                    direction_data = self.load_data_by_link_id(direction, *data[direction])
                else:
                    direction_data = self.load_data_by_point(direction, *data[direction])
                pile_number_data.update(direction_data)
            except:
                logger.logger_pytessng.error(f"Failed to export direction {direction} with the error: {traceback.format_exc()}!")

        # 关闭进度条
        pgd().close()

        # 保存数据
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(pile_number_data, file, indent=4, ensure_ascii=False)

    # 方式一：根据路段ID计算
    def load_data_by_link_id(self, direction: str, start_pile_number: float, end_pile_number: float, start_link_id: int, start_dist: float, end_link_id: int, end_dist: float):
        start_road = start_link = {"is_link": True, "road_id": start_link_id}
        end_road = end_link = {"is_link": True, "road_id": end_link_id}

        # 核验长度
        if start_dist > self._p2m(self.netiface.findLink(start_link_id).length()):
            raise Exception("The start_dist is too long!")
        if end_dist > self._p2m(self.netiface.findLink(end_link_id).length()):
            raise Exception("The end_dist is too long!")

        # 如果end_dist是-1就取路段的长度
        if end_dist == -1:
            end_dist = self._p2m(self.netiface.findLink(end_link_id).length())

        pile_number_data = self._load_data(direction, start_pile_number, end_pile_number, start_road, start_link, start_dist, end_road, end_link, end_dist)

        return pile_number_data

    # 方式二：根据平面点坐标计算
    def load_data_by_point(self, direction: str, start_pile_number: float, end_pile_number: float, start_x: float, start_y: float, end_x: float, end_y: float):
        # 找到起始路段
        start_point = (start_x, start_y)
        start_road, start_link, start_dist = self._find_road(start_point, "start")
        # 找到结束路段
        end_point = (end_x, end_y)
        end_road, end_link, end_dist = self._find_road(end_point, "end")

        pile_number_dict = self._load_data(direction, start_pile_number, end_pile_number, start_road, start_link, start_dist, end_road, end_link, end_dist)

        return pile_number_dict

    # 计算数据的根本方法
    def _load_data(self, direction: str, start_pile_number: float, end_pile_number: float, start_road: dict, start_link: dict, start_dist: float, end_road: dict, end_link: dict, end_dist: float):
        # 如果起始路段和结束路段相同
        if start_road == end_road:
            link = self._find_road_obj(**start_road)
            # 找到路段列表
            road_list = [
                {
                    "id": link.id(),
                    "is_link": True,
                    "length": round(self._p2m(link.length()), 3),
                    "lane_count": link.laneCount(),
                }
            ]
            all_length_tess = end_dist - start_dist

        else:
            # 找到最短路径
            routing = self._find_routing(start_link, end_link)
            # 找到路段列表
            road_list, all_length_tess = self._find_road_list(start_road, start_link, start_dist, end_road, end_link, end_dist, routing)

        # 实际长度
        all_length_real = end_pile_number - start_pile_number

        # 比较两个长度
        if abs(abs(all_length_real) - all_length_tess) > 20:
            logger.logger_pytessng.warning(f"The difference between the actual length {abs(all_length_real):.1f} and the tess length {all_length_tess:.1f} is too large!")

        # 放缩比例
        ratio = all_length_real / all_length_tess
        logger.logger_pytessng.debug(f"Actual length: {all_length_real}, tessng length: {all_length_tess}, ratio: {ratio}")

        # 得到桩号字典数据
        pile_number_data = self._calc_pile_number_data(road_list, direction, start_pile_number, start_dist, ratio)

        return pile_number_data

    # 获取路段/连接段对象
    def _find_road_obj(self, is_link: bool, road_id: int):
        return self.netiface.findLink(road_id) if is_link else self.netiface.findConnector(road_id)

    # （方式二需要）根据点定位路段
    def _find_road(self, point: tuple, mode: str):
        x, y = point[0], -point[1]
        self.netiface.buildNetGrid(5)
        locations = self.netiface.locateOnCrid(QPointF(x, y), 9)

        if not locations:
            raise "Can't find the location road!"

        location = locations[0]
        dist = round(self._p2m(location.distToStart), 3)
        lane = location.pLaneObject

        try:
            road = lane.link()
            link = road
        except:
            road = lane.connector()
            link = road.toLink() if mode == "start" else road.fromLink()

        road_dict = {"is_link": road.isLink(), "road_id": road.id()}
        link_dict = {"is_link": link.isLink(), "road_id": link.id()}

        return road_dict, link_dict, dist

    # 获取路径对象
    def _find_routing(self, start_link, end_link):
        start_link = self._find_road_obj(**start_link)
        end_link = self._find_road_obj(**end_link)

        routing = self.netiface.shortestRouting(start_link, end_link)

        if routing is None:
            logger.logger_pytessng.error(f"The route from link {start_link.id()} to link {end_link.id()} can't be found!")
            raise f"The route can't be found!"

        return routing

    # 获取道路列表
    def _find_road_list(self, start_road, start_link, start_dist: float, end_road, end_link, end_dist: float, routing):
        start_road = self._find_road_obj(**start_road)
        start_link = self._find_road_obj(**start_link)
        end_road = self._find_road_obj(**end_road)
        end_link = self._find_road_obj(**end_link)

        road_list = []
        all_length_tess = 0

        # 头路段
        if start_link != start_road:
            road_id = start_road.id()
            length = round(self._p2m(start_road.length()), 3)
            lane_count = len(start_road.laneConnectors())
            road = {
                "id": road_id,
                "is_link": False,
                "length": length,
                "lane_count": lane_count,
            }
            road_list.append(road)
            all_length_tess += length - start_dist

        # 中间路段
        current_road = start_link
        while current_road:
            road_id = current_road.id()
            is_link = current_road.isLink()

            if is_link:
                length = self._p2m(current_road.length())
                lane_count = current_road.laneCount()
            else:
                # 考虑连接主路的连接段车道
                from_link_id = road_list[-1]["id"]
                to_link_id = routing.nextRoad(current_road).id()
                lengths = [
                    self._p2m(lane.length())
                    for lane in current_road.laneConnectors()
                    if lane.fromLane().link().id() == from_link_id and lane.toLane().link().id() == to_link_id
                ]
                length = max(lengths)  # 用各车道的最大长度
                lane_count = len(lengths)

            link = {
                "id": road_id,
                "is_link": is_link,
                "length": round(length, 3),
                "lane_count": lane_count,
            }
            road_list.append(link)

            # 如果第一个road是link
            if len(road_list) == 0 and start_link == start_road:
                all_length_tess += length - start_dist
            else:
                all_length_tess += length

            current_road = routing.nextRoad(current_road) if routing else None

        # 如果最后一个road是link
        if end_link == end_road:
            length = road_list[-1]["length"]
            all_length_tess += -(length - end_dist)
        else:
            road_id = end_road.id()
            length = round(self._p2m(end_road.length()), 3)
            lane_count = len(end_road.laneConnectors())
            road = {
                "id": road_id,
                "is_link": False,
                "length": length,
                "lane_count": lane_count,
            }
            road_list.append(road)
            all_length_tess += end_dist

        return road_list, all_length_tess

    # 根据道路列表计算桩号数据
    def _calc_pile_number_data(self, road_list: list, direction: str, start_pile_number: float, start_dist: float, ratio: float):
        attrs = self.netiface.netAttrs().otherAttrs()
        if attrs.get("proj_string"):
            proj_string: str = attrs["proj_string"]
            proj: Callable = Proj(proj_string)
        else:
            proj: Callable = lambda x, y, inverse: (None, None)

        pile_number_data: dict = {}

        # 为了判断桩号是增还是减
        step = int(ratio / abs(ratio))

        # 桩号的起始值
        current_distance = start_pile_number - ratio * start_dist

        # 遍历道路列表
        for index, road in pgd.progress(enumerate(road_list), f"方向{direction}计算中..."):
            # 总的的开始/结束桩号
            road["start_pile_number"] = start_pile_number = round(current_distance, 2)
            current_distance += road["length"] * ratio
            road["end_pile_number"] = end_pile_number = round(current_distance, 2)

            # 道路信息
            road_id = road["id"]
            is_link = road["is_link"]
            lane_count = road["lane_count"]
            is_have_emergency_lane = False
            road_obj = self._find_road_obj(is_link, road_id)
            lanes = road_obj.lanes() if is_link else road_obj.laneConnectors()

            # 向上取整
            start = math.ceil(start_pile_number) if index != 0 else math.floor(start_pile_number)
            # 向下取整
            end = math.floor(end_pile_number) if index != len(road_list) - 1 else math.ceil(end_pile_number)

            for pile_number in range(start, end + 1, step):
                dist = round(abs((pile_number - start_pile_number) / ratio), 3)
                # 桩号字符串：方向+桩号
                pile_number_str = f"{direction}{pile_number}"
                # 道路数据
                road_data: dict = {
                    "id": road_id,
                    "isLink": is_link,
                    "laneCount": lane_count,
                    "isHaveEmergencyLane": is_have_emergency_lane,
                    "distance": dist,
                }
                # 各车道点位数据
                position_data: dict = {}
                coord_data: dict = {}
                angle_data: dict = {}
                for lane_index, lane in enumerate(lanes[::-1], start=1):
                    # ========== TESS坐标 ==========
                    center_points: list = self._qtpoint2list(lane.centerBreakPoint3Ds())
                    center_point, index, r = LinePointGetter.get_point_and_index_by_dist(center_points, dist)
                    x: float = center_point[0]
                    y: float = center_point[1]
                    z: float = center_point[2]
                    position_data[lane_index] = [x, y, z]

                    # ========== 经纬度 ==========
                    coord: Tuple[float, float] = proj(x, y, inverse=True)
                    coord_data[lane_index] = [coord[0], coord[1], z]

                    # ========== 角度 ==========
                    # 索引
                    if index < len(center_points) - 1:
                        index_1: int = index
                        index_2: int = index + 1
                    else:
                        index_1: int = index - 1
                        index_2: int = index
                    # 航向角
                    last_point: list = center_points[index_1]
                    next_point: list = center_points[index_2]
                    yaw: float = LineBase.calculate_angle_with_y_axis(last_point, next_point)
                    yaw: float = round(yaw, 2)
                    # 俯仰角
                    pitch: float = LineBase.calculate_pitch_angle(last_point, next_point)
                    pitch: float = round(pitch, 2)
                    # 滚转角
                    left_points: list = self._qtpoint2list(lane.leftBreakPoint3Ds())
                    right_points: list = self._qtpoint2list(lane.rightBreakPoint3Ds())
                    left_point_1: list = left_points[index_1]
                    right_point_1: list = right_points[index_1]
                    left_point_2: list = left_points[index_2]
                    right_point_2: list = right_points[index_2]
                    angle_1: float = LineBase.calculate_pitch_angle(left_point_1, right_point_1)
                    angle_2: float = LineBase.calculate_pitch_angle(left_point_2, right_point_2)
                    roll: float = angle_1 + (angle_2 - angle_1) * r
                    roll: float = round(roll, 2)
                    angle_data[lane_index] = [yaw, pitch, roll]

                pile_number_data[pile_number_str] = {
                    "road": road_data,
                    "position": position_data,
                    "coord": coord_data,
                    "headingPitchRoll": angle_data,
                }

        return pile_number_data
