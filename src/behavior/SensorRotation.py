import math

import numpy as np
from typing import List
from src.behavior.AbstractBehavior import AbstractBehavior


class SensorRotation(AbstractBehavior):

    def __init__(self, population: List):
        super().__init__(name="SensorRotation")
        self.population = population

    def calculate(self):
        sensor_angle = self.population[0].s_theta / (2 * math.pi)
        self.set_value(sensor_angle)

