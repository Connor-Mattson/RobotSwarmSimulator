import math

import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior

class DistanceToGoal(AbstractBehavior):

    def __init__(self, history=100):
        super().__init__(name = "Goal_Dist", history_size=history)
        self.population = None
        self.goals = None

    def attach_world(self, world):
        self.population = world.population
        self.goals = world.goals

    def calculate(self):
        if not self.goals or not self.population:
            self.set_value(0.0)

        distances = []
        for agent in self.population:
            dist_to_goals = []
            for goal in self.goals:
                d = self.calc_dist_to_goal(agent, goal)
                dist_to_goals.append(d)
            distances.append(min(dist_to_goals))
        if distances:
            self.set_value(np.average(distances))
        else:
            self.set_value(0.0)

    def calc_dist_to_goal(self, agent, goal):
        if goal.agent_achieved_goal(agent):
            return 0.0
        a_pos = [agent.x_pos, agent.y_pos]
        goal_positions = [goal.rect.topleft, goal.rect.topright, goal.rect.bottomleft, goal.rect.bottomright]
        dist_squared = []
        for x, y in goal_positions:
            dist_squared.append((x - a_pos[0]) ** 2 + (y - a_pos[1]) ** 2)
        return math.sqrt(min(dist_squared))