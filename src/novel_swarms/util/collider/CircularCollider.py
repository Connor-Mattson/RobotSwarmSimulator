import pygame
import numpy as np

class CircularCollider:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.v = np.array([x, y])
        self.collision_flag = False

    def update(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.v = np.array([x, y])

    def flag_collision(self):
        self.collision_flag = True

    def collision_then_correction(self, other):
        dist_between_radii = self.dist(other)
        dist_difference = (self.r + other.r) - dist_between_radii
        if dist_difference < 0:
            return None
        correction_vector = ((other.v - self.v) / (dist_between_radii + 0.001)) * (dist_difference + 0.01)
        return -correction_vector

    def dist(self, other):
        return np.linalg.norm(other.v - self.v)

    def draw(self, screen, color=(0, 255, 0)):
        if self.collision_flag:
            color = (255, 0, 0)
        pygame.draw.circle(screen, color, (self.x, self.y), self.r, 3)
