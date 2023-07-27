import numpy as np
import pygame.draw
import shapely
from ...world.objects.WorldObject import WorldObject

class GrowthRegion(WorldObject):
    def __init__(self, world, points, growth_step=1, growth_method="Centroid", detectable=False):
        super().__init__(world, detectable)
        self.points = np.array(points)
        self.step_size = growth_step
        self.method = growth_method
        self.centroid = self.get_centroid()

    def get_centroid(self):
        return np.mean(self.points, axis=0)

    def step(self):
        if self.method == "Centroid":
            for i in range(len(self.points)):
                # print(f"Before: {self.points[i]}")
                self.points[i] += ((self.points[i] - self.centroid) / np.linalg.norm(self.points[i] - self.centroid)) * self.step_size
                # print(f"After: {self.points[i]}")

    def draw(self, screen):
        pygame.draw.polygon(screen, (200, 0, 0), self.points, width=0)

    def point_inside(self, point):
        poly = shapely.Polygon([shapely.Point(p) for p in self.points])
        return poly.contains(shapely.Point(point))