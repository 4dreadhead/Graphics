from lines_generation.lines_generation import LinesGenerator
from plane_transformations.plane_transformations import FallingLeaf
from three_dimensional_transformations.action_control import ActionControl
from three_dimensional_transformations.figure_rendering import FigureRendering
from consolemenu import *
from consolemenu.items import *


# Simple console application
class ConsoleApplication:
    def __init__(self):
        self.console_menu = ConsoleMenu(
            'Course "Computer Graphics", ISIT, Krasnoyarsk.\n\nby Vyacheslav Zhdanov, 2021',
            "Keyboard hotkeys for 3D-figure transformations:\n" +
            "\t* w/s - zoom in/out;\n" +
            "\t* a/d - spin figure;\n"
            "\t* up/down/left/right - rotate around the axes;\n"
            "\t* u/j/h/k - move figure.")

        self.console_menu.append_item(FunctionItem("Lines generation", LinesGenerator().run))
        self.console_menu.append_item(FunctionItem("Leaf falling", FallingLeaf().run))
        self.console_menu.append_item(FunctionItem("3D-figure transformation", ActionControl().run))
        self.console_menu.append_item(FunctionItem("3D-figure with z-buffer rendering", FigureRendering().run))

    def run_console_application(self):
        self.console_menu.show()


if __name__ == '__main__':
    ConsoleApplication().run_console_application()
