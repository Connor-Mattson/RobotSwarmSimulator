import numpy as np
from typing import List
from src.behavior.AbstractBehavior import AbstractBehavior

class ScatterBehavior(AbstractBehavior):
    def __init__(self, population: List, r: float):
        super().__init__(name = "Scatter")
        self.population = population
        self.world_radius = r

    def calculate(self):
        n = len(self.population)
        r = self.world_radius

        distance_list = []
        mew = self.center_of_mass()

        for agent in self.population:
            x_i = agent.getPosition()

            distance = np.linalg.norm(x_i - mew) ** 2
            distance_list.append(distance)

        scatter = sum(distance_list) / (r * r * n)
        self.set_value(scatter)    

    def center_of_mass(self):
        positions = [
            [
                agent.getPosition()[i] for agent in self.population
            ] for i in range(len(self.population[0].getPosition()))
        ]
        center = np.array([np.average(pos) for pos in positions])
        return center