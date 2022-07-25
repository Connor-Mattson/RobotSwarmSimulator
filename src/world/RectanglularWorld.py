import math, random
from multiprocessing import managers
from turtle import distance
from typing import List, Tuple
from src.world.World import World
from src.agent.Agent import Agent
from src.agent.DiffDriveAgent import DifferentialDriveAgent

class RectangularWorld(World):

    def __init__(self, w, h, pop_size = 20):
        super().__init__(w, h)
        self.population_size = pop_size

    def setup(self):
        self.population = [DifferentialDriveAgent(angle=0, name=f"Bot_{i}") for i in range(self.population_size)]
        # self.population = [
        #     DifferentialDriveAgent(x=10, y=10, angle=1.9),
        #     DifferentialDriveAgent(x=50, y=50, angle=1.9)
        # ]

    def step(self):
        """
        Cycle through the entire population and take one step.
        """
        for agent in self.population:
            if not issubclass(type(agent), DifferentialDriveAgent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))
            agent.step(
                check_for_world_boundaries = self.withinWorldBoundaries, 
                check_for_agent_collisions = self.preventAgentCollisions, 
                check_for_sensor = self.checkForSensor
            )

    def draw(self, screen):
        """
        Cycle through the entire population and draw the agents.
        """
        for agent in self.population:
            if not issubclass(type(agent), DifferentialDriveAgent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))
            agent.draw(screen)

    def getNeighborsWithinDistance(self, center: Tuple, r, excluded = None) -> List:
        """
        Given the center of a circle, find all Agents located within the circumference defined by center and r
        """
        filtered_agents = []
        for agent in self.population:
            if not issubclass(type(agent), Agent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))
            if self.distance(center, (agent.x_pos, agent.y_pos)) < r:
                if agent != excluded:
                    filtered_agents.append(agent)
        return filtered_agents

    def getNeighborhoodBoundingBox(self, agents: List) -> List:
        maxX = 0
        maxY = 0
        minX = self.bounded_width
        minY = self.bounded_height
        for agent in agents:
            if not issubclass(type(agent), Agent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))
            maxX = max(maxX, agent.x_pos)
            maxY = max(maxY, agent.y_pos)
            minX = min(minX, agent.x_pos)
            minY = min(minY, agent.y_pos)
        return (minX, minY), (maxX, maxY)
    
    def onClick(self, pos) -> None:
        neighborhood = self.getNeighborsWithinDistance(pos, self.population[0].radius)
        if(len(neighborhood) == 0): return

        # Remove Highlights from everyone
        for n in self.population:
            n.is_highlighted = False

        if self.gui != None:
            self.gui.set_selected(neighborhood[0])
            neighborhood[0].is_highlighted = True
    
    def withinWorldBoundaries(self, agent: DifferentialDriveAgent):
        """
        Set agent position with respect to the world's boundaries and the bounding box of the agent
        """
        padding = 10
        agent.x_pos = max(agent.radius + padding, min((self.bounded_width - agent.radius - padding), agent.x_pos))
        agent.y_pos = max(agent.radius + padding, min((self.bounded_height - agent.radius - padding), agent.y_pos))

    def preventAgentCollisions(self, agent: DifferentialDriveAgent) -> None:
        """
        Using a set of neighbors that collide with the agent and the bounding box of those neighbors,
            push the agent to the edge of the box and continue checking for collisions until the agent is in a
            safe location OR we have expired the defined timeout.
        """

        agent_center = agent.getPosition()
        timeout = 100
        while(timeout > 0):
            timeout -= 1
            minimum_distance = agent.radius * 2
            target_distance = minimum_distance + 0.1

            neighborhood = self.getNeighborsWithinDistance(agent_center, minimum_distance, excluded=agent)
            if(len(neighborhood) == 0):
                return

            colliding_agent = neighborhood[0]
            center_distance = self.distance(agent_center, colliding_agent.getPosition())
                        
            # Calculate the required offsets for the agent's x, y position in order to avoid a collision with the neighbor
            dy = colliding_agent.y_pos - agent_center[1]
            dx = colliding_agent.x_pos - agent_center[0]
            theta = 0
            if(dy != 0):
                theta = math.atan((dx) / (dy))

            if(theta < 0):
                offset_x = (target_distance * math.sin(theta)) - dx
                offset_y = (target_distance * math.cos(theta)) - dy
            else:
                offset_x = (target_distance * math.sin(theta)) + dx
                offset_y = (target_distance * math.cos(theta)) + dy
            
            # print("TESTING (Attempt {})[n: {}]".format(str(100 - timeout), len(neighborhood)))
            # print("=" * 20)
            # print("Preventing Collision between A (collidor) and B")
            # print("Distance: {}".format(center_distance))
            # print("Center: {}".format(agent_center))
            # print("=" * 20)
            # print("A: {}".format(str(agent)))
            # print("B: {}".format(str(colliding_agent)))
            # print("dx: {}".format(dx))
            # print("dy: {}".format(dy))
            # print("Angle from A to B: {}".format(theta))
            # print("Pushback with Vector: {}".format([offset_x, offset_y]))
            # print("=" * 20)
            # print("\n")
            
            agent.x_pos -= offset_x
            agent.y_pos -= offset_y
            agent_center = (agent.x_pos, agent.y_pos)

        raise Exception("Could not find a suitible position for agent. Consider increasing the search domain, decreasing the population count or increasing the size of the environment")

    def checkForSensor(self, source_agent: DifferentialDriveAgent) -> bool:
        sensor_position = source_agent.getPosition()
        a, b, c = self.generalEquationOfALine(sensor_position, source_agent.getFrontalPoint())
        for agent in self.population:
            if not issubclass(type(agent), Agent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))
            if agent == source_agent:
                continue
            distance_from_agent_to_line = ((a * agent.x_pos) + (b * agent.y_pos) + c) / (math.sqrt(a*a + b*b))
            
            # Vector A: The vector between the source and target agents
            vecA = [agent.x_pos - sensor_position[0], agent.y_pos - sensor_position[1]]

            # Vector B: The vector representing the sensor's line of sight
            vecB = source_agent.getLOSVector()

            # If the angle between the vectors is acute (positive dot product) 
            # and if the LOS crosses through the area of another bot, then the sensor is active
            dot = (vecA[0] * vecB[0]) + (vecA[1] * vecB[1])
            
            if distance_from_agent_to_line <= agent.radius / 2:
                if dot > 0:
                    source_agent.agent_in_sight = agent
                    return True

        source_agent.agent_in_sight = None
        return False

    def generalEquationOfALine(self, pointA: Tuple, pointB: Tuple) -> Tuple:
        x1, y1 = pointA
        x2, y2 = pointB

        a = y1 - y2
        b = x2 - x1
        c = (x1 - x2) * y1 + (y2 - y1) * x1
        return a, b, c

    def distance(self, pointA, pointB) -> float:
        return math.dist(pointA, pointB)
