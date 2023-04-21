import pygame
from ..WorldObject import WorldObject

class Wall(WorldObject):
    def __init__(self, world, x, y, w, h, angle=0, color=(255, 255, 255), detectable=True):
        super().__init__(world, detectable)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.angle = angle
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))

    def get_sensing_segments(self):
        if not self.detectable:
            return []
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        return [
            [rect.topleft, rect.topright],
            [rect.topright, rect.bottomright],
            [rect.bottomright, rect.bottomleft],
            [rect.bottomleft, rect.topleft]
        ]

    def get_collision_segments(self):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        return [
            [rect.topleft, rect.topright],
            [rect.topright, rect.bottomright],
            [rect.bottomright, rect.bottomleft],
            [rect.bottomleft, rect.topleft]
        ]

    def __repr__(self):
        return f"Wall(None, {self.x}, {self.y}, {self.w}, {self.h})"
