from typing import List, Dict
from PySide2.QtWidgets import QAction


class GlobalVar:
    # 是否是完整版
    extension: bool = False
    # 路网对象
    my_net = None
    # 仿真对象
    my_simulator = None
    # 界面对象
    my_menu = None
    # 与鼠标事件相关的按钮
    actions_related_to_mouse_event: Dict[str, QAction] = {}
    # 只能正式版本使用的按钮
    actions_only_official_version: List[QAction] = []

    @classmethod
    def set_extension(cls, extension: bool) -> None:
        cls.extension = extension

    @classmethod
    def set_my_net(cls, my_net) -> None:
        cls.my_net = my_net

    @classmethod
    def set_my_simulator(cls, my_simulator) -> None:
        cls.my_simulator = my_simulator

    @classmethod
    def set_my_menu(cls, my_menu) -> None:
        cls.my_menu = my_menu

    # 给MyNet添加鼠标观察者
    @classmethod
    def attach_observer_of_my_net(cls, observer_obj, is_fixed: bool = False) -> None:
        if cls.my_net is not None:
            cls.my_net.attach_observer(observer_obj, is_fixed)
        else:
            print("[ERROR] MyNet is not initialized!")

    # 给MyNet移除鼠标观察者
    @classmethod
    def detach_observer_of_my_net(cls) -> None:
        if cls.my_net is not None:
            cls.my_net.detach_observer()
        else:
            print("[ERROR] MyNet is not initialized!")

    # 给MySimulator添加仿真观察者的函数
    @classmethod
    def attach_observer_of_my_simulator(cls, observer_name: str, observer_obj) -> None:
        if cls.my_simulator is not None:
            cls.my_simulator.attach_observer(observer_name, observer_obj)
        else:
            print("[ERROR] MySimulator is not initialized!")

    # 给MySimulator移除仿真观察者的函数
    @classmethod
    def detach_observer_of_my_simulator(cls, observer_name: str) -> None:
        if cls.my_simulator is not None:
            cls.my_simulator.detach_observer(observer_name)
        else:
            print("[ERROR] MySimulator is not initialized!")

    @classmethod
    def get_actions_related_to_mouse_event(cls) -> Dict[str, QAction]:
        if cls.my_menu is not None:
            return cls.my_menu.actions_related_to_mouse_event
        print("[ERROR] MyMenu is not initialized!")
        return {}

    @classmethod
    def get_actions_only_official_version(cls) -> List[QAction]:
        if cls.my_menu is not None:
            return cls.my_menu.actions_only_official_version
        print("[ERROR] MyMenu is not initialized!")
        return []
