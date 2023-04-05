import random

from pygame import math

from .WorldConfig import RectangularWorldConfig
from ..sensors.SensorSet import SensorSet


class DiffDriveAgentConfig:
    def __init__(self,
                 x=None,
                 y=None,
                 controller=None,
                 angle=None,
                 world_config: RectangularWorldConfig = None,
                 seed=None,
                 agent_radius=5,
                 wheel_radius=2.0,
                 dt=1.0,
                 sensors: SensorSet = None,
                 trace_length=None,
                 trace_color=None,
                 body_color=(255, 255, 255),
                 body_filled=False
                ):

        self.x = x
        self.y = y
        self.angle = angle
        self.world = world_config
        self.seed = seed
        self.dt = dt
        self.agent_radius = agent_radius
        self.wheel_radius = wheel_radius
        self.controller = controller
        self.sensors = sensors
        self.trace_length = trace_length
        self.trace_color = trace_color
        self.body_color = body_color
        self.body_filled = body_filled

    def attach_world_config(self, world_config):
        self.world = world_config

class UnicycleAgentConfig:
    def __init__(self,
                 x=None,
                 y=None,
                 controller=None,
                 angle=None,
                 world_config: RectangularWorldConfig = None,
                 seed=None,
                 agent_radius=5,
                 wheel_radius=2.0,
                 dt=1.0,
                 sensors: SensorSet = None,
                 idiosyncrasies=False,
                 stop_on_collide=False,
                 body_color=(255, 255, 255),
                 body_filled=False,
                 trace_length=None,
                 trace_color=None,
                 ):

        self.x = x
        self.y = y
        self.angle = angle
        self.world = world_config
        self.seed = seed
        self.dt = dt
        self.agent_radius = agent_radius
        self.wheel_radius = wheel_radius
        self.controller = controller
        self.sensors = sensors
        self.idiosyncrasies = idiosyncrasies
        self.stop_on_collision = stop_on_collide
        self.body_color = body_color
        self.body_filled = body_filled
        self.trace_length = trace_length
        self.trace_color = trace_color

    def attach_world_config(self, world_config):
        self.world = world_config

class LevyAgentConfig:
    def __init__(self,
                 config=None,
                 world_config: RectangularWorldConfig = None,
                 levy_constant='Random',
                 forward_rate=1.0,
                 turning_rate=1.0,
                 step_scale=1.0,
                 seed=None,
                 ):
        self.x = config.x
        self.y = config.y
        self.agent_radius = config.agent_radius
        self.unicycle_config = config
        self.world = world_config
        self.levy_constant = levy_constant
        self.forward_rate = forward_rate
        self.turning_rate = turning_rate
        self.step_scale = step_scale
        self.seed = seed

    def attach_world_config(self, world_config):
        self.world = world_config
        self.unicycle_config.attach_world_config(world_config)



class MazeAgentConfig:
    def __init__(self,
                 x=None,
                 y=None,
                 controller=None,
                 angle=None,
                 world_config: RectangularWorldConfig = None,
                 seed=None,
                 agent_radius=5,
                 dt=1.0,
                 sensors: SensorSet = None,
                 idiosyncrasies=False,
                 stop_on_collide=False,
                 body_color=(255, 255, 255),
                 body_filled=False
                 ):

        self.x = x
        self.y = y
        self.angle = angle
        self.world = world_config
        self.seed = seed
        self.dt = dt
        self.agent_radius = agent_radius
        self.controller = controller
        self.sensors = sensors
        self.idiosyncrasies = idiosyncrasies
        self.stop_on_collision = stop_on_collide
        self.body_color = body_color
        self.body_filled = body_filled

    def attach_world_config(self, world_config):
        self.world = world_config


class StaticAgentConfig:
    def __init__(self,
                 x=None,
                 y=None,
                 angle=None,
                 world_config: RectangularWorldConfig = None,
                 seed=None,
                 agent_radius=5,
                 dt=1.0,
                 body_color=(255, 255, 255),
                 body_filled=False
                 ):

        self.x = x
        self.y = y
        self.angle = angle
        self.world = world_config
        self.seed = seed
        self.dt = dt
        self.agent_radius = agent_radius
        self.body_color = body_color
        self.body_filled = body_filled

    def attach_world_config(self, world_config):
        self.world = world_config