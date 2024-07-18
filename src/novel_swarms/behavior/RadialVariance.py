import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior


class RadialVarianceBehavior(AbstractBehavior):
    def __init__(self, history=100, regularize=True, ceil=None, floor=None):
        super().__init__(name="Radial_Variance", history_size=history)
        self.population = None
        self.world_radius = 0
        self.regularize = regularize
        self.ceil = ceil
        self.floor = floor

    def attach_world(self, world):
        self.population = world.population
        self.world_radius = world.config.radius

    def attach_population(self, pop):
        self.population = pop

    def calculate(self):
        n = len(self.population)
        r = self.world_radius
        mew = self.center_of_mass()

        # Calculate the Average distance from C.O.M. for all agents first, save to variable 'avg_dist'
        distance_list = []
        for agent in self.population:
            x_i = agent.getPosition()
            distance = np.linalg.norm(x_i - mew)
            distance_list.append(distance)
        avg_dist = np.average(distance_list)

        variance_list = []
        for agent in self.population:
            x_i = agent.getPosition()
            distance = np.linalg.norm(x_i - mew)
            variance = (distance - avg_dist) ** 2  # Square to make positive(?)
            variance_list.append(variance)

        scaling_factor = (1 / (r * r * n)) if self.regularize else (1 / n)
        radial_variance = sum(variance_list) * scaling_factor

        if self.ceil is not None:
            radial_variance = min(self.ceil, radial_variance)
        if self.floor is not None:
            radial_variance = max(self.floor, radial_variance)
        self.set_value(radial_variance)

    def center_of_mass(self):
        positions = [
            [
                agent.getPosition()[i] for agent in self.population
            ] for i in range(len(self.population[0].getPosition()))
        ]
        center = np.array([np.average(pos) for pos in positions])
        return center
