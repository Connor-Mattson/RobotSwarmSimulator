from typing import Tuple
import pygame
import random
import math
from copy import deepcopy
from .Agent import Agent
from ..config.AgentConfig import DiffDriveAgentConfig
from ..sensors.GenomeDependentSensor import GenomeBinarySensor
from ..util.timer import Timer

class DifferentialDriveAgent(Agent):

    SEED = -1

    def __init__(self, config: DiffDriveAgentConfig = None) -> None:

        self.controller = config.controller

        if config.seed is not None:
            self.seed(config.seed)

        if config.x is None:
            self.x_pos = random.randint(0 + config.agent_radius, config.world.w - config.agent_radius)
        else:
            self.x_pos = config.x

        if config.y is None:
            self.y_pos = random.randint(0 + config.agent_radius, config.world.h - config.agent_radius)
        else:
            self.y_pos = config.y

        super().__init__(self.x_pos, self.y_pos, name="None")

        if config.angle is None:
            self.angle = random.random() * math.pi * 2
        else:
            self.angle = config.angle

        self.radius = config.agent_radius
        self.wheel_radius = config.wheel_radius
        self.dt = config.dt
        self.is_highlighted = False
        self.agent_in_sight = None

        self.sensors = deepcopy(config.sensors)
        for sensor in self.sensors:
            if isinstance(sensor, GenomeBinarySensor):
                sensor.augment_from_genome(config.controller)

        self.attach_agent_to_sensors()

    def seed(self, seed):
        random.seed(DifferentialDriveAgent.SEED)

    def step(self, check_for_world_boundaries=None, world=None, check_for_agent_collisions=None) -> None:

        if world is None:
            raise Exception("Expected a Valid value for 'World' in step method call")

        # timer = Timer("Calculations")
        super().step()
        if world.goals and world.goals[0].agent_achieved_goal(self):
            vl, vr = 0, 0
        else:
            vl, vr = self.interpretSensors()

        self.dx = (self.wheel_radius / 2) * (vl + vr) * math.cos(self.angle)
        self.dy = (self.wheel_radius / 2) * (vl + vr) * math.sin(self.angle)
        heading = (vl - vr) / (self.radius * 2)

        old_x_pos = self.x_pos
        old_y_pos = self.y_pos

        self.x_pos += self.dx * self.dt
        self.y_pos += self.dy * self.dt
        self.angle += heading * self.dt

        if check_for_world_boundaries is not None:
            check_for_world_boundaries(self)

        if check_for_agent_collisions is not None:
            check_for_agent_collisions(self)

        # Calculate the 'real' dx, dy after collisions have been calculated.
        # This is what we use for velocity in our equations
        self.dx = self.x_pos - old_x_pos
        self.dy = self.y_pos - old_y_pos
        # timer = timer.check_watch()

        # timer = Timer("Sensors")
        for sensor in self.sensors:
            sensor.step(world=world)
        # timer = timer.check_watch()

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
        sensor_state = self.sensors.getState()
        vl = self.controller[sensor_state * 2]
        vr = self.controller[(sensor_state * 2) + 1]
        return vl, vr

    def __str__(self) -> str:
        return "(x: {}, y: {}, r: {}, θ: {})".format(self.x_pos, self.y_pos, self.radius, self.angle)
