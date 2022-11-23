from .AbstractBehavior import AbstractBehavior
import math

class KNNBehavior(AbstractBehavior):
    def __init__(self, history=100, archiveMode=False):
        super().__init__(name = "3 Nearest Neighbors", history_size=history, archiveMode=archiveMode)
        self.population = None

    def attach_world(self, world):
        self.population = world.population
    
    def euclideanDistance(self, agent1, agent2):
        return math.sqrt((agent2.x_pos - agent1.x_pos) ** 2 + (agent2.y_pos - agent1.y_pos) ** 2)

    def agentCalculate(self, targetAgent):
        # k = 3
        nearestAgents = [998, 999, 1000] # Ordered from smallest to largest
        for agent in self.population:
            dist = self.euclideanDistance(agent, targetAgent)
            if dist < min(nearestAgents):
                nearestAgents = [dist] + nearestAgents[:2]
        return sum(nearestAgents) / (3 * 500)

    def calculate(self):
        result = 0
        for agent in self.population:
            result += self.agentCalculate(agent)
        result /= len(self.population)
        self.set_value(result)