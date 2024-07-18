from typing import Tuple
import pygame
import random
import math
import pymunk
import numpy as np
from copy import deepcopy
from .Agent import Agent
from ..config.AgentConfig import MechanumAgentConfig
from ..sensors.GenomeDependentSensor import GenomeBinarySensor
from ..util.collider.AABB import AABB
from ..util.collider.CircularCollider import CircularCollider

class MechanumDriveAgent(Agent):
    """
    TODO: Documentation
    """

    SEED = -1
    DEBUG = False

    def __init__(self, config: MechanumAgentConfig = None, name=None) -> None:

        self.controller = config.controller

        if config.seed is not None:
            self.seed(config.seed)

        if config.x is None:
            self.set_x_pos(random.randint(0, config.world.w))
        else:
            self.set_x_pos(config.x)

        if config.y is None:
            self.set_y_pos(random.randint(0, config.world.h))
        else:
            self.set_y_pos(config.y)

        super().__init__(self.x_pos, self.y_pos, name=name)

        if config.angle is None:
            self.angle = random.random() * math.pi * 2
        else:
            self.angle = config.angle

        ### Unique parameters
        self.lx = config.lx
        self.ly = config.ly
        self.wheel_radius = config.wheel_radius
        self.dt = config.dt
        self.agent_in_sight = None
        self.radius = max(self.ly, self.lx)

        self.body_filled = False
        self.is_highlighted = False
        # Set Trace Settings if a trace was assigned to this object.
        self.trace = config.trace_length is not None
        if self.trace:
            self.trace_path = []
            self.trace_length = config.trace_length

        if config.body_color == "Random":
            self.body_color = self.get_random_color()
        else:
            self.body_color = config.body_color

        if not config.trace_color:
            self.trace_color = self.body_color
        else:
            self.trace_color = config.trace_color

        self.aabb = None
        self.sensors = deepcopy(config.sensors)
        for sensor in self.sensors:
            if isinstance(sensor, GenomeBinarySensor):
                sensor.augment_from_genome(config.controller)

        self.attach_agent_to_sensors()

    def seed(self, seed):
        # random.seed(DifferentialDriveAgent.SEED)
        pass

    def step(self, check_for_world_boundaries=None, world=None, check_for_agent_collisions=None) -> None:

        if world is None:
            raise Exception("Expected a Valid value for 'World' in step method call")

        # timer = Timer("Calculations")
        super().step()
        self.aabb = None

        if world.goals and world.goals[0].agent_achieved_goal(self):
            vx, vy, dtheta = 0, 0, 0
        else:
            vx, vy, dtheta = self.interpretSensors()

        # Calculate Heading
        v = np.sqrt(vx ** 2 + vy ** 2)
        heading = math.atan2(vy, vx)

        self.dx = v * math.cos(self.angle + heading)
        self.dy = v * math.sin(self.angle + heading)

        old_x_pos = self.get_x_pos()
        old_y_pos = self.get_y_pos()

        self.x_pos += self.dx * self.dt
        self.y_pos += self.dy * self.dt
        self.angle += dtheta * self.dt

        if check_for_world_boundaries is not None:
            check_for_world_boundaries(self)

        self.handle_collisions(world)

        # Calculate the 'real' dx, dy after collisions have been calculated.
        # This is what we use for velocity in our equations
        self.dx = self.x_pos - old_x_pos
        self.dy = self.y_pos - old_y_pos
        # timer = timer.check_watch()

        self.add_to_trace(self.get_x_pos(), self.get_y_pos())

        # timer = Timer("Sensors")
        for sensor in self.sensors:
            sensor.step(world=world)
        # timer = timer.check_watch()

    @staticmethod
    def rotate_tuple(t, theta, x=0, y=0):
        c = np.cos(theta)
        s = np.sin(theta)
        rot = c * t[0] + s * t[1], -s * t[0] + c * t[1]
        return rot[0] + x, rot[1] + y

    def draw(self, screen) -> None:
        super().draw(screen)
        for sensor in self.sensors:
            sensor.draw(screen)

        # Draw Cell Membrane
        filled = 0 if self.is_highlighted or self.body_filled else 1
        x, y = self.get_x_pos(), self.get_y_pos()
        lx, ly = self.lx, self.ly

        top_left_0 = (-lx, -ly)
        bot_left_0 = (-lx, ly)
        bot_right_0 = (lx, ly)
        top_right_0 = (lx, -ly)

        # Essentially, an expanded rotation matrix multiplication and translation back to (x, y)
        tl = self.rotate_tuple(top_left_0, -self.angle, x, y)
        bl = self.rotate_tuple(bot_left_0, -self.angle, x, y)
        br = self.rotate_tuple(bot_right_0, -self.angle, x, y)
        tr = self.rotate_tuple(top_right_0, -self.angle, x, y)

        pygame.draw.polygon(screen, self.body_color, [tl, bl, br, tr], width=filled)

        # Draw Wheels
        xdist = 0.9 * self.lx
        ydist = (0.8 * self.ly)
        offx = (0.2 * self.lx)
        offy = self.wheel_radius / 2
        for deltax, deltay in [(xdist, ydist), (-xdist, ydist), (-xdist, -ydist), (xdist, -ydist)]:
            poly = []
            for offx, offy in [(offx, offy), (offx, -offy), (-offx, -offy), (-offx, offy)]:
                p = (offy + deltay, offx + deltax)  # Note, Intentionally Flopped
                poly.append(self.rotate_tuple(p, -self.angle, x, y))
            pygame.draw.polygon(screen, self.body_color, poly, width=filled)
            # pygame.draw.circle(screen, self.body_color, center=(deltax + x, deltay + y), radius=3, width=filled)

        # Draw Trace (if parameterized to do so)
        self.draw_trace(screen)

        # "Front" direction vector
        head = self.getFrontalPoint()
        tail = self.getPosition()
        vec = [head[0] - tail[0], head[1] - tail[1]]
        mag = self.lx * 2
        vec_with_magnitude = ((vec[0] * mag) + tail[0], (vec[1] * mag) + tail[1])
        pygame.draw.line(screen, self.body_color, tail, vec_with_magnitude)

        if self.DEBUG:
            self.debug_draw(screen)

    def interpretSensors(self) -> Tuple:
        sensor_state = self.sensors.getState()
        forward_v = self.controller[sensor_state * 3]
        strafe_v = self.controller[(sensor_state * 3) + 1]
        turning_rate = self.controller[(sensor_state * 3) + 2]
        return forward_v, strafe_v, turning_rate

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

    def get_random_color(self):
        rand_color = [255, 255, 255]
        while sum(rand_color) > 245*3:
            rand_color = np.random.choice(256, 3)
        return rand_color

    def debug_draw(self, screen):
        self.get_aabb().draw(screen)

    def handle_collisions(self, world):
        collisions = True
        attempts = 0
        while collisions and attempts < 10:
            collisions = False
            attempts += 1
            collider = self.build_collider()
            agent_set = world.getAgentsMatchingYRange(self.get_aabb())
            for agent in agent_set:
                if agent.name == self.name:
                    continue
                if self.aabb.intersects(agent.get_aabb()):
                    self.get_aabb().toggle_intersection()
                    correction = collider.collision_then_correction(agent.build_collider())
                    if correction is not None:
                        self.x_pos += correction[0]
                        self.y_pos += correction[1]
                        collisions = True
                        break

    def build_collider(self):
        return CircularCollider(self.x_pos, self.y_pos, self.lx)

    def simulate_error(self, err_type="Death"):
        if err_type == "Death":
            self.controller = [0 for _ in self.controller]
            self.body_color = (255, 0, 0)
            self.body_filled = True
        elif err_type == "Divergence":
            self.controller = [1, 1, 1, 1]
            self.body_color = (255, 0, 0)
            self.body_filled = True

    def get_aabb(self):
        """
        Return the Bounding Box of the agent
        """
        if not self.aabb:
            top_left = (self.x_pos - self.lx, self.y_pos - self.lx)
            bottom_right = (self.x_pos + self.lx, self.y_pos + self.lx)
            self.aabb = AABB(top_left, bottom_right)
        return self.aabb

    def __str__(self) -> str:
        return "(x: {}, y: {}, r: {}, θ: {})".format(self.x_pos, self.y_pos, self.lx, self.angle)
