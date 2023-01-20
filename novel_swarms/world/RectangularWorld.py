import math
import random
import numpy as np
from typing import List, Tuple
import pygame.draw
from ..agent.Agent import Agent
from ..agent.DiffDriveAgent import DifferentialDriveAgent
from ..config.WorldConfig import RectangularWorldConfig
from ..agent.AgentFactory import AgentFactory
from .World import World
from ..util.timer import Timer


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
        self.objects = config.objects
        self.goals = config.goals

        if config.seed is not None:
            # print(f"World Instantiated with Seed: {config.seed}")
            # print(f"TESTING RAND: {random.random()}")
            random.seed(config.seed)

        self.population = [
            AgentFactory.create(config.agentConfig, name=f"{i}") for i in range(self.population_size)
        ]

        ac = config.agentConfig
        if config.defined_start:
            for i in range(len(config.agent_init)):
                init = config.agent_init[i]
                noise_x = ((np.random.random() * 2) - 1) * 20
                noise_y = ((np.random.random() * 2) - 1) * 20
                noise_theta = ((np.random.random() * 2) - 1) * (np.pi / 8)
                self.population[i].x_pos = init[0] + noise_x
                self.population[i].y_pos = init[1] + noise_y
                if len(init) > 2:
                    self.population[i].angle = init[2] + noise_theta
            
        elif ac.x is None and config.seed is not None:
            for agent in self.population:
                agent.x_pos = random.randint(0 + ac.agent_radius, ac.world.w - ac.agent_radius)
                agent.y_pos = random.randint(0 + ac.agent_radius, ac.world.h - ac.agent_radius)
                agent.angle = random.random() * 2 * math.pi

        # print([(a.x_pos, a.y_pos, a.angle) for a in self.population])

        for i in range(len(self.objects)):
            self.objects[i].world = self

        self.behavior = config.behavior
        for b in self.behavior:
            b.attach_world(self)

    def step(self):
        """
        Cycle through the entire population and take one step. Calculate Behavior if needed.
        """
        agent_step_timer = Timer("Population Step")
        for agent in self.population:
            if not issubclass(type(agent), Agent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))

            agent.step(
                check_for_world_boundaries=self.withinWorldBoundaries,
                check_for_agent_collisions=self.preventAgentCollisions,
                world=self
            )
        # agent_step_timer.check_watch()

        behavior_timer = Timer("Behavior Calculation Step")
        for behavior in self.behavior:
            behavior.calculate()
        # behavior_timer.check_watch()


    def draw(self, screen):
        """
        Cycle through the entire population and draw the agents. Draw Environment Walls if needed.
        """
        if self.config.show_walls:
            p = self.config.padding
            w = self.config.w
            h = self.config.h
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect((p, p), (w - (2*p), h - (2*p))), 1)

        for world_obj in self.objects:
            world_obj.draw(screen)

        for world_goal in self.goals:
            world_goal.draw(screen)

        for agent in self.population:
            if not issubclass(type(agent), Agent):
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

        if self.gui is not None and len(neighborhood) == 0:
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
        agent_center = agent.getPosition()
        minimum_distance = agent.radius * 2
        target_distance = minimum_distance + 0.001

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
                    # colliding_agent.collision_flag = False
                    continue

                if agent.stop_on_collision:
                    agent.stopped_duration = 3

                agent.collision_flag = True
                colliding_agent.collision_flag = True

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
