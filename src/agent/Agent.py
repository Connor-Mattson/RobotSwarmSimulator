import numpy
from abc import abstractmethod
from typing import Tuple

class Agent():

    name = "Agent"
    x_pos = 100
    y_pos = 100
    dy = 0
    dx = 0

    def __init__(self, x, y, name = None) -> None:
        self.x_pos = x
        self.y_pos = y
        self.name = name
        pass

    def step(self, check_for_world_boundaries = None) -> None:
        pass

    def draw(self, screen) -> None:
        pass

    def getPosition(self):
        return numpy.array([self.x_pos, self.y_pos])

    def getVelocity(self):
        return numpy.array([self.dx, self.dy])