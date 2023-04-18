import pygame
import numpy as np

class Polygon:
    def __init__(self, points=None):
        if points:
            self.boundary = points
        else:
            self.boundary = []

    def addPoint(self, point):
        self.boundary.append(point)

    def draw(self, screen, color=(255, 255, 255), width=1):
        pygame.draw.polygon(screen, color, [(p.x, p.y) for p in self.boundary], width=width)

    def __getitem__(self, item):
        return self.boundary[item % len(self.boundary)]

    def __len__(self):
        return len(self.boundary)

    def area(self):
        minuses = 0
        pluses = 0
        if len(self.boundary) < 3:
            return 0.0

        for i in range(len(self.boundary)):
            pluses += self.__getitem__(i).x * self.__getitem__(i + 1).y
            minuses += self.__getitem__(i + 1).x * self.__getitem__(i).y

        return abs((pluses - minuses) / 2)


class Triangle:
    def __init__(self, p0, p1, p2):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2

    def ccw(self):
        v1 = np.array(self.p1.p - self.p0.p)
        v2 = np.array(self.p2.p - self.p0.p)
        z = np.cross(v1, v2)
        return z > 0
