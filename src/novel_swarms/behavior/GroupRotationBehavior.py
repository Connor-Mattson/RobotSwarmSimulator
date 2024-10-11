import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior

class GroupRotationBehavior(AbstractBehavior):

    def __init__(self, history=100, normalization_constant=1):
        super().__init__(name="Group_Rotation", history_size=history)
        self.population = None
        self.normalization_constant = normalization_constant

    def attach_world(self, world):
        self.population = world.population

    def calculate(self):
        n = len(self.population)
        if n == 1:
            self.set_value(0.0)
            return

        momentum_list = []
        mew = self.center_of_mass()

        for agent in self.population:
            x_i = agent.getPosition()
            v_i = agent.getVelocity()

            distance_unit_vector = (x_i - mew) / np.linalg.norm(x_i - mew)
            momentum = np.cross(v_i, distance_unit_vector)
            momentum_list.append(momentum)

        normalized_momentum = sum(momentum_list) / (n * self.normalization_constant)
        self.set_value(normalized_momentum)    

    def center_of_mass(self):
        positions = [
            [
                agent.getPosition()[i] for agent in self.population
            ] for i in range(len(self.population[0].getPosition()))
        ]
        center = np.array([np.average(pos) for pos in positions])
        return center

    def as_config_dict(self):
        return {"name": self.name, "history_size": self.history_size, "normalization": self.normalization_constant}