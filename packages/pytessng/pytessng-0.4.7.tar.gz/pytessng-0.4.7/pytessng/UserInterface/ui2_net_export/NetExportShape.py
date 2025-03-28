from typing import Tuple

from .BaseNetExport import BaseNetExport


class NetExportShape(BaseNetExport):
    name: str = "导出为Shape"
    mode: str = "shape"
    format_: Tuple[str, str] = ("Shape", "shp")

    style: int = 2
    box_message: str = ""
