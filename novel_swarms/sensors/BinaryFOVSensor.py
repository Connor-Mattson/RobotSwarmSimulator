import pygame
import numpy as np
import math
from .AbstractSensor import AbstractSensor
from typing import List


class BinaryFOVSensor(AbstractSensor):
    def __init__(self, parent=None, theta=10, distance=10, degrees=False):
        super(BinaryFOVSensor, self).__init__(parent=parent)
        self.current_state = 0
        self.angle = 0
        self.theta = theta
        if degrees:
            self.theta = np.deg2rad(self.theta)
        self.r = distance

    def checkForLOSCollisions(self, population) -> None:
        # Mathematics obtained from Sundaram Ramaswamy
        # https://legends2k.github.io/2d-fov/design.html
        # See section 3.1.1.2
        sensor_origin = self.parent.getPosition()

        # First, bag all agents that lie within radius r of the parent
        bag = []
        for agent in population:
            if self.getDistance(sensor_origin, agent.getPosition()) < self.r:
                bag.append(agent)

        if not bag:
            self.parent.agent_in_sight = None
            self.current_state = 0
            return

        e_left, e_right = self.getSectorVectors()

        for agent in bag:
            u = agent.getPosition() - sensor_origin
            directional = np.dot(u, self.getLOSVector())
            if directional > 0:
                u = np.append(u, [0])
                cross_l = np.cross(e_left, u)
                cross_r = np.cross(u, e_right)
                sign_l = np.sign(cross_l)
                sign_r = np.sign(cross_r)
                added_signs = sign_l - sign_r
                sector_boundaries = np.all(added_signs == 0)
                if sector_boundaries:
                    self.parent.agent_in_sight = agent
                    self.current_state = 1
                    return

        self.parent.agent_in_sight = None
        self.current_state = 0
        return

    def step(self, population):
        super(BinaryFOVSensor, self).step(population=population)
        self.checkForLOSCollisions(population=population)

    def draw(self, screen):
        super(BinaryFOVSensor, self).draw(screen)

        # Draw Sensory Vector (Vision Vector)
        sight_color = (255, 0, 0)
        if self.current_state == 1:
            sight_color = (0, 255, 0)

        magnitude = self.r if self.parent.is_highlighted else self.parent.radius * 5

        head = (self.parent.x_pos, self.parent.y_pos)
        e_left, e_right = self.getSectorVectors()

        tail_l = (self.parent.x_pos + (magnitude * e_left[0]),
                  self.parent.y_pos + (magnitude * e_left[1]))

        tail_r = (self.parent.x_pos + (magnitude * e_right[0]),
                  self.parent.y_pos + (magnitude * e_right[1]))

        pygame.draw.line(screen, sight_color, head, tail_l)
        pygame.draw.line(screen, sight_color, head, tail_r)
        if self.parent.is_highlighted:
            pygame.draw.circle(screen, sight_color, self.parent.getPosition(), self.r, 3)

    def getDistance(self, a, b):
        return np.linalg.norm(b - a)

    def getLOSVector(self) -> List:
        head = self.parent.getPosition()
        tail = self.getFrontalPoint()
        return [tail[0] - head[0], tail[1] - head[1]]

    def getFrontalPoint(self):
        if self.angle is None:
            return self.parent.getFrontalPoint()
        return self.parent.x_pos + math.cos(self.angle + self.parent.angle), self.parent.y_pos + math.sin(
            self.angle + self.parent.angle)

    def getSectorVectors(self):
        rot_z_left = np.array([
            [np.cos(self.theta), -np.sin(self.theta), 0],
            [np.sin(self.theta), np.cos(self.theta), 0],
            [0, 0, 1]
        ])

        rot_z_right = np.array([
            [np.cos(-self.theta), -np.sin(-self.theta), 0],
            [np.sin(-self.theta), np.cos(-self.theta), 0],
            [0, 0, 1]
        ])

        v = np.append(self.getLOSVector(), [0])
        e_left = np.matmul(rot_z_left, v)
        e_right = np.matmul(rot_z_right, v)
        return e_left, e_right
