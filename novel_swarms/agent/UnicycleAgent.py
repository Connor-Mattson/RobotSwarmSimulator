from typing import Tuple
import pygame
import random
import math
import time
import numpy as np
from copy import deepcopy
from .Agent import Agent
from ..config.AgentConfig import UnicycleAgentConfig
from ..sensors.GenomeDependentSensor import GenomeBinarySensor, GenomeFOVSensor
from ..util.collider.CircularCollider import CircularCollider
from ..util.timer import Timer
from ..util.collider.AABB import AABB
from ..util.collider.AngleSensitiveCC import AngleSensitiveCC


class UnicycleAgent(Agent):
    SEED = -1
    DEBUG = False

    def __init__(self, config: UnicycleAgentConfig = None, name=None) -> None:

        self.controller = config.controller

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
        self.wheel_radius = config.wheel_radius
        self.dt = config.dt
        self.is_highlighted = False
        self.agent_in_sight = None
        self.idiosyncrasies = config.idiosyncrasies
        I1_MEAN, I1_SD = 0.93, 0.08
        I2_MEAN, I2_SD = 0.95, 0.06
        self.i_1 = np.random.normal(I1_MEAN, I1_SD) if self.idiosyncrasies else 1.0
        self.i_2 = np.random.normal(I2_MEAN, I2_SD) if self.idiosyncrasies else 1.0
        self.stop_on_collision = config.stop_on_collision

        self.sensors = deepcopy(config.sensors)
        for sensor in self.sensors:
            if isinstance(sensor, GenomeBinarySensor) or isinstance(sensor, GenomeFOVSensor):
                sensor.augment_from_genome(config.controller)

        self.aabb = None
        self.collider = None
        self.body_filled = config.body_filled
        self.body_color = config.body_color

        self.attach_agent_to_sensors()

        # Set Trace Settings if a trace was assigned to this object.
        self.trace_color = config.trace_color
        self.trace = config.trace_length is not None
        if self.trace:
            self.trace_path = []
            self.trace_length = config.trace_length

    def seed(self, seed):
        random.seed(UnicycleAgent.SEED)

    def step(self, check_for_world_boundaries=None, world=None, check_for_agent_collisions=None) -> None:

        if world is None:
            raise Exception("Expected a Valid value for 'World' in step method call - Unicycle Agent")

        # timer = Timer("Calculations")
        super().step()
        self.aabb = None
        self.collider = None

        if world.goals and world.goals[0].agent_achieved_goal(self):
            v, omega = 0, 0
        else:
            v, omega = self.interpretSensors()

        # Define Idiosyncrasies that may occur in actuation/sensing
        idiosync_1 = self.i_1
        idiosync_2 = self.i_2

        self.dx = v * math.cos(self.angle) * idiosync_1
        self.dy = v * math.sin(self.angle) * idiosync_1
        dw = omega * idiosync_2

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
            check_for_world_boundaries(self)

        # if check_for_agent_collisions is not None:
        #     check_for_agent_collisions(self, forward_freeze=True)

        self.handle_collisions(world)

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
        for sensor in self.sensors:
            sensor.step(world=world)
        # timer = timer.check_watch()

        self.add_to_trace(self.x_pos, self.y_pos)

    def handle_collisions(self, world):
        collisions = True
        limit = 10
        while collisions and limit > 0:
            limit -= 1
            collisions = False
            self.build_collider()
            agent_set = world.getAgentsMatchingYRange(self.get_aabb())
            for agent in agent_set:
                if agent.name == self.name:
                    continue
                if self.aabb.intersects(agent.get_aabb()):
                    self.get_aabb().toggle_intersection()
                    correction = self.collider.collision_then_correction(agent.build_collider())
                    if correction is not None:
                        collisions = True
                        if np.linalg.norm(correction) == 0:
                            self.stopped_duration = 15
                        else:
                            self.x_pos += correction[0]
                            self.y_pos += correction[1]
                        break
            if collisions:
                self.collider.flag_collision()

    def build_collider(self):
        if self.stop_on_collision:
            self.collider = AngleSensitiveCC(self.x_pos, self.y_pos, self.radius, self.angle, self.get_action(), sensitivity=45)
        else:
            self.collider = CircularCollider(self.x_pos, self.y_pos, self.radius)
        return self.collider

    def draw(self, screen) -> None:
        super().draw(screen)
        for sensor in self.sensors:
            sensor.draw(screen)

        # Draw Cell Membrane
        filled = 0 if self.is_highlighted or self.body_filled else 1
        color = self.body_color if not self.stopped_duration else (255, 255, 51)
        pygame.draw.circle(screen, color, (self.x_pos, self.y_pos), self.radius, width=filled)

        # Draw Trace (if parameterized to do so)
        self.draw_trace(screen)

        # "Front" direction vector
        head = self.getFrontalPoint()
        tail = self.getPosition()
        vec = [head[0] - tail[0], head[1] - tail[1]]
        mag = self.radius * 2
        vec_with_magnitude = ((vec[0] * mag) + tail[0], (vec[1] * mag) + tail[1])
        pygame.draw.line(screen, (255, 255, 255), tail, vec_with_magnitude)

        if self.DEBUG:
            self.debug_draw(screen)

    def interpretSensors(self) -> Tuple:
        sensor_state = self.sensors.getState()
        v = self.controller[sensor_state * 2]
        omega = self.controller[(sensor_state * 2) + 1]
        return v, omega

    def debug_draw(self, screen):
        # self.aabb.draw(screen)
        self.collider.draw(screen)

    def get_action(self):
        return np.array([self.dx * self.dt, self.dy, self.dt])

    def get_aabb(self):
        """
        Return the Bounding Box of the agent
        """
        if not self.aabb:
            top_left = (self.x_pos - self.radius, self.y_pos - self.radius)
            bottom_right = (self.x_pos + self.radius, self.y_pos + self.radius)
            self.aabb = AABB(top_left, bottom_right)
        return self.aabb

    def draw_trace(self, screen):
        if not self.trace:
            return
        for x, y in self.trace_path:
            pygame.draw.circle(screen, self.trace_color, (x, y), 2)

    def add_to_trace(self, x, y):
        if not self.trace:
            return
        self.trace_path.append((x, y))
        if len(self.trace_path) > self.trace_length:
            self.trace_path.pop(0)

    def __str__(self) -> str:
        return "(x: {}, y: {}, r: {}, θ: {})".format(self.x_pos, self.y_pos, self.radius, self.angle)
