from typing import List, Tuple
import pygame
import random
import math
from src.agent.Agent import Agent

class DifferentialDriveAgent(Agent):
    
    wheel_radius = 2.5
    sensor_on = False
    dt = 0.6
    
    # Circling
    vr_0 = 0.7
    vl_0 = -0.3
    vr_1 = 1
    vl_1 = 1

    # Aggregation
    # vr_0 = -0.7
    # vl_0 = -1.0
    # vr_1 = 1.0
    # vl_1 = -1.0

    def __init__(self, x = None, y = None, controller = [], name = None) -> None:
        """
        Controller is a vector of length 4 that details the velocities of the wheels.
        """
        if x == None and y == None:
            x = random.randint(30, 470)
            y = random.randint(30, 470)

        super().__init__(x, y, name=name)

        if len(controller) == 4:
            self.vr_0 = controller[0]
            self.vl_0 = controller[1]
            self.vr_1 = controller[2]
            self.vl_1 = controller[3]

        self.radius = 5
        self.angle = random.random() * math.pi

    def step(self, check_for_sensor = None, check_for_world_boundaries = None, check_for_agent_collisions = None) -> None:
        super().step()

        if check_for_sensor != None:
            self.sensor_on = check_for_sensor(self)

        if not self.sensor_on:
            vl = self.vl_0
            vr = self.vr_0
        else:
            vl = self.vl_1
            vr = self.vr_1

        dx = (self.wheel_radius / 2) * (vl + vr) * math.cos(self.angle)
        dy = (self.wheel_radius / 2) * (vl + vr) * math.sin(self.angle)
        heading = (vr - vl) / (self.radius * 2)

        self.x_pos += dx * self.dt
        self.y_pos += dy * self.dt
        self.angle += heading * self.dt

        if check_for_world_boundaries != None:
            check_for_world_boundaries(self)
        if check_for_agent_collisions != None:
            check_for_agent_collisions(self)

    def draw(self, screen) -> None:
        super().draw(screen)

        # Draw Cell Membrane
        pygame.draw.circle(screen, (255, 255, 255), (self.x_pos, self.y_pos), self.radius, width=1)
        
        # Draw Sensory Vector (Vision Vector)
        sight_color = (255, 0, 0)
        if(self.sensor_on):
            sight_color = (0, 255, 0)
        mangitude = self.radius * 4.2
        head = (self.x_pos, self.y_pos)
        tail = (self.x_pos + (mangitude * math.cos(self.angle)), self.y_pos + (mangitude * math.sin(self.angle)))
        pygame.draw.line(screen, sight_color, head, tail)

    def getFrontalPoint(self) -> Tuple:
        """
        Returns the location on the circumference that represents the "front" of the robot
        """
        return (self.x_pos + math.cos(self.angle), self.y_pos + math.sin(self.angle))

    def getLOSVector(self) -> List:
        head = (self.x_pos, self.y_pos)
        tail = self.getFrontalPoint()
        return [tail[0] - head[0], tail[1] - head[1]]
        
    def __str__(self) -> str:
        return "(x: {}, y: {}, r: {}, θ: {})".format(self.x_pos, self.y_pos, self.radius, self.angle)
