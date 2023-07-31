import math

import copy
import numpy as np
from typing import List
import warnings
from .AbstractBehavior import AbstractBehavior
from ..agent.MazeAgent import MazeAgent

class AgentsAtGoal(AbstractBehavior):
    def __init__(self, name="Goal_Agents", history=100):
        super().__init__(name=name, history_size=history)
        self.population = None
        self.goals = None
        self.world = None

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
        self.set_value(count)

        # total_agents = 0
        # for goal in self.goals:
        #     total_agents += goal.get_count()
        # self.set_value(total_agents)

class PercentageAtGoal(AgentsAtGoal):
    def __init__(self, percentage, history=100):
        super().__init__(name=f"{round(percentage * 100)}-At-Goal:", history=history)
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
