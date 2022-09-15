import math

import numpy as np
from typing import List
from src.behavior.AbstractBehavior import AbstractBehavior


class SensorOffset(AbstractBehavior):

    def __init__(self, sensor_a_index=0, sensor_b_index=1, history=100):
        super().__init__(name="SensorOffset", history_size=history)
        self.population = 0
        self.a = sensor_a_index
        self.b = sensor_b_index

    def attach_world(self, world):
        self.population = world.population

    def calculate(self):
        a_theta = self.population[0].sensors[self.a].angle
        b_theta = self.population[0].sensors[self.b].angle
        sensor_angle = abs(a_theta - b_theta) / (2 * math.pi)
        self.set_value(sensor_angle)

