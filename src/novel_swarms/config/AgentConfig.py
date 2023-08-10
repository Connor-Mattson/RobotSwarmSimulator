import random

from pygame import math

from .WorldConfig import RectangularWorldConfig
from ..sensors.SensorSet import SensorSet
from ..sensors.SensorFactory import SensorFactory


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

    @staticmethod
    def from_dict(d):
        ret = DiffDriveAgentConfig()
        for k, v in d.items():
            if k != "type":
                setattr(ret, k, v)
        ret.sensors = SensorFactory.create(ret.sensors)
        return ret


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

    @staticmethod
    def from_dict(d):
        ret = DroneAgentConfig()
        for k, v in d.items():
            if k != "type":
                setattr(ret, k, v)
        ret.sensors = SensorFactory.create(ret.sensors)
        return ret


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
            "body_color": self.body_color,
            "body_filled": self.body_filled,
            "controller": self.controller,
            "sensors": self.sensors.as_config_dict(),
            "idiosyncrasies": self.idiosyncrasies,
            "stop_on_collision": self.stop_on_collision,
            "trace_length": self.trace_length,
            "trace_color": self.trace_color,
        }

    @staticmethod
    def from_dict(d):
        ret = UnicycleAgentConfig()
        for k, v in d.items():
            if k != "type":
                setattr(ret, k, v)
        ret.sensors = SensorFactory.create(ret.sensors)
        return ret


class LevyAgentConfig:
    def __init__(self, **kwargs):
        self.x = kwargs["config"].x
        self.y = kwargs["config"].y
        self.agent_radius = kwargs["config"].agent_radius
        self.unicycle_config = kwargs["config"]
        self.world = kwargs.get("world_config", None)
        self.levy_constant = kwargs.get("levy_constant", 1.0)
        self.forward_rate = kwargs["forward_rate"]
        self.turning_rate = kwargs["turning_rate"]
        self.step_scale = kwargs.get("step_scale", 1.0)

        self.seed = kwargs.get("seed", None)
        self.body_color = kwargs.get("body_color", (255, 255, 255))
        self.body_filled = kwargs.get("body_filled", True)
        self.stop_at_goal = kwargs.get("stop_at_goal", False)
        self.stop_on_goal_detect = kwargs.get("stop_on_goal_detect", False)
        self.curve_based = kwargs.get("curve_based", True)

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

    @staticmethod
    def from_dict(d):
        ret = LevyAgentConfig()
        for k, v in d.items():
            if k != "type":
                setattr(ret, k, v)
        return ret


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
                 body_filled=False,
                 catastrophic_collisions=False,
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
        self.controller = controller
        self.sensors = sensors
        self.idiosyncrasies = idiosyncrasies
        self.stop_on_collision = stop_on_collide
        self.stop_at_goal = stop_at_goal
        self.body_color = body_color
        self.body_filled = body_filled
        self.catastophic_collisions = catastrophic_collisions
        self.trace_length = trace_length
        self.trace_color = trace_color

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
            "catastophic_collisions" : self.catastophic_collisions
        }

    @staticmethod
    def from_dict(d):
        ret = MazeAgentConfig()
        for k, v in d.items():
            if k != "type":
                setattr(ret, k, v)
        ret.sensors = SensorFactory.create(ret.sensors)
        return ret


class ModeSwitchingAgentConfig():
    def __init__(self,
                 configs=None,
                 switch_mode="Keyboard"  # Elem in ["Keyboard", "Time", "Distribution"]
                 ):

        self.world = configs[0].world
        self.configs = configs
        self.switch_mode = switch_mode

    def attach_world_config(self, world_config):
        self.world = world_config
        for config in self.configs:
            config.attach_world_config(world_config)

    def as_dict(self):
        raise NotImplementedError

    @staticmethod
    def from_dict(d):
        parent_config = AgentConfigFactory.create(d["parent_config"])
        controllers = d["controllers"]
        switch_mode = d["switch_mode"]
        return ModeSwitchingAgentConfig(
            parent_config=parent_config,
            controllers=controllers,
            switch_mode=switch_mode
        )


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

    @staticmethod
    def from_dict(d):
        ret = StaticAgentConfig()
        for k, v in d.items():
            if k != "type":
                setattr(ret, k, v)
        return ret

class AgentConfigFactory:
    @staticmethod
    def create(d):
        if d["type"] == "StaticAgentConfig":
            return StaticAgentConfig.from_dict(d)
        elif d["type"] == "ModeSwitchingAgentConfig":
            return ModeSwitchingAgentConfig.from_dict(d)
        elif d["type"] == "MazeAgentConfig":
            return MazeAgentConfig.from_dict(d)
        elif d["type"] == "LevyAgentConfig":
            return LevyAgentConfig.from_dict(d)
        elif d["type"] == "UnicycleAgentConfig":
            return UnicycleAgentConfig.from_dict(d)
        elif d["type"] == "DroneAgentConfig":
            return DroneAgentConfig.from_dict(d)
        elif d["type"] == "DiffDriveAgentConfig":
            return DiffDriveAgentConfig.from_dict(d)
        elif d["type"] == "HeterogeneousSwarmConfig":
            from ..config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
            return HeterogeneousSwarmConfig.from_dict(d)
        else:
            raise Exception(f"Cannot instantiate a config of type: {d['type']}")

class AgentYAMLFactory:
    @staticmethod
    def from_yaml(file_name):
        import yaml
        config = None
        with open(file_name, "r") as stream:
            config = yaml.safe_load(stream)

        a_type = config["type"]
        if a_type == "Levy":
            return LevyAgentConfig(**config)
        else:
            raise Exception(f"Unknown Agent type: {config['type']}")


