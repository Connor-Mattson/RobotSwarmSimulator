import math
from numpy import array
from typing import Tuple


class Agent:

    def __init__(self, x, y, name=None, sensors=None, angle=0) -> None:
        self.x_pos = x
        self.y_pos = y
        self.name = name
        self.dy = 0
        self.dx = 0
        self.angle = angle
        self.sensors = sensors
        self.collision_flag = False
        self.stop_on_collision = False
        self.stopped_duration = 0
        self.detection_id = 0
        self.aabb = None
        pass

    def step(self, check_for_world_boundaries=None) -> None:
        pass

    def draw(self, screen) -> None:
        pass

    def getPosition(self):
        return array([self.x_pos, self.y_pos])

    def getVelocity(self):
        return array([self.dx, self.dy])

    def getFrontalPoint(self) -> Tuple:
        """
        Returns the location on the circumference that represents the "front" of the robot
        """
        return self.x_pos + math.cos(self.angle), self.y_pos + math.sin(self.angle)

    def attach_agent_to_sensors(self):
        for sensor in self.sensors:
            sensor.parent = self

    def get_aabb(self):
        pass

    def set_pos_vec(self, vec):
        """
        Set the x, y, and angle of the agent.

        @params
        vec: An iterable of len 3, where vec[0] is the x_position, vec[1] is the y_position, and vec[2] is the angle heading

        @return None
        """
        self.x_pos, self.y_pos, self.angle = vec[0], vec[1], vec[2]