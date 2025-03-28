from typing import TypeVar
from PySide2.QtGui import QMouseEvent, QKeyEvent, QWheelEvent

from .BaseTess import BaseTess, PyCustomerNet


class BaseMouse(BaseTess):
    # 添加之前
    def before_attach(self) -> None:
        pass

    # 移除之前
    def before_detach(self) -> None:
        pass

    # 鼠标单击
    def after_mouse_press_event(self, event: QMouseEvent) -> None:
        pass

    # 鼠标释放
    def after_mouse_release_event(self, event: QMouseEvent) -> None:
        pass

    # 鼠标移动
    def after_mouse_move_event(self, event: QMouseEvent) -> None:
        pass

    # 鼠标双击
    def after_mouse_double_click_event(self, event: QMouseEvent) -> None:
        pass

    # 键盘按下
    def after_key_press_event(self, event: QKeyEvent) -> None:
        pass

    # 鼠标滚轮滚动
    def after_wheel_event(self, event: QWheelEvent) -> None:
        pass


BaseMouseType = TypeVar("BaseMouseType", bound="BaseMouse")
