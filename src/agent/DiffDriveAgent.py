from typing import List, Tuple
import pygame
import random
import math
from src.agent.Agent import Agent
from src.sensors.BinaryLOSSensor import BinaryLOSSensor

class DifferentialDriveAgent(Agent):
    def __init__(self, x=None, y=None, controller=None, name=None, angle=None, world_dim=[500, 500]) -> None:
        """
        Controller is a vector of length 4 that details the velocities of the wheels.
        """
        if controller is None:
            controller = []

        self.radius = 5
        self.wheel_radius = 1.0
        self.is_highlighted = False
        self.agent_in_sight = None
        self.dt = 1.8

        if x is None and y is None:
            x = random.randint(0 + self.radius, world_dim[0] - self.radius)
            y = random.randint(0 + self.radius, world_dim[1] - self.radius)

        super().__init__(x, y, name=name)

        if len(controller) == 4:
            self.vr_0 = controller[0]
            self.vl_0 = controller[1]
            self.vr_1 = controller[2]
            self.vl_1 = controller[3]
            # self.vl_2 = controller[4]
            # self.vr_2 = controller[5]
            # self.vr_3 = controller[6]
            # self.vl_3 = controller[7]
            # self.a_theta = controller[8]
            # self.b_theta = controller[9]
        else:
            raise Exception("This should not be thrown")
            self.vr_0 = -0.7
            self.vl_0 = 0.3
            self.vr_1 = 1
            self.vl_1 = 1
            self.s_theta = 0

        if angle is None:
            self.angle = random.random() * math.pi * 2
        else:
            self.angle = angle

        self.sensors = [
            BinaryLOSSensor(parent=self, angle=0),
            # BinaryLOSSensor(parent=self, angle=self.a_theta),
            # BinaryLOSSensor(parent=self, angle=self.b_theta)
        ]

    def step(self, check_for_world_boundaries=None, population=[], check_for_agent_collisions=None) -> None:
        super().step()
        vr, vl = self.interpretSensors()
        self.dx = (self.wheel_radius / 2) * (vl + vr) * math.cos(self.angle)
        self.dy = (self.wheel_radius / 2) * (vl + vr) * math.sin(self.angle)
        heading = (vr - vl) / (self.radius * 2)

        self.x_pos += self.dx * self.dt
        self.y_pos += self.dy * self.dt
        self.angle += heading * self.dt

        if check_for_world_boundaries is not None:
            check_for_world_boundaries(self)

        if check_for_agent_collisions is not None:
            check_for_agent_collisions(self)

        for sensor in self.sensors:
            sensor.step(population=population)

    def draw(self, screen) -> None:
        super().draw(screen)
        for sensor in self.sensors:
            sensor.draw(screen)

        # Draw Cell Membrane
        filled = 0 if self.is_highlighted else 1
        pygame.draw.circle(screen, (255, 255, 255), (self.x_pos, self.y_pos), self.radius, width=filled)

        # "Front" direction vector
        head = self.getFrontalPoint()
        tail = self.getPosition()
        vec = [head[0] - tail[0], head[1] - tail[1]]
        mag = self.radius * 2
        vec_with_magnitude = ((vec[0] * mag) + tail[0], (vec[1] * mag) + tail[1])
        pygame.draw.line(screen, (255, 255, 255), tail, vec_with_magnitude)

    def interpretSensors(self) -> Tuple:

        if self.sensors[0].on:
            vr = self.vr_1
            vl = self.vl_1
        else:
            vr = self.vr_0
            vl = self.vl_0

        # if self.sensors[0].on and self.sensors[1].on:
        #     vr = self.vr_3
        #     vl = self.vl_3
        # elif self.sensors[1].on:
        #     vr = self.vr_2
        #     vl = self.vl_2
        # elif self.sensors[0].on:
        #     vr = self.vr_1
        #     vl = self.vl_1
        # else:
        #     vr = self.vr_0
        #     vl = self.vl_0
        return vr, vl

    def __str__(self) -> str:
        return "(x: {}, y: {}, r: {}, θ: {})".format(self.x_pos, self.y_pos, self.radius, self.angle)
