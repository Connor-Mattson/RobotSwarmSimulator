import pygame
import numpy as np
import math
from .AbstractSensor import AbstractSensor
from typing import List


class BinaryFOVSensor(AbstractSensor):
    def __init__(self, parent=None, theta=10, distance=10, degrees=False, bias=0.0, false_positive=0.0, false_negative=0.0):
        super(BinaryFOVSensor, self).__init__(parent=parent)
        self.current_state = 0
        self.angle = 0
        self.theta = theta
        self.bias = bias
        self.fp = false_positive
        self.fn = false_negative
        if degrees:
            self.theta = np.deg2rad(self.theta)
            self.bias = np.deg2rad(self.bias)
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
            self.determineState(False, None)
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
                    self.determineState(True, agent)
                    return

                # It may also be the case that the center of the agent is not within the FOV, but that some part of the
                # circle is visible and on the edges of the left and right viewing vectors.
                # LinAlg Calculations obtained from https://www.bluebill.net/circle_ray_intersection.html

                # u, defined earlier is the vector from the point of interest to the center of the circle
                # Project u onto e_left and e_right
                u_l = np.dot(u, e_left) * e_left
                u_r = np.dot(u, e_right) * e_right

                # Determine the minimum distance between the agent's center (center of circle) and the projected vector
                dist_l = np.linalg.norm(u - u_l)
                dist_r = np.linalg.norm(u - u_r)

                radius = self.parent.radius    # Note: Assumes homogenous radius
                if dist_l < radius or dist_r < radius:
                    self.determineState(True, agent)
                    return

        self.determineState(False, None)
        return

    def determineState(self, real_value, agent):
        if real_value:
            # Consider Reporting False Negative
            if np.random.random_sample() < self.fn:
                self.parent.agent_in_sight = None
                self.current_state = 0
                return

            self.parent.agent_in_sight = agent
            self.current_state = 1
        else:
            # Consider Reporting False Positive
            if np.random.random_sample() < self.fp:
                self.parent.agent_in_sight = None
                self.current_state = 1
                return

            self.parent.agent_in_sight = None
            self.current_state = 0

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

        theta_l = self.theta + self.bias
        theta_r = -self.theta + self.bias

        rot_z_left = np.array([
            [np.cos(theta_l), -np.sin(theta_l), 0],
            [np.sin(theta_l), np.cos(theta_l), 0],
            [0, 0, 1]
        ])

        rot_z_right = np.array([
            [np.cos(theta_r), -np.sin(theta_r), 0],
            [np.sin(theta_r), np.cos(theta_r), 0],
            [0, 0, 1]
        ])

        v = np.append(self.getLOSVector(), [0])
        e_left = np.matmul(rot_z_left, v)
        e_right = np.matmul(rot_z_right, v)
        return e_left, e_right
