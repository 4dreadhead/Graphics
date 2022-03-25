from .three_dimension_transformation.three_dimensional_transformation import ThreeDimensionalTransformation
from .three_dimension_transformation.transform_helper import TransformHelper
import pygame
import numpy as np


class ActionControl(ThreeDimensionalTransformation):
    def run(self):
        still_running = True
        self.initialize_pygame_window()
        self.set_figure()

        x_count, y_count, z_count, second_x_count, second_y_count = 0, 0, 0, 0, 0

        self.display.fill((201, 232, 232))

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

            self.display.fill((201, 232, 232))

            # 1. Action control zone
            keys = pygame.key.get_pressed()
            counters = x_count, y_count, z_count, second_x_count, second_y_count
            x_count, y_count, z_count, second_x_count, second_y_count = self.catch_events(keys, counters)
            counters = x_count, y_count, z_count, second_x_count, second_y_count

            # 2. Transform zone
            self.transform(counters)

            # 3. Draw scene
            self.draw_figure()
            pygame.display.update()
            self.clock.tick(self.fps)

    # Catching events from keyboard
    def catch_events(self, keys, event_counters):
        x_count, y_count, z_count, second_x_count, second_y_count = event_counters
        if keys[pygame.K_s]:
            self.viewpoint_vector[0] += self.control_step_x
            self.viewpoint_vector[1] += self.control_step_y
            self.viewpoint_vector[2] += self.control_step_z
        if keys[pygame.K_w]:
            self.viewpoint_vector[0] -= self.control_step_x
            self.viewpoint_vector[1] -= self.control_step_y
            self.viewpoint_vector[2] -= self.control_step_z
        if keys[pygame.K_UP] and x_count < 10:
            x_count += 1
        if keys[pygame.K_DOWN] and x_count > -10:
            x_count -= 1
        if keys[pygame.K_LEFT] and y_count > -10:
            y_count -= 1
        if keys[pygame.K_RIGHT] and y_count < 10:
            y_count += 1
        if keys[pygame.K_a] and z_count > -10:
            z_count -= 1
        if keys[pygame.K_d] and z_count < 10:
            z_count += 1
        if keys[pygame.K_u]:
            second_x_count -= 1
        if keys[pygame.K_j]:
            second_x_count += 1
        if keys[pygame.K_h]:
            second_y_count -= 1
        if keys[pygame.K_k]:
            second_y_count += 1

        return x_count, y_count, z_count, second_x_count, second_y_count

    # Transform from figure to display picture
    def transform(self, counters):
        x_count, y_count, z_count, second_x_count, second_y_count = counters
        for i in range(len(self.figure)):
            for j in range(len(self.figure[i])):
                if x_count != 0:
                    self.figure[i][j] = np.matmul(self.figure[i][j], TransformHelper.x_turn(x_count * np.pi / 600))
                if y_count != 0:
                    self.figure[i][j] = np.matmul(self.figure[i][j], TransformHelper.y_turn(y_count * np.pi / 600))
                if z_count != 0:
                    self.figure[i][j] = np.matmul(self.figure[i][j], TransformHelper.z_turn(z_count * np.pi / 600))

        self.view_transform()

        for i in range(len(self.figure_view)):
            for j in range(len(self.figure_view[i])):
                self.figure_view[i][j] = np.matmul(self.figure_view[i][j],
                                                   TransformHelper.x_turn(second_x_count * np.pi / 250))
                self.figure_view[i][j] = np.matmul(self.figure_view[i][j],
                                                   TransformHelper.y_turn(second_y_count * np.pi / 250))

        self.perspective_transform()
