import pygame
from accessify import private
from math import pi
from .apex.apex import Apex


class FallingLeaf:
    def __init__(self, display_width=600, display_height=1000, fps=30):
        pygame.init()

        # Pygame window parameters
        self.fps = fps
        self.display_width = display_width
        self.display_height = display_height

        # pygame clock, display objects
        self.clock, self.display = None, None

        # Default colors
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "green": (20, 100, 0),
            "brown": (83, 21, 0),
            "blue": (179, 190, 255)
        }
        # Apex storage
        self.apex_list = []

        # Constants

        # The circle around which the leaf rotates
        self.x_center = display_width / 2
        self.y_center = 0.0
        self.radius = display_width // 4

        # Anchor point of the leaf shape
        self.anchor_leaf_coordinates = {
            "x": int(self.x_center + self.radius),
            "y": int(self.y_center)
        }
        # Rotation parameters
        self.radius_increase_coefficient = 1.003
        self.rotation_step = pi / 288
        self.current_angle = 0

        # Parameters for determinate the move direction of the leaf
        self.move_number = 1
        self.direction_multiplier = 1
        self.make_move = True

    def run(self):
        still_running = True
        self.initialize_pygame_window()
        self.create_leaf_apexes()

        # Main Loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    still_running = False
                    break

            # Quit if pygame window was closed
            if not still_running:
                break

            # When leaf fallen - stop moving, else - falling
            if self.make_move:
                self.let_leaf_fall()

            if self.apex_list[6].y >= self.display_height - 100:
                self.make_move = False

            # Draw scene
            self.draw_background()
            self.draw_leaf()

            pygame.display.update()
            self.clock.tick(self.fps)

    # Private methods
    @private
    def initialize_pygame_window(self):
        # Pygame window initialization
        pygame.init()
        pygame.display.set_caption('Falling Leaf')

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.display_width, self.display_height), pygame.RESIZABLE)

    @private
    def create_leaf_apexes(self):
        # Construct leaf
        self.apex_list.append(
            Apex(
                {
                    "x": self.anchor_leaf_coordinates["x"],
                    "y": self.anchor_leaf_coordinates["y"] - self.radius // 10,
                },
            )
        )
        self.apex_list.append(
            Apex(
                {
                    "x": self.anchor_leaf_coordinates["x"],
                    "y": self.anchor_leaf_coordinates["y"] - self.radius // 5,
                },
            )
        )
        self.apex_list.append(
            Apex(
                {
                    "x": self.anchor_leaf_coordinates["x"] - self.radius // 20,
                    "y": self.anchor_leaf_coordinates["y"] - 2*self.radius // 5,
                },
            )
        )
        self.apex_list.append(
            Apex(
                {
                    "x": self.anchor_leaf_coordinates["x"] - self.radius // 10,
                    "y": self.anchor_leaf_coordinates["y"],
                },
            )
        )
        self.apex_list.append(
            Apex(
                {
                    "x": self.anchor_leaf_coordinates["x"],
                    "y": self.anchor_leaf_coordinates["y"] + self.radius // 5,
                },
            )
        )
        self.apex_list.append(
            Apex(
                {
                    "x": self.anchor_leaf_coordinates["x"] + self.radius // 10,
                    "y": self.anchor_leaf_coordinates["y"] - self.radius // 10,
                },
            )
        )
        self.apex_list.append(Apex(self.anchor_leaf_coordinates))

    @private
    def define_move_direction(self):
        # This method defines direction by checking number of moves
        self.direction_multiplier = 1 if self.move_number % 2 == 1 else -1

    @private
    def let_leaf_fall(self):
        # This method rotates coordinates of leaf apexes
        for apex in self.apex_list:
            apex.rotate(
                self.x_center,
                self.y_center,
                self.radius_increase_coefficient,
                self.rotation_step * self.direction_multiplier
            )

        self.current_angle += self.rotation_step * self.direction_multiplier
        self.radius *= self.radius_increase_coefficient

        if self.apex_list[6].x <= 50 and self.direction_multiplier == 1 or \
           self.apex_list[6].x >= self.display_width - 50 and self.direction_multiplier == -1:

            self.move_number += 1
            self.define_move_direction()

    @private
    def draw_leaf(self):
        # This method draws leaf by drawing lines between apexes
        pygame.draw.polygon(self.display, self.colors["green"],
                            [[self.apex_list[1].x, self.apex_list[1].y], [self.apex_list[3].x, self.apex_list[3].y],
                             [self.apex_list[4].x, self.apex_list[4].y], [self.apex_list[5].x, self.apex_list[5].y]])
        pygame.draw.line(self.display, self.colors["black"],
                         [self.apex_list[0].x, self.apex_list[0].y], [self.apex_list[1].x, self.apex_list[1].y], 3)
        pygame.draw.line(self.display, self.colors["black"],
                         [self.apex_list[1].x, self.apex_list[1].y], [self.apex_list[2].x, self.apex_list[2].y], 3)
        pygame.draw.line(self.display, self.colors["black"],
                         [self.apex_list[1].x, self.apex_list[1].y], [self.apex_list[3].x, self.apex_list[3].y], 3)
        pygame.draw.line(self.display, self.colors["black"],
                         [self.apex_list[1].x, self.apex_list[1].y], [self.apex_list[5].x, self.apex_list[5].y], 3)
        pygame.draw.line(self.display, self.colors["black"],
                         [self.apex_list[4].x, self.apex_list[4].y], [self.apex_list[3].x, self.apex_list[3].y], 3)
        pygame.draw.line(self.display, self.colors["black"],
                         [self.apex_list[4].x, self.apex_list[4].y], [self.apex_list[5].x, self.apex_list[5].y], 3)

    @private
    def draw_background(self):
        # This method draws background
        pygame.draw.rect(self.display, self.colors["blue"], (0, 0, self.display_width, self.display_height - 100))
        pygame.draw.rect(self.display, self.colors["brown"], (0, self.display_height - 100, self.display_width, 100))
        pygame.draw.line(self.display, self.colors["black"],
                         [0, self.display_height - 100], [self.display_width, self.display_height - 100], 5)
