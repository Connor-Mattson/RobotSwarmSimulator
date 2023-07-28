import math

import copy
import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior
from ..agent.MazeAgent import MazeAgent
from ..util.geometry.Point import Point
from ..util.geometry.ConvexHull import ConvexHull as CH
from ..util.geometry.Polygon import Polygon

class ConvexHull(AbstractBehavior):
    def __init__(self, name="Convex_Hull_Area", history=100):
        super().__init__(name=name, history_size=history)
        self.population = None
        self.goals = None
        self.world = None
        self.polygon = None

    def attach_world(self, world):
        self.population = world.population
        self.goals = world.goals
        self.world = world

    def calculate(self):
        if not self.world:
            self.set_value(math.nan)
        points = [Point.from_agent(a) for a in self.world.population]
        try:
            self.polygon = CH(method="Graham").find_hull(points)
        except:
            try:
                self.polygon = CH(method="Wrapping").find_hull(points)
            except Exception as e1:
                print(f"ConvexHull Calculation Error! {e1}")
                self.polygon = Polygon()

        self.set_value(self.polygon.area())

    def draw(self, screen):
        if not self.polygon:
            return
        self.polygon.draw(screen, color=(0, 255, 0), width=4)


class InverseConvexHull(AbstractBehavior):
    def __init__(self, name="Inverse_Hull_Area", history=100):
        super().__init__(name=name, history_size=history)
        self.population = None
        self.goals = None
        self.world = None
        self.polygon = None

    def attach_world(self, world):
        self.population = world.population
        self.goals = world.goals
        self.world = world

    def get_inverse_point(self, p, centroid, inverse_dist):
        p_new = centroid.p + ((inverse_dist / p.dist(centroid)) * (p.p - centroid.p))
        return Point.from_vector(p_new)

    def calculate(self):
        if not self.world:
            self.set_value(math.nan)
        points = [Point.from_agent(a) for a in self.world.population]
        centroid = Point.get_centroid(points)
        distances = [p.dist(centroid) for p in points]
        distance_points = zip(distances, points)
        dp = sorted(distance_points)
        point_length = len(dp)

        # Create a mapping from inverse points to points, so we can convert the inverse Hull back into the workspace.
        inverse_dict = {
            self.get_inverse_point(dp[i][1], centroid, dp[point_length - 1 - i][0]): dp[i][1]
            for i in range(point_length)
        }
        inv_points = list(inverse_dict.keys())

        try:
            inv_hull = CH(method="Graham").find_hull(inv_points)
        except Exception as e:
            try:
                inv_hull = CH(method="Wrapping").find_hull(inv_points)
            except Exception as e1:
                print(f"InverseConvexHull Calculation Error! {e1}")
                self.set_value(-1.0)
                return

        self.polygon = Polygon()
        for p in inv_hull.boundary:
            self.polygon.addPoint(inverse_dict[p])

        self.set_value(self.polygon.area())

    def draw(self, screen):
        if not self.polygon:
            return
        self.polygon.draw(screen, color=(255, 0, 0), width=4)