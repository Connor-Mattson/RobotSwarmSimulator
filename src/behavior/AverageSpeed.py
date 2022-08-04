import numpy as np
from typing import List
from src.behavior.AbstractBehavior import AbstractBehavior

class AverageSpeedBehavior(AbstractBehavior):
    
    population = []
    
    def __init__(self, population: List):
        super().__init__(name = "Average Speed")
        self.population = population

    def calculate(self):
        n = len(self.population)
        velocities = [np.linalg.norm(agent.getVelocity()) for agent in self.population]
        average_speed = sum(velocities) / n
        self.set_value(average_speed)    

