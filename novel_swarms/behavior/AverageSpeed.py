import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior


class AverageSpeedBehavior(AbstractBehavior):
    def __init__(self, history=100):
        super().__init__(name="Average Speed", history_size=history)
        self.population = None

    def attach_world(self, world):
        self.population = world.population

    def calculate(self):
        n = len(self.population)
        velocities = [np.linalg.norm(agent.getVelocity()) for agent in self.population]
        average_speed = sum(velocities) / n
        self.set_value(average_speed)
