from pytessng.UserInterface.public import BaseUIVirtual
from pytessng.ToolInterface import MyOperation


class NetEditRecalcConnectorCenterline(BaseUIVirtual):
    name: str = "重新计算连接段中心线"
    mode: str = "recalc_connector_centerline"

    def load_ui(self):
        MyOperation().apply_net_edit_operation(self.mode, dict(), self)
