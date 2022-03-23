from .three_dimension_transformation.three_dimensional_transformation import ThreeDimensionalTransformation
from .three_dimension_transformation.math_helper import MathHelper
import pygame


class FigureRendering(ThreeDimensionalTransformation):
    def __init__(self):
        super().__init__()

        self.color_step = 0
        self.number_of_apexes *= 2
        self.z_buffer = []
        self.to_draw_coordinates_list = {}
        self.render = True

    def run(self):
        self.initialize_pygame_window()
        self.display.fill((201, 232, 232))

        self.set_figure()
        self.view_transform()
        self.perspective_transform()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.let_z_buffer_algorithm()

    def let_z_buffer_algorithm(self):
        if self.render:
            self.z_buffer = [[99999 for _ in range(self.display_width)] for _ in range(self.display_height)]
            for i in range(len(self.figure_projection)):
                z_max, z_min, z_color_step = self.calculate_additional_z_values(i)

                for j in range(len(self.figure_projection[i])):
                    # Do not draw invisible polygons
                    if self.figure_projection[i][j][2] < 0 or self.figure_projection[i][j - 1][2] < 0 or \
                       self.figure_projection[i - 1][j][2] < 0 or self.figure_projection[i - 1][j - 1][2] < 0:
                        continue

                    color_step = MathHelper.set_color_step([
                        self.figure_projection[i][j - 1],
                        self.figure_projection[i][j],
                        self.figure_projection[i - 1][j]
                    ], z_max, z_color_step)

                    # Draw if it is visible
                    self.draw_triangle([
                        self.figure_projection[i][j - 1],
                        self.figure_projection[i][j],
                        self.figure_projection[i - 1][j]
                    ], color_step)

                    self.draw_triangle([
                        self.figure_projection[i][j - 1],
                        self.figure_projection[i - 1][j - 1],
                        self.figure_projection[i - 1][j]
                    ], color_step)
                pygame.display.update()
            self.render = False

    # Pixel-by-pixel drawing of polygons
    def draw_triangle(self, polygon, color_step):
        apex_a, apex_b, apex_c = MathHelper.sort_apexes(polygon, descending=True)

        color_step = 255 if color_step > 255 else 0 if color_step < 0 else color_step
        lime_color = (int(3 / 5 * color_step), color_step, 0)

        self.get_triangle_sides(apex_a, apex_b, apex_c)

        for i in range(int(apex_a[1]), int(apex_c[1] + 3)):
            if i in self.to_draw_coordinates_list and len(self.to_draw_coordinates_list[i]) > 1:
                for j in range(min(self.to_draw_coordinates_list[i]), max(self.to_draw_coordinates_list[i])):
                    if 0 <= j < self.display_width and 0 <= i < self.display_height:

                        point = [j, i, 0]
                        point[2] = MathHelper.z_frequency(apex_a, apex_b, apex_c, j, i)

                        if 0 < point[2] < self.z_buffer[point[1]][point[0]]:
                            pygame.draw.rect(self.display, lime_color, (point[0], point[1], 1, 1))
                            self.z_buffer[point[1]][point[0]] = point[2]

    # Calculation of coordinates for the sides of polygons
    def get_triangle_side(self, first_x, first_y, second_x, second_y):
        delta_x = 0
        delta_y = 0
        max_iterations_based_on_display_height = 0

        if abs(first_x - second_x) == 0:
            delta_x = 0
            delta_y = 1 if first_y < second_y else -1

        elif abs(first_y - second_y) == 0:
            delta_x = 1 if first_x < second_x else -1
            delta_y = 0

        elif abs(second_x - first_x) >= abs(second_y - first_y):
            delta_x = 1 if first_x < second_x else -1
            delta_y = (second_y - first_y) / abs(first_x - second_x)

        elif abs(second_x - first_x) < abs(second_y - first_y):
            delta_x = (second_x - first_x) / abs(first_y - second_y)
            delta_y = 1 if first_y < second_y else -1

        while max_iterations_based_on_display_height < self.display_height:
            first_y += delta_y
            first_x += delta_x

            if round(first_y) in self.to_draw_coordinates_list:
                self.to_draw_coordinates_list[round(first_y)].append(round(first_x))

            if (abs(delta_x) == 1 and abs(first_x - second_x) < 1) or \
               (abs(delta_y) == 1 and abs(first_y - second_y) < 1):
                break

            max_iterations_based_on_display_height += 1

    # Form polygons on borders
    def get_triangle_sides(self, apex_a, apex_b, apex_c):
        self.to_draw_coordinates_list = {y: [] for y in range(round(apex_a[1]), round(apex_c[1]) + 1)}

        self.get_triangle_side(round(apex_a[0]), round(apex_a[1]), round(apex_c[0]), round(apex_c[1]))
        self.get_triangle_side(round(apex_a[0]), round(apex_a[1]), round(apex_b[0]), round(apex_b[1]))
        self.get_triangle_side(round(apex_b[0]), round(apex_b[1]), round(apex_c[0]), round(apex_c[1]))

    # Calculation of max, min z_values, color step for three-dimensional picture
    def calculate_additional_z_values(self, i):
        z_max = 0
        z_min = 9999999

        for j in range(len(self.figure_projection[i])):
            if z_min > self.figure_projection[i][j][2]:
                z_min = self.figure_projection[i][j][2]
            if z_min > self.figure_projection[i - 1][j][2]:
                z_min = self.figure_projection[i - 1][j][2]
            if z_max < self.figure_projection[i][j][2]:
                z_max = self.figure_projection[i][j][2]
            if z_max < self.figure_projection[i - 1][j][2]:
                z_max = self.figure_projection[i - 1][j][2]

        z_color_step = (z_max - z_min) / 275
        return z_max, z_min, z_color_step


if __name__ == '__main__':
    FigureRendering().run()
