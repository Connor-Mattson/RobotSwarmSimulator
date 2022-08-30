import math

import numpy as np
from typing import List
from src.behavior.AbstractBehavior import AbstractBehavior


class SensorRotation(AbstractBehavior):

    def __init__(self, population: List, sensor_index=0):
        super().__init__(name="SensorRotation")
        self.population = population
        self.i = sensor_index

    def calculate(self):
        sensor_angle = self.population[0].sensors[self.i].angle / (2 * math.pi)
        self.set_value(sensor_angle)

