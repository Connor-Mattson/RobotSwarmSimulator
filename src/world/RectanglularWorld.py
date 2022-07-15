from src.world.World import World
from src.agent.Agent import Agent
from src.agent.DiffDriveAgent import DifferentialDriveAgent

class RectangularWorld(World):

    def __init__(self, w, h, pop_size = 20):
        super().__init__(w, h)
        self.population_size = pop_size
        pass

    def setup(self):
        self.population = [DifferentialDriveAgent() for _ in range(self.population_size)]
        pass

    def step(self):
        """
        Cycle through the entire population and take one step.
        """
        for agent in self.population:
            if not issubclass(type(agent), Agent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))
            agent.step(check_for_world_boundaries = self.withinWorldBoundaries)

    def draw(self, screen):
        """
        Cycle through the entire population and draw the agents.
        """
        for agent in self.population:
            if not issubclass(type(agent), Agent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))
            agent.draw(screen)

    def withinWorldBoundaries(self, agent: DifferentialDriveAgent):
        # Set agent position with respect to the world's boundaries and the bounding box of the agent
        agent.x_pos = max(agent.radius, min(self.bounded_width - agent.radius, agent.x_pos))
        agent.y_pos = max(agent.radius, min(self.bounded_height - agent.radius, agent.y_pos))