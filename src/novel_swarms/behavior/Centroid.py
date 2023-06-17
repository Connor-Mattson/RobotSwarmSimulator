import math

import copy
import warnings

import numpy as np
from typing import List

import pygame.draw

from .AbstractBehavior import AbstractBehavior
from ..agent.MazeAgent import MazeAgent
from ..util.geometry.Point import Point
from ..util.geometry.ConvexHull import ConvexHull as CH
from ..util.geometry.Polygon import Polygon

class Centroid(AbstractBehavior):
    def __init__(self, name="Centroid", history=100):
        super().__init__(name=name, history_size=history)
        self.population = None
        self.centroid = np.array([0.0, 0.0], dtype=np.float64)

    def attach_world(self, world):
        self.population = world.population
        self.goals = world.goals
        self.world = world

    def calculate(self):
        if not self.world:
            self.set_value(np.array([0.0, 0.0], dtype=np.float64))
        points = [Point.from_agent(a) for a in self.world.population]
        try:
            c = np.array([0.0, 0.0], dtype=np.float64)
            for p in points:
                c += np.array([p.x, p.y])
            c /= len(points)
            self.centroid = c
        except Exception as e:
            raise e

        self.set_value(self.centroid)

    def draw(self, screen):
        for centroid in self.value_history:
            pygame.draw.circle(screen, (255, 0, 255), centroid, 5, width=0)
