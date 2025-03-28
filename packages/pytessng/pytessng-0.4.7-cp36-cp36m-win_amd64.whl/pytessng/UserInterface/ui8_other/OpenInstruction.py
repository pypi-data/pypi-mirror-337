from webbrowser import open

from pytessng.Config import PathConfig
from pytessng.UserInterface.public.BaseUI import BaseUIVirtual


class OpenInstruction(BaseUIVirtual):
    name = "打开用户说明书"

    def load_ui(self):
        open(PathConfig.INSTRUCTION_FILE_PATH, new=2)
