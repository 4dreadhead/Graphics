import pygame
from accessify import private


class LinesGenerator:
    def __init__(self, fps=10, display_width=1400, display_height=800):
        # pygame window params
        self.fps = fps
        self.display_width = display_width
        self.display_height = display_height

        # coordinates of triangle apexes
        self.first_triangle, self.second_triangle = {}, {}

        # drawing steps (pseudo-pixel size)
        self.first_width_step, self.first_height_step = 10, 10
        self.second_width_step, self.second_height_step = 20, 20

        # pygame clock, display objects
        self.clock, self.display = None, None

    def run(self):
        self.initialize_pygame_window()

        # Main loop
        while True:
            # Catching resize events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.VIDEORESIZE:
                    self.display_width = event.w
                    self.display_height = event.h
                    self.display = pygame.display.set_mode((self.display_width, self.display_height), pygame.RESIZABLE)

            # Skip draw scene when window size too small
            if self.display_width < 100 or self.display_height < 100:
                continue

            self.display.fill((25, 25, 25))

            self.get_coordinates_with_screen_size()

            # Drawing lines
            for index in range(1, 4):
                first_dot, second_dot = (index, 1) if index == 3 else (index, index + 1)

                # Using '//' + '*' for round to pseudo-pixel size
                self.unbalanced_algorithm(
                    self.first_triangle[first_dot]["x"] // self.first_width_step * self.first_width_step,
                    self.first_triangle[first_dot]["y"] // self.first_height_step * self.first_height_step,
                    self.first_triangle[second_dot]["x"] // self.first_width_step * self.first_width_step,
                    self.first_triangle[second_dot]["y"] // self.first_height_step * self.first_height_step,
                    self.first_width_step,
                    self.first_height_step
                )
                self.bresenham_algorithm(
                    self.second_triangle[first_dot]["x"] // self.second_width_step * self.second_width_step,
                    self.second_triangle[first_dot]["y"] // self.second_height_step * self.second_height_step,
                    self.second_triangle[second_dot]["x"] // self.second_width_step * self.second_width_step,
                    self.second_triangle[second_dot]["y"] // self.second_height_step * self.second_height_step,
                    self.second_width_step,
                    self.second_height_step
                )

            pygame.display.update()
            self.clock.tick(self.fps)

    # Private methods
    @private
    def initialize_pygame_window(self):
        # Pygame window initialization
        pygame.init()
        pygame.display.set_caption('Star')

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.display_width, self.display_height), pygame.RESIZABLE)

    @private
    def get_coordinates_with_screen_size(self):
        # second method triangle apexes coordinates
        if self.display_width >= self.display_height:
            indent = (self.display_width - self.display_height) // 2
            self.second_triangle = {
                1: {
                        "x": indent,
                        "y": self.display_height // 4
                },
                2: {
                        "x": self.display_width - indent,
                        "y": self.display_height // 4
                },
                3: {
                        "x": self.display_width // 2,
                        "y": self.display_height
                }
            }
        else:
            indent = (self.display_width - self.display_height) // 2
            self.second_triangle = {
                1: {
                    "x": 0,
                    "y": (self.display_height - (self.display_width * 3 ** 0.5) / 3) // 2
                },
                2: {
                    "x": self.display_width,
                    "y": (self.display_height - (self.display_width * 3 ** 0.5) / 3) // 2
                },
                3: {
                    "x": self.display_width // 2,
                    "y": self.display_height - indent
                }
            }
        # first method triangle apexes coordinates based on second
        self.first_triangle = {
            1: {
                "x": self.second_triangle[1]["x"],
                "y": self.display_height - self.second_triangle[1]["y"]
            },
            2: {
                "x": self.second_triangle[2]["x"],
                "y": self.display_height - self.second_triangle[2]["y"]
            },
            3: {
                "x": self.second_triangle[3]["x"],
                "y": self.display_height - self.second_triangle[3]["y"]
            }
        }

    @private
    def unbalanced_algorithm(self, first_x, first_y, second_x, second_y, step_x, step_y):
        # :params first_x, first_y: coordinates of first given apex
        # :params second_x, second_y: coordinates of second given apex
        # :params step_x, step_y: steps size (pseudo-pixels)

        delta_x = 0
        delta_y = 0

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

        while True:
            pygame.draw.rect(
                self.display,
                (0, 255, 0),
                (
                    first_x // step_x * step_x,
                    first_y // step_y * step_y,
                    step_x,
                    step_y
                )
            )

            first_y += delta_y * step_y
            first_x += delta_x * step_x

            if (abs(delta_x) == 1 and abs(first_x - second_x) < step_x) or \
               (abs(delta_y) == 1 and abs(first_y - second_y) < step_y):
                break

    @private
    def bresenham_algorithm(self, first_x, first_y, second_x, second_y, step_x, step_y):
        # :params first_x, first_y: coordinates of first given apex
        # :params second_x, second_y: coordinates of second given apex
        # :params step_x, step_y: steps size (pseudo-pixels)

        if first_y > second_y:
            # swap apexes
            first_x, first_y, second_x, second_y = second_x, second_y, first_x, first_y

        diff_x = second_x - first_x
        diff_y = second_y - first_y

        delta_x = step_x if diff_x >= 0 else -step_x
        diff_x = abs(diff_x)

        current_diff = 0

        # Two situations:
        # First - when difference by 'y' more than difference by 'x'
        if diff_y > diff_x:
            step = diff_x
            current_position = diff_y

            while first_y != second_y:
                pygame.draw.rect(self.display, (255, 0, 0), (first_x, first_y, step_x, step_y))
                first_y += step_y
                current_diff += step
                if current_diff > diff_y:
                    first_x += delta_x
                    current_diff -= current_position
            pygame.draw.rect(self.display, (255, 0, 0), (first_x, first_y, step_x, step_y))

        # Second - when difference by 'x' more than difference by 'y'
        else:
            step = diff_y
            current_position = diff_x

            while first_x != second_x:
                pygame.draw.rect(self.display, (255, 0, 0), (first_x, first_y, step_x, step_y))
                first_x += step_x
                current_diff += step
                if current_diff > diff_x:
                    first_y += diff_y
                    current_diff -= current_position
            pygame.draw.rect(self.display, (255, 0, 0), (first_x, first_y, step_x, step_y))


if __name__ == '__main__':
    LinesGenerator().run()
