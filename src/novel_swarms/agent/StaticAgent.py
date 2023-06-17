from typing import Tuple
import pygame
import random
import math
import numpy as np
from copy import deepcopy
from .Agent import Agent
from ..config.AgentConfig import StaticAgentConfig
from ..sensors.GenomeDependentSensor import GenomeBinarySensor
from ..util.collider.AABB import AABB
from ..util.collider.CircularCollider import CircularCollider
from ..util.timer import Timer


class StaticAgent(Agent):
    SEED = -1
    DEBUG = True

    def __init__(self, config: StaticAgentConfig = None, name=None) -> None:

        if config.seed is not None:
            self.seed(config.seed)

        if config.x is None:
            self.x_pos = random.randint(round(0 + config.agent_radius), round(config.world.w - config.agent_radius))
        else:
            self.x_pos = config.x

        if config.y is None:
            self.y_pos = random.randint(round(0 + config.agent_radius), round(config.world.h - config.agent_radius))
        else:
            self.y_pos = config.y

        super().__init__(self.x_pos, self.y_pos, name=name)

        if config.angle is None:
            self.angle = random.random() * math.pi * 2
        else:
            self.angle = config.angle

        self.radius = config.agent_radius
        self.dt = config.dt
        self.is_highlighted = False
        self.agent_in_sight = None
        self.body_filled = config.body_filled
        self.body_color = config.body_color

    def seed(self, seed):
        random.seed(StaticAgent.SEED)

    def step(self, check_for_world_boundaries=None, world=None, check_for_agent_collisions=None) -> None:
        super().step()

    def draw(self, screen) -> None:
        super().draw(screen)
        filled = 0 if (self.is_highlighted or self.stopped_duration or self.body_filled) else 1
        color = self.body_color if not self.stopped_duration else (255,255,51)
        pygame.draw.circle(screen, color, (self.x_pos, self.y_pos), self.radius, width=filled)
        if self.DEBUG:
            self.debug_draw(screen)

    def build_collider(self):
        return CircularCollider(self.x_pos, self.y_pos, self.radius)

    def debug_draw(self, screen):
        self.get_aabb().draw(screen)

    def get_aabb(self):
        """
        Return the Bounding Box of the agent
        """
        top_left = (self.x_pos - self.radius, self.y_pos - self.radius)
        bottom_right = (self.x_pos + self.radius, self.y_pos + self.radius)
        return AABB(top_left, bottom_right)

    def __str__(self) -> str:
        return "(x: {}, y: {}, r: {}, θ: {})".format(self.x_pos, self.y_pos, self.radius, self.angle)
