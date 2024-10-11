import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior


class AverageSpeedBehavior(AbstractBehavior):
    def __init__(self, history=100, normalization_constant=1):
        super().__init__(name="Average_Speed", history_size=history)
        self.population = None
        self.normalization_constant = normalization_constant

    def attach_world(self, world):
        self.population = world.population

    def calculate(self):
        n = len(self.population)
        velocities = [np.linalg.norm(agent.getVelocity()) for agent in self.population]
        average_speed = sum(velocities) / (self.normalization_constant * n)
        self.set_value(average_speed)

    def as_config_dict(self):
        return {"name": self.name, "history_size": self.history_size, "normalization": self.normalization_constant}
