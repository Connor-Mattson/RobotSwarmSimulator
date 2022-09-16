import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior


class ScatterBehavior(AbstractBehavior):
    def __init__(self, history=100):
        super().__init__(name="Scatter", history_size=history)
        self.population = None
        self.world_radius = 0

    def attach_world(self, world):
        self.population = world.population
        self.world_radius = world.config.radius

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
