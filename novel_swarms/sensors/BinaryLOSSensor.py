import pygame
import numpy as np
import math
from .AbstractSensor import AbstractSensor
from typing import List


class BinaryLOSSensor(AbstractSensor):
    def __init__(self, parent=None, angle=None, draw=True):
        super(BinaryLOSSensor, self).__init__(parent=parent, draw=draw)
        self.current_state = 0
        self.angle = angle

    def checkForLOSCollisions(self, world) -> None:
        sensor_position = self.parent.getPosition()

        # Equations taken from Dunn's 3D Math Primer for Graphics, section A.12
        p_0 = np.array(sensor_position)
        d = np.array(self.getLOSVector())
        d_hat = d / np.linalg.norm(d)

        # Check seen agent from last frame first, to avoid expensive computation
        if self.parent.agent_in_sight is not None:
            agent = self.parent.agent_in_sight
            if self.agent_in_sight(agent, p_0, d_hat):
                self.parent.agent_in_sight = agent
                self.current_state = 1
                return

        for agent in world.population:
            if self.agent_in_sight(agent, p_0, d_hat):
                self.parent.agent_in_sight = agent
                self.current_state = 1
                return

        self.parent.agent_in_sight = None
        self.current_state = 0

    def agent_in_sight(self, agent, p_0, d_hat):
        if agent == self.parent:
            return False

        c = np.array(agent.getPosition())
        e = c - p_0
        a = np.dot(e, d_hat)
        if a < 0:
            return False

        r_2 = agent.radius * agent.radius
        e_2 = np.dot(e, e)
        a_2 = a * a

        has_intersection = (r_2 - e_2 + a_2) >= 0
        if has_intersection:
            return True

        return False

    def step(self, world):
        super(BinaryLOSSensor, self).step(world=world)
        self.checkForLOSCollisions(world=world)

    def draw(self, screen):
        if not self.show:
            return
        super(BinaryLOSSensor, self).draw(screen)

        # Draw Sensory Vector (Vision Vector)
        sight_color = (255, 0, 0)
        if self.current_state == 1:
            sight_color = (0, 255, 0)

        magnitude = self.parent.radius * (20 if self.parent.is_highlighted else 1)
        magnitude *= 5 if self.angle is None else 3

        head = (self.parent.x_pos, self.parent.y_pos)

        if self.angle is None:
            tail = (self.parent.x_pos + (magnitude * math.cos(self.parent.angle)),
                    self.parent.y_pos + (magnitude * math.sin(self.parent.angle)))
        else:
            tail = (self.parent.x_pos + (magnitude * math.cos(self.angle + self.parent.angle)),
                    self.parent.y_pos + (magnitude * math.sin(self.angle + self.parent.angle)))

        pygame.draw.line(screen, sight_color, head, tail)

    def getLOSVector(self) -> List:
        head = self.parent.getPosition()
        tail = self.getFrontalPoint()
        return [tail[0] - head[0], tail[1] - head[1]]

    def getFrontalPoint(self):
        if self.angle is None:
            return self.parent.getFrontalPoint()
        return self.parent.x_pos + math.cos(self.angle + self.parent.angle), self.parent.y_pos + math.sin(self.angle + self.parent.angle)
