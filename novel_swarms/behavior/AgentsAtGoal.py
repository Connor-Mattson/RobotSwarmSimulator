import math

import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior


class AgentsAtGoal(AbstractBehavior):
    def __init__(self, history=100):
        super().__init__(name="Goal_Agents", history_size=history)
        self.population = None
        self.goals = None

    def attach_world(self, world):
        self.population = world.population
        self.goals = world.goals

    def calculate(self):
        if not self.goals or not self.population:
            self.set_value(0.0)

        total_agents = 0
        for goal in self.goals:
            total_agents += goal.get_count()
        self.set_value(total_agents)