import pygame
import math, random
import numpy as np
from multiprocessing import managers
from turtle import distance
from typing import List, Tuple
from src.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.behavior.ScatterBehavior import ScatterBehavior
from src.behavior.RadialVariance import RadialVarianceBehavior
from src.behavior.AngularMomentum import AngularMomentumBehavior
from src.behavior.AverageSpeed import AverageSpeedBehavior
from src.world.World import World
from src.agent.Agent import Agent
from src.agent.DiffDriveAgent import DifferentialDriveAgent

class RectangularWorld(World):

    def __init__(self, w, h, pop_size = 20):
        super().__init__(w, h)
        self.population_size = pop_size

    def setup(self):
        self.population = [DifferentialDriveAgent(angle=0, name=f"Bot_{i}") for i in range(self.population_size)]
        self.population = [
            DifferentialDriveAgent(angle=0, controller=[1, 1, 1, 1], x = 20, y = 100),
            # DifferentialDriveAgent(angle=180, controller=[1, 1, 1, 1], x = 200, y = 100)
        ]
        
        world_radius = np.linalg.norm([self.bounded_width/2, self.bounded_height/2])
        self.behavior = [
            AverageSpeedBehavior(population = self.population),
            AngularMomentumBehavior(population = self.population, r = world_radius),
            RadialVarianceBehavior(population = self.population, r= world_radius),
            ScatterBehavior(population = self.population, r = world_radius),
            GroupRotationBehavior(population = self.population)
        ]

    def step(self):
        """
        Cycle through the entire population and take one step. Calculate Behavior if needed.
        """
        for agent in self.population:
            if not issubclass(type(agent), DifferentialDriveAgent):
                raise Exception("Agents must be subtype of Agent, not {}".format(type(agent)))
            
            agent.step(
                check_for_world_boundaries = self.withinWorldBoundaries, 
                check_for_agent_collisions = self.preventAgentCollisions, 
                check_for_sensor = self.checkForSensor
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

        # Remove Highlights from everyone
        for n in self.population:
            n.is_highlighted = False

        if(len(neighborhood) == 0): 
            self.gui.set_selected(None)
            return

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
        # agent.angle += (math.pi / 720)

    def preventAgentCollisions(self, agent: DifferentialDriveAgent) -> None:
        """
        Using a set of neighbors that collide with the agent and the bounding box of those neighbors,
            push the agent to the edge of the box and continue checking for collisions until the agent is in a
            safe location OR we have expired the defined timeout.
        """

        agent_center = agent.getPosition()

        minimum_distance = agent.radius * 2
        target_distance = minimum_distance + (0.1)

        neighborhood = self.getNeighborsWithinDistance(agent_center, minimum_distance, excluded=agent)
        if(len(neighborhood) == 0):
            return

        colliding_agent = neighborhood[0]
        center_distance = self.distance(agent_center, colliding_agent.getPosition())
        distance_needed = target_distance - center_distance

        base = np.array([1, 0])
        a_to_b = agent_center - colliding_agent.getPosition()
        theta = np.arccos(np.dot(a_to_b, base) / np.linalg.norm(a_to_b) * np.linalg.norm(base))
        
        agent.x_pos += distance_needed * np.cos(theta)
        agent.y_pos += distance_needed * np.sin(theta)
        
        # agent.angle += (math.pi / 720)
        agent_center = (agent.x_pos, agent.y_pos)

    def checkForSensor(self, source_agent: DifferentialDriveAgent) -> bool:
        sensor_position = source_agent.getPosition()
        
        # Equations taken from Dunn's 3D Math Primer for Graphics, section A.12
        p_0 = np.array([sensor_position[0], sensor_position[1]])
        d = np.array(source_agent.getLOSVector())
        d_hat = d / np.linalg.norm(d)
        
        for agent in self.population:
            if agent == source_agent:
                continue

            c = np.array([agent.x_pos, agent.y_pos])
            e = c - p_0
            a = np.dot(e, d_hat)

            r_2 = agent.radius * agent.radius
            e_2 = np.dot(e, e)
            a_2 = a * a

            has_intersection = (r_2 - e_2 + a_2) >= 0
            if has_intersection and a >= 0:
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
