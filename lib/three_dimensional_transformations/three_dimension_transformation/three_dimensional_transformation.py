import pygame
import numpy as np
import random
import copy
from .transform_helper import TransformHelper


class ThreeDimensionalTransformation:
    def __init__(self, display_width=1920, display_height=1080, fps=30):
        self.fps = fps
        self.display_width = display_width
        self.display_height = display_height

        # Figure params
        self.sub_circle_radius = 350
        self.main_circle_radius = 500
        self.number_of_apexes = 8

        # Figure containers
        self.figure = []
        self.figure_view = []
        self.figure_projection = []

        # View params
        self.viewpoint_distance = 1000
        self.viewpoint_vector = [2250, -225, 2250]
        self.viewpoint = [-self.viewpoint_vector[0], -self.viewpoint_vector[1], -self.viewpoint_vector[2]]
        self.turn_angles = {"x": 0, "y": 0, "z": 0}

        # Figure color
        self.color = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))

        # Control transformation steps
        self.control_step_x = self.viewpoint_distance // 10
        self.control_step_y = self.viewpoint_distance // 10
        self.control_step_z = self.viewpoint_distance // 10

        # pygame clock, display objects
        self.clock, self.display = None, None

    # Pygame window initialization
    def initialize_pygame_window(self):
        # Pygame window initialization
        pygame.init()
        pygame.display.set_caption('Circle')

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.display_width, self.display_height), pygame.RESIZABLE)

    def set_sub_circle(self, x, y, z, angle):
        """
        :param x: X-coord of sub-circle center
        :param y: Y-coord of sub-circle center
        :param z: Z-coord of sub-circle center
        :param angle: current main circle angle position
        :return circle: sub-circle
        """
        circle = []
        for i in range(2 * self.number_of_apexes):
            x_current = x + (self.main_circle_radius -
                             (self.sub_circle_radius * np.cos(i * np.pi / self.number_of_apexes))) * np.cos(angle)

            y_current = y + self.sub_circle_radius * np.sin(i * np.pi / self.number_of_apexes)

            z_current = z + (self.main_circle_radius -
                             (self.sub_circle_radius * np.cos(i * np.pi / self.number_of_apexes))) * np.sin(angle)

            circle.append([x_current, y_current, z_current, 1])
        return circle

    # Setting all apexes for figure
    def set_figure(self):
        step = np.pi / (2 * self.number_of_apexes)

        for i in range(4 * self.number_of_apexes):
            y_center = 0
            z_center = self.main_circle_radius * np.sin(i * step)
            x_center = self.main_circle_radius * np.cos(i * step)

            self.figure.append(self.set_sub_circle(x_center, y_center, z_center, i * step))

        self.figure = np.matmul(self.figure, TransformHelper.x_turn(self.turn_angles["x"]))
        self.figure = np.matmul(self.figure, TransformHelper.y_turn(self.turn_angles["y"]))
        self.figure = np.matmul(self.figure, TransformHelper.z_turn(self.turn_angles["z"]))

    # Conversion from world to species coordinate system
    def view_transform(self):
        if self.viewpoint[0] == 0:
            angle_y = 0 if self.viewpoint[1] == 0 else np.pi / 2 if self.viewpoint[1] > 0 else -np.pi / 2
            angle_z = 0 if self.viewpoint[2] == 0 else np.pi / 2 if self.viewpoint[2] > 0 else -np.pi / 2
        else:
            angle_y = np.arctan(self.viewpoint[1] / self.viewpoint[0])
            angle_z = np.arctan(self.viewpoint[2] / self.viewpoint[0])

        viewpoint_vector_length = (
            self.viewpoint_vector[0] ** 2 +
            self.viewpoint_vector[1] ** 2 +
            self.viewpoint_vector[2] ** 2
        ) ** (1 / 2)

        z_turn_matrix = TransformHelper.z_turn(angle_z)
        y_turn_matrix = TransformHelper.y_turn(angle_y)

        figure_new = copy.deepcopy(self.figure)
        for i in range(len(figure_new)):
            for j in range(len(figure_new[i])):
                figure_new[i][j] = np.matmul(np.matmul(figure_new[i][j], z_turn_matrix), y_turn_matrix)
                figure_new[i][j] = np.matmul(figure_new[i][j], TransformHelper.move_apex(viewpoint_vector_length, 0, 0))
                figure_new[i][j] = np.matmul(figure_new[i][j], TransformHelper.change_direction()).tolist()

        self.figure_view = figure_new

    # Convert from view to screen projection
    def perspective_transform(self):
        self.figure_projection = [
            [
                [0, 0, 0] for _ in range(len(self.figure_view[0]))
            ] for _ in range(len(self.figure_view))
        ]
        for i in range(len(self.figure_view)):
            for j in range(len(self.figure_view[i])):
                if self.figure_view[i][j][2] != 0:
                    self.figure_projection[i][j][0] = self.viewpoint_distance * self.figure_view[i][j][0] / \
                                                      self.figure_view[i][j][2] + self.display_width / 2
                    self.figure_projection[i][j][1] = self.display_height / 2 - self.viewpoint_distance * \
                                                      self.figure_view[i][j][1] / self.figure_view[i][j][2]
                else:
                    self.figure_projection[i][j][0] = (self.viewpoint_distance *
                                                       self.figure_view[i][j][0]) + self.display_width / 2
                    self.figure_projection[i][j][1] = self.display_height / 2 - \
                                                      (self.viewpoint_distance * self.figure_view[i][j][1])

                self.figure_projection[i][j][2] = -(self.figure_view[i][j][2] + self.viewpoint_distance)

    # Drawing figure
    def draw_figure(self,) -> None:
        for i in range(len(self.figure_projection)):
            for j in range(len(self.figure_projection[i])):
                pygame.draw.line(self.display, self.color,
                                 [
                                     self.figure_projection[i][j - 1][0],
                                     self.figure_projection[i][j - 1][1]
                                 ],
                                 [
                                     self.figure_projection[i][j][0],
                                     self.figure_projection[i][j][1]
                                 ], 4)

                pygame.draw.line(self.display, self.color,
                                 [
                                     self.figure_projection[i - 1][j][0],
                                     self.figure_projection[i - 1][j][1]
                                 ],
                                 [
                                     self.figure_projection[i][j][0],
                                     self.figure_projection[i][j][1]
                                 ], 4)
