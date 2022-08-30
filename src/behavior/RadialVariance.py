import numpy as np
from typing import List
from src.behavior.AbstractBehavior import AbstractBehavior

class RadialVarianceBehavior(AbstractBehavior):
    def __init__(self, population: List, r: float):
        super().__init__(name = "Radial Variance")
        self.population = population
        self.world_radius = r

    def calculate(self):
        n = len(self.population)
        r = self.world_radius
        mew = self.center_of_mass()

        # Calculate the Average disance from C.O.M. for all agents first, save to variable 'avg_dist'
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
            variance = (distance - avg_dist) ** 2      # Square to make positive(?)
            variance_list.append(variance)

        radial_variance = sum(variance_list) / (r * r * n)

        WEIGHT = 20.0
        self.set_value(radial_variance * WEIGHT)    

    def center_of_mass(self):
        positions = [
            [
                agent.getPosition()[i] for agent in self.population
            ] for i in range(len(self.population[0].getPosition()))
        ]
        center = np.array([np.average(pos) for pos in positions])
        return center