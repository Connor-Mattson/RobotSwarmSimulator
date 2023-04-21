import pygame
import numpy as np
import math
from .CircularCollider import CircularCollider

class AngleSensitiveCC(CircularCollider):
    def __init__(self, x, y, r, theta, action, sensitivity=30):
        super().__init__(x, y, r)
        self.v_to_o = np.array([0, 0])
        self.theta = theta
        self.s = sensitivity  # In Degrees
        self.within_range = False
        self.action = action
        self.v_f = np.array([0, 0])
        self.v_c = np.array([0, 0])

    def collision_then_correction(self, other):
        fp_x, fp_y = self.get_frontal_point()
        self.v_f = np.array([fp_x, fp_y])
        self.v_to_o = other.v - self.v

        ret = super().collision_then_correction(other)
        self.within_range = False
        if ret is None:
            return None

        angle = self.get_angle_between()
        if angle < np.radians(self.s):
            self.within_range = True
            return np.array([0, 0])
        return ret

    def draw(self, screen, color=(0, 255, 0)):
        SHOW_ANGLE_VECTORS = True
        width = 2
        if self.within_range:
            color = (255, 255, 255)
            width = 10
        pygame.draw.line(screen, color, (self.x, self.y), (self.x + self.v_to_o[0], self.y + self.v_to_o[1]), width)
        pygame.draw.circle(screen, color, (self.x, self.y), self.r, 1)

        if SHOW_ANGLE_VECTORS:
            print(self.v_to_o, self.v_f, self.v_c)
            print(self.within_range)
            pygame.draw.circle(screen, (255, 0, 255), (self.x + self.v_f[0], self.y + self.v_f[1]), 5, 0)
            pygame.draw.circle(screen, (255, 255, 0), (self.x + self.v_to_o[0], self.y + self.v_to_o[1]), 5, 0)
            pygame.draw.line(screen, (255, 0, 255), (self.x, self.y), (self.x + (self.v_f[0] * 4), self.y + (self.v_f[1] * 4)), 2)
            pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), (self.x + (self.v_to_o[0] * 4), self.y + (self.v_to_o[1] * 4)), 2)

    def get_angle_between(self):
        return np.arccos(np.dot(self.v_f, self.v_to_o) / (np.linalg.norm(self.v_f) * np.linalg.norm(self.v_to_o)))

    def get_frontal_point(self):
        """
        Returns the location on the circumference that represents the "front" of the robot
        """
        return math.cos(self.theta) * self.r, math.sin(self.theta) * self.r

    def is_angle_breached(self) -> bool:
        return self.within_range
