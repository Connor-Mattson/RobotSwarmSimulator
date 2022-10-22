import math

import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior


class GeneElementDifference(AbstractBehavior):

    def __init__(self, genome_a_index, genome_b_index, history=100):
        super().__init__(name="SensorOffset", history_size=history)
        self.population = 0
        self.a = genome_a_index
        self.b = genome_b_index

    def attach_world(self, world):
        self.population = world.population

    def calculate(self):
        a_theta = self.population[0].controller[self.a]
        b_theta = self.population[0].controller[self.b]
        sensor_angle = abs(a_theta - b_theta) / (2 * math.pi)
        self.set_value(sensor_angle)

