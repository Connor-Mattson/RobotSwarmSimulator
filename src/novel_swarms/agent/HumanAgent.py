from typing import Tuple
import pygame
import random
import math
import numpy as np
from copy import deepcopy
from .Agent import Agent
from .DiffDriveAgent import DifferentialDriveAgent
from ..config.AgentConfig import DiffDriveAgentConfig
from ..sensors.GenomeDependentSensor import GenomeBinarySensor
from ..util.collider.AABB import AABB


class HumanDrivenAgent(DifferentialDriveAgent):
    def __init__(self, config, control="keys-holonomic"):
        super().__init__(config)
        self.control = control
        self.body_color = (255, 0, 255)

    def step(self, check_for_world_boundaries=None, world=None, check_for_agent_collisions=None) -> None:
        if check_for_world_boundaries is not None:
            check_for_world_boundaries(self)
        self.handle_collisions(world)

    def handle_key_press(self, keys):
        if self.control == "keys-holonomic":
            STEP_SIZE = 2
            if keys[pygame.K_RIGHT]:
                self.set_x_pos(self.get_x_pos() + STEP_SIZE)
            if keys[pygame.K_LEFT]:
                self.set_x_pos(self.get_x_pos() - STEP_SIZE)
            if keys[pygame.K_DOWN]:
                self.set_y_pos(self.get_y_pos() + STEP_SIZE)
            if keys[pygame.K_UP]:
                self.set_y_pos(self.get_y_pos() - STEP_SIZE)

