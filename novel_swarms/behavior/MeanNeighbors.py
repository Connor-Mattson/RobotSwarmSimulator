from .AbstractBehavior import AbstractBehavior
import math

class MeanNeighborDistance(AbstractBehavior):
    def __init__(self, history=100, archiveMode=False):
        super().__init__(name = "Mean Neighbor Distance", history_size=history, archiveMode=archiveMode)
        self.population = None

    def attach_world(self, world):
        self.population = world.population
    
    # Calculates the average distance between neighbors
    def calculate(self):
        result = 0
        for agent in self.population:
            result += self.agentMeanNeighborDistance(agent)
        
        result /= len(self.population)
        result /= 500
        self.set_value(result)
    
    def euclideanDistance(self, agent1, agent2):
        return math.sqrt((agent2.x_pos - agent1.x_pos) ** 2 + (agent2.y_pos - agent1.y_pos) ** 2)

    def agentMeanNeighborDistance(self, targetAgent):
        result = 0
        for agent in self.population:
            result += self.euclideanDistance(targetAgent, agent)
        return result / (len(self.population) - 1)
