import numpy as np
from .AbstractInit import AbstractInitialization


class NGonInitialization(AbstractInitialization):
    """
    NGonInitialization: Initialize all agents at the vertices of a perfect n-gon
    """
    def __init__(self, n, radius, center=None):
        super().__init__()
        if center is None:
            center = [50, 50]
        self.n = n
        self.r = radius
        self.scale = 1
        self.scaled = False
        self.center = center
        self.positions = self.getPositions()

    def rescale(self, zoom_factor):
        self.scale = zoom_factor
        self.center[0] *= zoom_factor
        self.center[1] *= zoom_factor
        if not self.scaled:
            for line in self.positions:
                line[0] *= zoom_factor
                line[1] *= zoom_factor
            self.scaled = True

    def as_dict(self):
        return {
            "type": "NGonInitialization",
            "n" : self.n,
            "r": self.r,
        }

    @staticmethod
    def from_dict(d):
        return NGonInitialization(d.get("n"), d.get("r"))

    def getShallowCopy(self):
        return self.from_dict(self.as_dict())

    def getPositions(self):
        positions = []
        angle_offset = (2 * np.pi) / self.n
        circle_angle = 0
        for n in range(self.n):
            x = (np.cos(circle_angle) * self.r) + self.center[0]
            y = (np.sin(circle_angle) * self.r) + self.center[1]
            theta = circle_angle - (np.pi / 2)
            positions.append([x, y, theta])
            circle_angle += angle_offset
        return positions