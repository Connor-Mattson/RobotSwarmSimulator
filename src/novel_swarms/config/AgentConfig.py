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

    def as_dict(self):
        return {
            "type": "DiffDriveAgentConfig",
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "seed": self.seed,
            "dt": self.dt,
            "agent_radius": self.agent_radius,
            "wheel_radius": self.wheel_radius,
            "body_color": self.body_color,
            "body_filled": self.body_filled,
            "controller": self.controller,
            "sensors": self.sensors.as_config_dict(),
            "trace_length": self.trace_length,
            "trace_color": self.trace_color,
        }


class DroneAgentConfig:
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
        self.controller = controller
        self.sensors = sensors
        self.trace_length = trace_length
        self.trace_color = trace_color
        self.body_color = body_color
        self.body_filled = body_filled

    def attach_world_config(self, world_config):
        self.world = world_config

    def as_dict(self):
        return {
            "type": "DroneAgentConfig",
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "seed": self.seed,
            "dt": self.dt,
            "agent_radius": self.agent_radius,
            "body_color": self.body_color,
            "body_filled": self.body_filled,
            "controller": self.controller,
            "sensors": self.sensors.as_config_dict(),
            "trace_length": self.trace_length,
            "trace_color": self.trace_color,
        }


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

    def as_dict(self):
        return {
            "type": "UnicycleAgentConfig",
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "seed": self.seed,
            "dt": self.dt,
            "agent_radius": self.agent_radius,
            "wheel_radius": self.wheel_radius,
            "body_color": self.body_color,
            "body_filled": self.body_filled,
            "controller": self.controller,
            "sensors": self.sensors.as_config_dict(),
            "idiosyncrasies": self.idiosyncrasies,
            "stop_on_collision": self.stop_on_collision,
            "trace_length": self.trace_length,
            "trace_color": self.trace_color,
        }


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

    def as_dict(self):
        return {
            "type": "LevyAgentConfig",
            "x": self.x,
            "y": self.y,
            "seed": self.seed,
            "agent_radius": self.agent_radius,
            "unicycle_config": self.unicycle_config.as_dict(),
            "levy_constant": self.levy_constant,
            "forward_rate": self.forward_rate,
            "turning_rate": self.turning_rate,
            "step_scale": self.step_scale,
        }


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
                 stop_at_goal=True,
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
        self.stop_at_goal = stop_at_goal
        self.body_color = body_color
        self.body_filled = body_filled

    def attach_world_config(self, world_config):
        self.world = world_config

    def as_dict(self):
        return {
            "type": "MazeAgentConfig",
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "seed": self.seed,
            "dt": self.dt,
            "agent_radius": self.agent_radius,
            "body_color": self.body_color,
            "body_filled": self.body_filled,
            "controller": self.controller,
            "sensors": self.sensors.as_config_dict(),
            "idiosyncrasies": self.idiosyncrasies,
            "stop_on_collision": self.stop_on_collision,
            "stop_at_goal": self.stop_at_goal,
        }


class ModeSwitchingAgentConfig():
    def __init__(self,
                 parent_config: MazeAgentConfig,
                 controllers,
                 switch_mode="Keyboard"  # Elem in ["Keyboard", "Time", "Distribution"]
                 ):
        self.copy_config(parent_config)
        self.world = parent_config.world
        self.parent_config = parent_config
        self.controllers = controllers
        self.switch_mode = switch_mode

    def copy_config(self, config):
        self.x = config.x
        self.y = config.y
        self.angle = config.angle
        self.world = config.world
        self.seed = config.seed
        self.dt = config.dt
        self.agent_radius = config.agent_radius
        self.controller = config.controller
        self.sensors = config.sensors
        self.idiosyncrasies = config.idiosyncrasies
        self.stop_on_collision = config.stop_on_collision
        self.stop_at_goal = config.stop_at_goal
        self.body_color = config.body_color
        self.body_filled = config.body_filled

    def attach_world_config(self, world_config):
        self.world = world_config
        self.parent_config.attach_world_config(world_config)

    def as_dict(self):
        return {
            "type": "ModeSwitchingAgentConfig",
            "parent_config": self.parent_config.as_dict(),
            "controllers": self.controllers,
            "switch_mode": self.switch_mode
        }


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

    def as_dict(self):
        return {
            "type": "StaticAgentConfig",
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "seed": self.seed,
            "dt": self.dt,
            "agent_radius": self.agent_radius,
            "body_color": self.body_color,
            "body_filled": self.body_filled
        }
