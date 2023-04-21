from typing import Tuple
import pygame
import random
import math
import time
import numpy as np
from copy import deepcopy

import scipy.special

from .Agent import Agent
from .UnicycleAgent import UnicycleAgent
from ..config.AgentConfig import UnicycleAgentConfig, LevyAgentConfig
from ..sensors.GenomeDependentSensor import GenomeBinarySensor, GenomeFOVSensor
from ..util.timer import Timer
from ..util.collider.AABB import AABB
from ..util.collider.AngleSensitiveCC import AngleSensitiveCC
from scipy.special import gamma

class LevyAgent(UnicycleAgent):
    def __init__(self, config: LevyAgentConfig = None, name=None) -> None:
        super().__init__(config.unicycle_config)

        if config.seed is not None:
            random.seed(config.seed)
            np.random.seed(config.seed)

        if config.levy_constant == "Random":
            self.levy_dist_index = random.random() + 1
        else:
            self.levy_dist_index = config.levy_constant

        self.sigma_u = self._sigma(self.levy_dist_index)
        self.sigma_v = 1

        self.turning_rate = config.turning_rate
        self.forward_rate = config.forward_rate

        self.omega = 0
        self.v = 1

        # Initialize the number of steps within the levy segment left to walk
        self.steps_left = 0
        self.step_scaling = config.step_scale

    def step(self, check_for_world_boundaries=None, world=None, check_for_agent_collisions=None) -> None:

        if world is None:
            raise Exception("Expected a Valid value for 'World' in step method call - Unicycle Agent")

        world.meta["levy_value"] = self.levy_dist_index

        self.aabb = None
        self.collider = None

        self.steps_left -= 1
        if self.steps_left <= 0:
            if self.v > 0:
                self.new_heading()
            else:
                self.new_foward_steps()

        v, omega = self.v, self.omega
        if world.goals and world.goals[0].agent_achieved_goal(self):
            self.steps_left = 1000
            if world.goals[0].remove_at:
                world.goals[0].add_achieved_agent(self.name)
                world.removeAgent(self)
                return

        self.dx = v * math.cos(self.angle)
        self.dy = v * math.sin(self.angle)
        dw = omega

        old_x_pos = self.x_pos
        old_y_pos = self.y_pos
        old_heading = self.angle

        if self.stopped_duration > 0:
            self.stopped_duration -= 1

        else:
            self.x_pos += self.dx * self.dt
            self.y_pos += self.dy * self.dt
            self.angle += dw * self.dt

        if check_for_world_boundaries is not None:
            collisions = check_for_world_boundaries(self)
            if collisions:
                self.steps_left = 0

        # if check_for_agent_collisions is not None:
        #     check_for_agent_collisions(self, forward_freeze=True)

        self.handle_collisions(world)
        if self.collider and self.collider.collision_flag:
            self.steps_left = 0

        if self.stopped_duration > 0:
            self.x_pos = old_x_pos
            self.y_pos = old_y_pos
            self.angle = old_heading

        # Calculate the 'real' dx, dy after collisions have been calculated.
        # This is what we use for velocity in our equations
        self.dx = self.x_pos - old_x_pos
        self.dy = self.y_pos - old_y_pos
        # timer = timer.check_watch()

        # timer = Timer("Sensors")
        # for sensor in self.sensors:
        #     sensor.step(world=world)
        # timer = timer.check_watch()

        self.add_to_trace(self.x_pos, self.y_pos)

    def new_heading(self):
        d_theta = (random.random() * 2 * np.pi) - np.pi
        self.steps_left = abs(d_theta // self.turning_rate) + 1
        if d_theta < 0:
            self.omega = -self.turning_rate
        else:
            self.omega = self.turning_rate
        self.v = 0

    def new_foward_steps(self):
        step = self.sample_step_size() * self.step_scaling
        self.steps_left = (step // self.forward_rate) + 1
        self.omega = 0
        self.v = self.forward_rate

    def sample_step_size(self):
        u = np.random.normal(0, np.power(self.sigma_u, 2))
        v = np.random.normal(0, np.power(self.sigma_v, 2))
        s = u / np.power(np.abs(v), 1 / self.levy_dist_index)
        return s

    def _sigma(self, beta):
        numer = (self._gamma(1 + beta) * np.sin(np.pi * (beta / 2)))
        denom = (self._gamma((1 + beta) / 2) * beta * np.power(2, ((beta - 1) / 2)))
        return np.power((numer / denom), 1 / beta)

    def _gamma(self, z):
        return gamma(z)

    def get_action(self):
        return np.array([self.dx * self.dt, self.dy, self.dt])
