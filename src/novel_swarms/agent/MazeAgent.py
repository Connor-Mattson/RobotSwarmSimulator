from typing import Tuple
import pygame
import random
import math
import numpy as np
from copy import deepcopy
from .Agent import Agent
from ..config.AgentConfig import MazeAgentConfig
from ..sensors.GenomeDependentSensor import GenomeBinarySensor
from ..util.collider.AABB import AABB
from ..util.timer import Timer


class MazeAgent(Agent):
    SEED = -1

    def __init__(self, config: MazeAgentConfig = None, name=None) -> None:

        self.controller = config.controller

        self.seed = config.seed
        if config.seed is not None:
            self.set_seed(config.seed)

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
        self.idiosyncrasies = config.idiosyncrasies
        I1_MEAN, I1_SD = 0.93, 0.08
        I2_MEAN, I2_SD = 0.95, 0.06
        self.i_1 = np.random.normal(I1_MEAN, I1_SD) if self.idiosyncrasies else 1.0
        self.i_2 = np.random.normal(I2_MEAN, I2_SD) if self.idiosyncrasies else 1.0
        self.stop_on_collision = config.stop_on_collision

        self.sensors = deepcopy(config.sensors)
        for sensor in self.sensors:
            if isinstance(sensor, GenomeBinarySensor):
                sensor.augment_from_genome(config.controller)

        self.attach_agent_to_sensors()

        self.body_filled = config.body_filled
        if config.body_color == "Random":
            self.body_color = self.get_random_color()
        else:
            self.body_color = config.body_color

    def set_seed(self, seed):
        random.seed(seed)

    def step(self, check_for_world_boundaries=None, world=None, check_for_agent_collisions=None) -> None:

        if world is None:
            raise Exception("Expected a Valid value for 'World' in step method call - Unicycle Agent")

        # timer = Timer("Calculations")
        super().step()

        if world.goals and world.goals[0].agent_achieved_goal(self) or self.detection_id == 2:
            v, omega = 0, 0
            self.detection_id = 2
            self.set_color_by_id(3)
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

        if self.stopped_duration > 0:
            self.stopped_duration -= 1

        else:
            self.x_pos += self.dx * self.dt
            self.y_pos += self.dy * self.dt

        self.angle += dw * self.dt

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
        filled = 0 if (self.is_highlighted or self.stopped_duration or self.body_filled) else 1
        color = self.body_color if not self.stopped_duration else (255,255,51)
        pygame.draw.circle(screen, color, (self.x_pos, self.y_pos), self.radius, width=filled)

        # "Front" direction vector
        head = self.getFrontalPoint()
        tail = self.getPosition()
        vec = [head[0] - tail[0], head[1] - tail[1]]
        mag = self.radius * 2
        vec_with_magnitude = ((vec[0] * mag) + tail[0], (vec[1] * mag) + tail[1])
        pygame.draw.line(screen, (255, 255, 255), tail, vec_with_magnitude)

    def interpretSensors(self) -> Tuple:
        sensor_state = self.sensors.getState()
        sensor_detection_id = self.sensors.getDetectionId()
        self.set_color_by_id(sensor_detection_id)

        if sensor_detection_id == 2:
            return 12, 0

        v = self.controller[sensor_state * 2]
        omega = self.controller[(sensor_state * 2) + 1]
        return v, omega

    def set_color_by_id(self, id):
        if id == 0:
            self.body_color = (255, 255, 255)
        elif id == 2:
            self.body_color = (255, 255, 0)
            self.body_filled = True
        elif id == 3:
            self.body_color = (15, 15, 255)
            self.body_filled = True

    def get_random_color(self):
        rand_color = [255, 255, 255]
        while sum(rand_color) > 245*3:
            rand_color = np.random.choice(256, 3)
        return rand_color

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
