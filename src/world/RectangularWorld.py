import math
import random
from typing import List, Tuple

import numpy as np
from src.agent.Agent import Agent
from src.agent.DiffDriveAgent import DifferentialDriveAgent
from src.world.World import World
from src.config.WorldConfig import RectangularWorldConfig
from src.agent.AgentFactory import AgentFactory


def distance(pointA, pointB) -> float:
    return math.dist(pointA, pointB)


class RectangularWorld(World):
    def __init__(self, config: RectangularWorldConfig = None):
        if config is None:
            raise Exception("RectangularWorld must be instantiated with a WorldConfig class")

        super().__init__(config.w, config.h)
        self.config = config
        self.population_size = config.population_size
        self.behavior = config.behavior
        self.padding = config.padding
        self.population = [
            AgentFactory.create(config.agentConfig) for i in range(self.population_size)
        ]
        self.behavior = config.behavior
        for b in self.behavior:
            b.attach_world(self)

        print("Hello World")

    def step(self):
        """
        Cycle through the entire population and take one step. Calculate Behavior if needed.
        """
        for agent in self.population:
            if not issubclass(type(agent), DifferentialDriveAgent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))

            agent.step(
                check_for_world_boundaries=self.withinWorldBoundaries,
                check_for_agent_collisions=self.preventAgentCollisions,
                population=self.population
            )

        for behavior in self.behavior:
            behavior.calculate()

    def draw(self, screen):
        """
        Cycle through the entire population and draw the agents.
        """
        for agent in self.population:
            if not issubclass(type(agent), DifferentialDriveAgent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))
            agent.draw(screen)

    def getNeighborsWithinDistance(self, center: Tuple, r, excluded=None) -> List:
        """
        Given the center of a circle, find all Agents located within the circumference defined by center and r
        """
        filtered_agents = []
        for agent in self.population:
            if not issubclass(type(agent), Agent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))
            if distance(center, (agent.x_pos, agent.y_pos)) < r:
                if agent != excluded:
                    filtered_agents.append(agent)
        return filtered_agents

    def onClick(self, pos) -> None:
        neighborhood = self.getNeighborsWithinDistance(pos, self.population[0].radius)

        # Remove Highlights from all agents
        for n in self.population:
            n.is_highlighted = False

        if len(neighborhood) == 0:
            self.gui.set_selected(None)
            return

        if self.gui is not None:
            self.gui.set_selected(neighborhood[0])
            neighborhood[0].is_highlighted = True

    def withinWorldBoundaries(self, agent: DifferentialDriveAgent):
        """
        Set agent position with respect to the world's boundaries and the bounding box of the agent
        """
        padding = self.padding

        # Prevent Left Collisions
        agent.x_pos = max(agent.radius + padding, agent.x_pos)

        # Prevent Right Collisions
        agent.x_pos = min((self.bounded_width - agent.radius - padding), agent.x_pos)

        # Prevent Top Collisions
        agent.y_pos = max(agent.radius + padding, agent.y_pos)

        # Prevent Bottom Collisions
        agent.y_pos = min((self.bounded_height - agent.radius - padding), agent.y_pos)

        # agent.angle += (math.pi / 720)

    def preventAgentCollisions(self, agent: DifferentialDriveAgent) -> None:
        """
        Using a set of neighbors that collide with the agent and the bounding box of those neighbors,
            push the agent to the edge of the box and continue checking for collisions until the agent is in a
            safe location OR we have expired the defined timeout.
        """

        agent_center = agent.getPosition()
        minimum_distance = agent.radius * 2
        target_distance = minimum_distance + 0.1

        neighborhood = self.getNeighborsWithinDistance(agent_center, minimum_distance, excluded=agent)
        if len(neighborhood) == 0:
            return

        remaining_attempts = 10
        while len(neighborhood) > 0 and remaining_attempts > 0:

            # Check ALL Bagged agents for collisions
            for i in range(len(neighborhood)):

                colliding_agent = neighborhood[i]
                center_distance = distance(agent_center, colliding_agent.getPosition())

                if center_distance > minimum_distance:
                    continue

                # print(f"Overlap. A: {agent_center}, B: {colliding_agent.getPosition()}")
                distance_needed = target_distance - center_distance
                a_to_b = agent_center - colliding_agent.getPosition()

                # If distance super close to 0, we have a problem. Add noise.
                SIGNIFICANCE = 0.0001
                if a_to_b[0] < SIGNIFICANCE and a_to_b[1] < SIGNIFICANCE:
                    MAGNITUDE = 0.001
                    direction = 1
                    if random.random() > 0.5:
                        direction = -1
                    agent.x_pos += random.random() * direction * MAGNITUDE

                    direction = 1
                    if random.random() > 0.5:
                        direction = -1
                    agent.y_pos += random.random() * direction * MAGNITUDE

                    agent_center = agent.getPosition()
                    center_distance = distance(agent_center, colliding_agent.getPosition())
                    distance_needed = target_distance - center_distance
                    a_to_b = agent_center - colliding_agent.getPosition()

                pushback = (a_to_b / np.linalg.norm(a_to_b)) * distance_needed

                # print(base, a_to_b, theta)

                delta_x = pushback[0]
                delta_y = pushback[1]

                if math.isnan(delta_x) or math.isnan(delta_y):
                    break

                # print(delta_x, delta_y)

                agent.x_pos += delta_x
                agent.y_pos += delta_y

                # agent.angle += (math.pi / 720)
                agent_center = agent.getPosition()

            neighborhood = self.getNeighborsWithinDistance(agent_center, minimum_distance, excluded=agent)
            remaining_attempts -= 1

    def getBehaviorVector(self):
        behavior = np.array([s.out_average()[1] for s in self.behavior])
        return behavior
