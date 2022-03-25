from lines_generation.lines_generation import LinesGenerator
from plane_transformations.plane_transformations import FallingLeaf
from three_dimensional_transformations.action_control import ActionControl
from three_dimensional_transformations.figure_rendering import FigureRendering
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem


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

        self.console_menu.append_item(FunctionItem("Lines generation", self.run_lines_generation))
        self.console_menu.append_item(FunctionItem("Leaf falling", self.run_leaf_falling))
        self.console_menu.append_item(FunctionItem("3D-figure transformation", self.run_action_control))
        self.console_menu.append_item(FunctionItem("3D-figure with z-buffer rendering", self.run_figure_rendering))

    # Run application
    def run_console_application(self):
        self.console_menu.show()

    # Generate lines
    @staticmethod
    def run_lines_generation():
        LinesGenerator().run()

    # Start scene with leaf falling
    @staticmethod
    def run_leaf_falling():
        FallingLeaf().run()

    # Transformations control for 3D-figure
    @staticmethod
    def run_action_control():
        ActionControl().run()

    # Render 3D-figure with z-buffer algorithm
    @staticmethod
    def run_figure_rendering():
        FigureRendering().run()


if __name__ == '__main__':
    ConsoleApplication().run_console_application()
