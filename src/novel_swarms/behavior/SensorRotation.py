import math

import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior


class SensorRotation(AbstractBehavior):

    def __init__(self, sensor_index, history=100):
        super().__init__(name="Sensor_Rotation", history_size=history)
        self.population = None
        self.i = sensor_index

    def attach_world(self, world):
        self.population = world.population

    def attach_population(self, pop):
        self.population = pop

    def calculate(self):
        sensor_angle = self.population[0].controller[self.i] / (2 * math.pi)
        self.set_value(sensor_angle)

