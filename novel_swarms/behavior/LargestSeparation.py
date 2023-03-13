from .AbstractBehavior import AbstractBehavior
import math

class LargestSeparationBehavior(AbstractBehavior):
    def __init__(self, history=100, archiveMode=False):
        super().__init__(name = "Largest Separation", history_size=history, archiveMode=archiveMode)
        self.population = None

    def attach_world(self, world):
        self.population = world.population
    
    def euclideanDistance(self, agent1, agent2):
        return math.sqrt((agent2.x_pos - agent1.x_pos) ** 2 + (agent2.y_pos - agent1.y_pos) ** 2)

    # Calculates the distance between the two points that are furthest away from each other
    def calculate(self):
        largestSeparation = 0
        for a in self.population:
            for b in self.population:
                dist = self.euclideanDistance(a, b)
                if dist > largestSeparation:
                    largestSeparation = dist
        largestSeparation /= 500
        self.set_value(largestSeparation)
