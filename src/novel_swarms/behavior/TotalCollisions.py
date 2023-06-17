import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior


class TotalCollisionsBehavior(AbstractBehavior):
    def __init__(self, history=1):
        super().__init__(name="Total_Collisions", history_size=history)
        self.population = None
        self.total_collisions = 0

    def attach_world(self, world):
        self.population = world.population
        self.total_collisions = 0

    def calculate(self):
        for agent in self.population:
            if agent.collision_flag:
                self.total_collisions += 1
        self.set_value(self.total_collisions)
