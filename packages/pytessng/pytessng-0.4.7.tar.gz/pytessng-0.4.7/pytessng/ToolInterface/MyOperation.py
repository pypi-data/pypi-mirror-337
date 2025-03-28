import os
import uuid
from datetime import datetime
from typing import List, Union
from traceback import format_exc
from requests import post
from singleton_decorator import singleton
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QPointF

from .BaseTool import BaseTool
# 1-路网数据导入
from .alg1_net_import.Other2TessngFactory import Other2TessngFactory
# 2-路网数据导出
from .alg2_net_export.Tessng2OtherFactory import Tessng2OtherFactory
# 3-轨迹数据导入
from .alg3_sim_import.SimuImportTrajectoryActor import SimuImportTrajectoryActor
# 4.1-轨迹数据导出
from .alg4_sim_export.trajectory.SimuExportTrajectoryActor import SimuExportTrajectoryActor
# 4.2-信号灯数据导出
from .alg4_sim_export.signalLight.SimuExportSignalLightActor import SimuExportSignalLightActor
# 5.1-桩号数据导出
from .alg5_file_export.PileNumberDataSaver import PileNumberDataSaver
# 5.2-选区数据导出
from .alg5_file_export.GridDataSaver import GridDataSaver
# 6-路段编辑
from .alg6_net_edit.NetEditorFactory import NetEditorFactory
# x.1-核验shapefile
from .alg1_net_import.shape2tessng.ShapefileChecker import ShapefileChecker
# x.2-核验kafka
from .public.communication.KafkaChecker import KafkaChecker
# 公共工具
from pytessng.Config import PathConfig
from pytessng.GlobalVar import GlobalVar
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialog
from pytessng.Tessng import BaseTess


@singleton
class MyOperation(BaseTess):
    def __init__(self):
        super().__init__()
        # 是否是有界面版本
        self.is_gui_version: bool = True
        # 前端工具包
        self.ui_utils = None
        if self.is_gui_version:
            from pytessng.UserInterface import Utils
            self.ui_utils = Utils()

    def apply_net_import_operation(self, import_mode: str, params: dict, widget: QWidget = None) -> None:
        """路网数据导入"""
        # 导入模式
        if import_mode not in ["opendrive", "shape", "osm", "json", "excel", "aidaroe", "annex"]:
            raise ValueError("Invalid import mode!")
        # 是否是道路网络
        is_network: bool = import_mode != "annex"

        # 1.正在仿真中无法导入
        if self.simuiface.isRunning() or self.simuiface.isPausing():
            self._show_message_box("请先停止仿真！", "warning")
            return

        # 2.路网上已经有路段进行询问
        if self.is_gui_version:
            link_count: int = self.netiface.linkCount()
            if is_network and link_count > 0:
                messages: dict = {
                    "title": "是否继续",
                    "content": "路网上已有路段，请选择是否继续导入",
                    "yes": "继续",
                }
                confirm: int = self._show_confirm_dialog(messages)
                if confirm != 0:
                    return

        # 3.尝试关闭在线地图
        self.win.showOsmInline(False)

        # 4.尝试关闭窗口
        if widget is not None:
            widget.close()

        # 5.执行转换
        try:
            # 记录日志
            logger.logger_pytessng.info(f"Network import mode: {import_mode}")
            logger.logger_pytessng.info(f"Network import params: {params}")

            # 当前路网上的路段ID
            current_link_ids: List[int] = self.netiface.linkIds()

            # 创建路网
            response: dict = Other2TessngFactory.build(self.netiface, import_mode, params)
            status, message = response["status"], response["message"]

            # 如果有问题
            if not status:
                message, message_mode = message, "warning"
            # 如果没问题，问要不要移动
            else:
                # 新创建的路段
                new_links: list = [link for link in self.netiface.links() if link.id() not in current_link_ids]
                xs, ys = [], []
                for link in new_links:
                    points = link.centerBreakPoints()
                    xs.extend([point.x() for point in points])
                    ys.extend([point.y() for point in points])

                # 路网数据不为空
                if xs and ys:
                    # osm自动移动，其他要询问
                    if is_network and import_mode != "osm":
                        x_min, x_max = min(xs), max(xs)
                        y_min, y_max = min(ys), max(ys)
                        message = f"新创建路网的范围：\n    x = [ {x_min:.1f} m , {x_max:.1f} m ]\n    y = [ {y_min:.1f} m , {y_max:.1f} m ]\n"

                        messages: dict = {
                            "title": "是否移动至中心",
                            "content": message + "是否将路网移动到场景中心",
                            "yes": "确定",
                        }
                        confirm: int = self._show_confirm_dialog(messages)

                        # 移动路网
                        attrs: dict = self.netiface.netAttrs().otherAttrs()
                        # 要移动
                        if confirm == 0:
                            # 比例尺转换
                            scene_scale = self.netiface.sceneScale()
                            x_move: float = attrs["move_distance"]["x_move"] / scene_scale
                            y_move: float = attrs["move_distance"]["y_move"] / scene_scale
                            # 移动路网
                            move = QPointF(x_move, -y_move)
                            self.netiface.moveLinks(new_links, move)
                        # 不移动
                        else:
                            attrs.update({"move_distance": {"x_move": 0, "y_move": 0}})
                            network_name: str = self.netiface.netAttrs().netName()
                            self.netiface.setNetAttrs(network_name, otherAttrsJson=attrs)

                message, message_mode = "导入成功", "info"

            # 打印属性信息
            attrs: dict = self.netiface.netAttrs().otherAttrs()
            print("=" * 66)
            print("Create network! Network attrs:")
            for k, v in attrs.items():
                print(f"\t{k:<15}:{' ' * 5}{v}")
            print("=" * 66, "\n")
            logger.logger_pytessng.info(f"Network attrs: {attrs}")

        except:
            message, message_mode = "导入失败", "warning"
            logger.logger_pytessng.critical(format_exc())

        # 6.设置场景宽度和高度
        if is_network:
            BaseTool(self.netiface).update_scene_size()

        # 7.设置不限时长
        if is_network:
            self.simuiface.setSimuIntervalScheming(0)

        # 8.关闭进度条
        ProgressDialog().close()

        # 11.弹出提示框
        self._show_message_box(message, message_mode)

        # 12.记录信息
        self.send_message_to_server("operation", f"net_import_{import_mode}")

    def apply_net_export_operation(self, export_mode: str, params: dict, widget: QWidget = None) -> None:
        """路网数据导出"""
        # 导出模式
        if export_mode not in ["opendrive", "shape", "geojson", "json", "unity"]:
            raise ValueError("Invalid export mode!")

        # 1.正在仿真中无法导出
        if self.simuiface.isRunning() or self.simuiface.isPausing():
            self.ui_utils.show_message_box("请先停止仿真！", "warning")
            return

        # 2.检查路网上是否有路段
        if self.netiface.linkCount() == 0:
            self.ui_utils.show_message_box("当前路网没有路段！", "warning")
            return

        # 3.尝试关闭窗口
        if widget is not None:
            widget.close()

        # 4.执行转换
        try:
            logger.logger_pytessng.info(f"Network export mode: {export_mode}")
            logger.logger_pytessng.info(f"Network export params: {params}")
            Tessng2OtherFactory.build(self.netiface, export_mode, params)
            message, message_mode = "导出成功", "info"
            logger.logger_pytessng.info(f"Network attrs: {self.netiface.netAttrs().otherAttrs()}")
        except:
            message, message_mode = "导出失败", "warning"
            logger.logger_pytessng.critical(format_exc())

        # 5.关闭进度条
        ProgressDialog().close()

        # 6.提示信息
        self._show_message_box(message, message_mode)

        # 7.记录信息
        self.send_message_to_server("operation", f"net_export_{export_mode}")

    def apply_sim_import_or_export_operation(self, mode: str, params: dict) -> None:
        """仿真数据导入/仿真数据导出"""
        # 仿真观察者映射表
        simulator_observer_mapping = {
            "simu_import_trajectory": SimuImportTrajectoryActor,
            "simu_export_trajectory": SimuExportTrajectoryActor,
            "simu_export_signal_light": SimuExportSignalLightActor,
        }
        # 如果是非法模式则直接返回
        if mode not in simulator_observer_mapping:
            return

        # 仿真观察者名称
        simulator_observer_name: str = mode

        # 根据参数是否为空判断是添加还是移除
        if bool(params):
            # 获取仿真观察者
            simulator_observer_obj = simulator_observer_mapping[mode]()
            # 初始化数据
            simulator_observer_obj.init_data(params)
            # MySimulator添加观察者
            GlobalVar.attach_observer_of_my_simulator(simulator_observer_name, simulator_observer_obj)
        else:
            # MySimulator移除观察者
            GlobalVar.detach_observer_of_my_simulator(simulator_observer_name)

    def apply_file_export_operation(self, export_mode: str, params: dict, widget: QWidget = None) -> None:
        """文件导出"""
        # 操作者映射表
        operator_mapping = {
            "pile_number": PileNumberDataSaver,
            "grid": GridDataSaver,
        }

        # 1.正在仿真中无法导出
        if self.simuiface.isRunning() or self.simuiface.isPausing():
            widget.utils.show_message_box("请先停止仿真！", "warning")
            return

        # 2.将按钮修改成【取消工具】
        self.guiiface.actionNullGMapTool().trigger()

        # 3.获取保存路径
        file_path = widget.utils.get_save_file_path(widget.format)
        if not file_path:
            return
        # 更改默认路径
        PathConfig.OPEN_DIR_PATH = os.path.dirname(file_path)

        # 4.尝试关闭窗口
        if widget is not None:
            widget.close()

        # 5.执行操作
        logger.logger_pytessng.info(f"Other operation mode: {widget.mode}")
        logger.logger_pytessng.info(f"Other operation params: {params}")
        # 获取操作者
        operator = operator_mapping.get(widget.mode)
        if not operator:
            return
        try:
            operator(self.netiface).export(**params, file_path=file_path)
            message, message_mode = "操作完成", "info"
        except:
            logger.logger_pytessng.critical(format_exc())
            message, message_mode = "操作失败", "warning"

        # 6.关闭进度条
        ProgressDialog().close()

        # 7.提示信息
        self._show_message_box(message, message_mode)

        # 8.记录信息
        self.send_message_to_server("operation", f"file_export_{export_mode}")

    def apply_net_edit_operation(self, edit_mode: str, params: dict, widget: QWidget = None, close_widget: bool = True) -> Union[None, list]:
        """路网编辑"""
        # 编辑模式
        edit_mode: str = edit_mode

        # 1.正在仿真中无法编辑
        if self.simuiface.isRunning() or self.simuiface.isPausing():
            self.ui_utils.show_message_box("请先停止仿真！", "warning")
            return None

        # 2.检查有无路段
        check_count_edit_mode_list: List[str] = [
            "modify_link_attrs",
            "modify_link_speed",
            "merge_link",
            "split_link",
            "move_link",
            "rotate_link",
            "simplify_link_points",
            "complicate_link_points",
            "recalc_link_centerline",
            "recalc_connector_centerline",
            "extend_connector",
        ]
        if edit_mode in check_count_edit_mode_list:
            # 如果没有路段
            if not self.netiface.linkCount():
                self._show_message_box("当前路网没有路段！", "warning")
                return None

        # 3.尝试关闭窗口
        if widget is not None and close_widget and hasattr(widget, "close"):
            widget.close()

        # 4.执行路段编辑
        try:
            # 返回值为0表示无操作
            response: Union[None, list, int] = NetEditorFactory.build(edit_mode, self.netiface, params)
            # 如果是定位路段直接返回
            if edit_mode in ["locate_link", "modify_link_points"]:
                return response
            message, message_mode = "操作成功", "info"
            # 记录日志
            if response != 0:
                logger.logger_pytessng.info(f"Link edit mode: {edit_mode}")
                # 去除函数
                print_params = {
                    k: v
                    for k, v in params.items()
                    if not callable(v)
                }
                logger.logger_pytessng.info(f"Link edit params: {print_params}")
        except:
            response = None
            message, message_mode = "操作失败", "warning"
            # 记录日志
            logger.logger_pytessng.critical(format_exc())

        # 5.关闭进度条
        ProgressDialog().close()

        # 6.提示信息
        if response != 0:
            self._show_message_box(message, message_mode)

        # 7.记录信息
        if response != 0:
            self.send_message_to_server("operation", widget.name)
            return None
        return None

    def apply_check_data(self, mode: str, *args, **kwargs):
        """核验数据"""
        # 核验者映射表
        checker_mapping = {
            "shapefile": ShapefileChecker,
            "kafka": KafkaChecker,
        }

        # 获取核验者
        checker = checker_mapping.get(mode)
        if checker is None:
            return

        # 核验结果的具体类型根据核验者不同而不同
        check_result = checker.check_data(*args, **kwargs)
        return check_result

    @staticmethod
    def send_message_to_server(path: str, message: str) -> int:
        """发送信息"""
        # 用于唯一标识
        uuid_path: str = PathConfig.UUID_FILE_PATH
        if os.path.exists(uuid_path):
            UUID: str = open(uuid_path, "r").read()
        else:
            UUID: str = str(uuid.uuid4())
            with open(uuid_path, "w") as f:
                f.write(UUID)
        # 相关配置
        host: str = u"\u0031\u0032\u0039\u002e\u0032\u0031\u0031\u002e\u0032\u0038\u002e\u0032\u0033\u0037"
        port: str = u"\u0035\u0036\u0037\u0038"
        url: str = f"http://{host}:{port}/{path}/"
        message = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": os.getlogin(),
            "UUID": UUID,
            "message": message,
        }
        # 发送信息
        try:
            status_code: int = post(url, json=message).status_code
        except:
            status_code: int = 502
        return status_code

    def _show_message_box(self, message: str, mode: str = None) -> None:
        if self.is_gui_version:
            self.ui_utils.show_message_box(message, mode)
        else:
            print(message)

    def _show_confirm_dialog(self, messages: dict) -> int:
        if self.is_gui_version:
            return self.ui_utils.show_confirm_dialog(messages)
        return 0
