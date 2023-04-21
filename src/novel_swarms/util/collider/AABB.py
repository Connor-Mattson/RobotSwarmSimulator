import pygame

class AABB:
    def __init__(self, p1, p2):
        self.x_min = min(p1[0], p2[0])
        self.x_max = max(p1[0], p2[0])
        self.y_min = min(p1[1], p2[1])
        self.y_max = max(p1[1], p2[1])
        self.in_intersection = False

    def intersects(self, other) -> bool:
        return self.in_x_range(other) and self.in_x_range(other)

    def in_y_range(self, other) -> bool:
        y_range = min(self.y_max, other.y_max) - max(self.y_min, other.y_min)
        return y_range > 0

    def in_x_range(self, other) -> bool:
        x_range = min(self.x_max, other.x_max) - max(self.x_min, other.x_min)
        return x_range > 0

    def width(self):
        return self.x_max - self.x_min

    def height(self):
        return self.y_max - self.y_min

    def toggle_intersection(self):
        self.in_intersection = True

    def draw(self, screen, color=(0, 255, 0)):
        if self.in_intersection:
            color = (255, 255, 0)
        pygame.draw.rect(screen, color, pygame.Rect(self.x_min, self.y_min, self.width(), self.height()), 1)
