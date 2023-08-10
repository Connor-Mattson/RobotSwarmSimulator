import math
from numpy import array
from typing import Tuple


class Agent:

    def __init__(self, x, y, name=None, sensors=None, angle=0, group=0) -> None:
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
        self.group = group
        pass

    def step(self, check_for_world_boundaries=None) -> None:
        pass

    def draw(self, screen) -> None:
        pass

    def get_sensors(self):
        return self.sensors

    def getPosition(self):
        return array([self.get_x_pos(), self.get_y_pos()])

    def getVelocity(self):
        return array([self.dx, self.dy])

    def getFrontalPoint(self) -> Tuple:
        """
        Returns the location on the circumference that represents the "front" of the robot
        """
        return self.get_x_pos() + math.cos(self.get_heading()), self.get_y_pos() + math.sin(self.get_heading())

    def attach_agent_to_sensors(self):
        for sensor in self.sensors:
            sensor.parent = self

    def get_aabb(self):
        pass

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos

    def set_x_pos(self, new_x):
        self.x_pos = new_x

    def set_y_pos(self, new_y):
        self.y_pos = new_y

    def get_heading(self):
        return self.angle

    def set_heading(self, new_heading):
        self.angle = new_heading

    def on_key_press(self, event):
        pass

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def set_pos_vec(self, vec):
        """
        Set the x, y, and angle of the agent.

        @params
        vec: An iterable of len 3, where vec[0] is the x_position, vec[1] is the y_position, and vec[2] is the angle heading

        @return None
        """
        self.set_x_pos(vec[0])
        self.set_y_pos(vec[1])
        self.set_heading(vec[2])
