from math import sin, cos


class Apex:
    def __init__(self, coordinates, angle=0):
        self.x = coordinates["x"]
        self.y = coordinates["y"]
        self.angle = angle

    def rotate(self, x_center, y_center, rotation_step, rotation_angle):
        self.angle = rotation_angle
        self.x = x_center + (self.x - x_center) * cos(self.angle) - (self.y - y_center) * sin(self.angle)
        self.y = y_center + (self.x - x_center) * sin(self.angle) + (self.y - y_center) * cos(self.angle)
        self.x = x_center + (self.x - x_center) * rotation_step
        self.y = y_center + (self.y - y_center) * rotation_step
