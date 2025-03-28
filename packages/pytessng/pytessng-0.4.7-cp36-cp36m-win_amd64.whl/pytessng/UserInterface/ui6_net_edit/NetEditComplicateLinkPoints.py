from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton
from PySide2.QtGui import QDoubleValidator

from .BaseNetEdit import BaseNetEdit, HBoxLayout, VBoxLayout


class NetEditComplicateLinkPoints(BaseNetEdit):
    name: str = "加密路段点位"
    mode: str = "complicate_link_points"

    def _set_widget_layout(self):
        # 第一行：文本、输入框
        self.label_dist = QLabel('最大断点间距（m）：')
        self.line_edit_dist = QLineEdit()
        # 第二行：按钮
        self.button = QPushButton('加密路网')

        # 总体布局
        layout = VBoxLayout([
            HBoxLayout([self.label_dist, self.line_edit_dist]),
            self.button
        ])
        self.setLayout(layout)

        # 限制输入框内容
        validator = QDoubleValidator()
        self.line_edit_dist.setValidator(validator)

        # 设置提示信息
        self.line_edit_dist.setToolTip(f'{1} <= distance <= {1000}')

    def _set_monitor_connect(self):
        self.line_edit_dist.textChanged.connect(self._apply_monitor_state)

    def _set_default_state(self):
        default_interval = 10
        self.line_edit_dist.setText(f"{default_interval}")
        self._apply_monitor_state()

    def _apply_monitor_state(self):
        max_interval = self.line_edit_dist.text()
        enabled_button = False
        try:
            max_interval = float(max_interval)
            min_max_interval = 1
            max_max_interval = 1000
            if min_max_interval <= max_interval <= max_max_interval:
                enabled_button = True
        except:
            pass

        # 设置可用状态
        self.button.setEnabled(enabled_button)

    # 重写父类方法
    def _get_net_edit_params(self) -> dict:
        max_interval = float(self.line_edit_dist.text())
        return {
            "max_interval": max_interval,
        }
