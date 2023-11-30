import pygame
import numpy as np

class CircularCollider:
    def __init__(self, x, y, r, dx, dy, parent=None):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.v = np.array([x, y])
        self.collision_flag = False
        self.parent = parent

    def update(self, x, y, r, dx, dy):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.v = np.array([x, y])

    def flag_collision(self):
        self.collision_flag = True

    def collision_then_correction(self, other):
        dist_between_radii = self.dist(other)
        dist_difference = (self.r + other.r) - dist_between_radii
        if dist_difference < 0:
            return None

        # Old Correction Vector (Sliding)
        # correction_vector = ((other.v - self.v) / (dist_between_radii + 0.001)) * (dist_difference + 0.01)

        me_velocity = np.array([self.dx, self.dy])
        other_velocity = np.array([other.dx, other.dy])
        correction_vector_me = -1 * (np.dot(me_velocity - other_velocity, self.v - other.v) / (np.linalg.norm(self.v - other.v) ** 2)) * (self.v - other.v)
        correction_vector_other = -1 * (np.dot(other_velocity - me_velocity, other.v - self.v) / (np.linalg.norm(other.v - self.v) ** 2)) * (other.v - self.v)
        if dist_difference > 0:
            correction_vector_me += - (other.v - self.v)

        other.parent.elastic_correction += correction_vector_other
        return correction_vector_me

    def dist(self, other):
        return np.linalg.norm(other.v - self.v)

    def draw(self, screen, color=(0, 255, 0)):
        if self.collision_flag:
            color = (255, 0, 0)
        pygame.draw.circle(screen, color, (self.x, self.y), self.r, 3)
