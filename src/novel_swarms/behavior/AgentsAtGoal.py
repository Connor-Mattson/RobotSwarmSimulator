import math

import copy
import numpy as np
from typing import List
import warnings
from .AbstractBehavior import AbstractBehavior
from ..agent.MazeAgent import MazeAgent

class AgentsAtGoal(AbstractBehavior):
    def __init__(self, name="Goal_Agents", history=100, as_percent=False):
        super().__init__(name=name, history_size=history)
        self.population = None
        self.goals = None
        self.world = None
        self.as_percent = as_percent

    def attach_world(self, world):
        self.population = world.population
        self.goals = world.goals
        self.world = world

    def calculate(self):
        if not self.goals or not self.population:
            self.set_value(0.0)
            warnings.warn("Agents at Goal behavior was assigned but no goal was detected for this world!")

        count = 0
        for agent in self.population:
            for goal in self.goals:
                if goal.agent_achieved_goal(agent):
                    count += 1
        if self.as_percent:
            count = round(count / len(self.population), 3)
        self.set_value(count)

        # total_agents = 0
        # for goal in self.goals:
        #     total_agents += goal.get_count()
        # self.set_value(total_agents)

    def as_config_dict(self):
        return {"name": self.name, "history_size": self.history_size, "as_percent": self.as_percent}

class PercentageAtGoal(AgentsAtGoal):
    def __init__(self, percentage, history=100):
        super().__init__(name=f"p{round(percentage * 100)}_at_goal", history=history)
        self.percentage = percentage
        self.found = None

    def calculate(self):
        v = 0.0
        if not self.goals or not self.population:
            self.set_value(0.0)

        if self.found:
            self.set_value(self.found)
            return

        count = 0
        for agent in self.population:
            for goal in self.goals:
                if goal.agent_achieved_goal(agent):
                    count += 1
        v = count

        if v / self.world.population_size >= self.percentage:
            self.found = float(self.world.total_steps)
            self.set_value(self.found)
        else:
            self.set_value(int(self.world.total_steps))

    def as_config_dict(self):
        return {"name": self.name, "history_size": self.history_size, "percentage": self.percentage}