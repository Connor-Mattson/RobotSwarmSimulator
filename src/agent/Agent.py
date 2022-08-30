import math

import numpy
from abc import abstractmethod
from typing import Tuple


class Agent:

    def __init__(self, x, y, name=None) -> None:
        self.x_pos = x
        self.y_pos = y
        self.name = name
        self.dy = 0
        self.dx = 0
        self.angle = 0
        pass

    def step(self, check_for_world_boundaries=None) -> None:
        pass

    def draw(self, screen) -> None:
        pass

    def getPosition(self):
        return numpy.array([self.x_pos, self.y_pos])

    def getVelocity(self):
        return numpy.array([self.dx, self.dy])

    def getFrontalPoint(self) -> Tuple:
        """
        Returns the location on the circumference that represents the "front" of the robot
        """
        return self.x_pos + math.cos(self.angle), self.y_pos + math.sin(self.angle)
