import numpy as np


class TransformHelper:
    # Rotate around the Z-axis
    @staticmethod
    def z_turn(angle: float) -> tuple:
        r_z = ((np.cos(angle), np.sin(angle), 0, 0),
               (-np.sin(angle), np.cos(angle), 0, 0),
               (0, 0, 1, 0),
               (0, 0, 0, 1))
        return r_z

    # Rotate around the Y-axis
    @staticmethod
    def y_turn(angle: float) -> tuple:
        r_y = ((np.cos(angle), 0, -np.sin(angle), 0),
               (0, 1, 0, 0),
               (np.sin(angle), 0, np.cos(angle), 0),
               (0, 0, 0, 1))
        return r_y

    # Rotate around the X-axis
    @staticmethod
    def x_turn(angle: float) -> tuple:
        r_x = ((1, 0, 0, 0),
               (0, np.cos(angle), np.sin(angle), 0),
               (0, -np.sin(angle), np.cos(angle), 0),
               (0, 0, 0, 1))
        return r_x

    # Move by the vector (a, b, c)
    @staticmethod
    def move_apex(a, b, c) -> tuple:
        t = ((1, 0, 0, 0),
             (0, 1, 0, 0),
             (0, 0, 1, 0),
             (a, b, c, 1))
        return t

    # Scaling
    @staticmethod
    def scaling(sx, sy, sz) -> tuple:
        s = ((sx, 0, 0, 0),
             (0, sy, 0, 0),
             (0, 0, sz, 0),
             (0, 0, 0, 1))
        return s

    # Renaming the axes, changing the Z-axis direction
    @staticmethod
    def change_direction() -> tuple:
        s = ((0, 0, -1, 0),
             (1, 0, 0, 0),
             (0, 1, 0, 0),
             (0, 0, 0, 1))
        return s
