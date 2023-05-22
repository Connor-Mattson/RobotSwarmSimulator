import warnings
import numpy as np


class RectangularWorldConfig:
    def __init__(self,
                 size=(500, 500),
                 n_agents=30,
                 seed=None,
                 behavior=None,
                 agentConfig=None,
                 padding=0,
                 collide_walls=True,
                 show_walls=True,
                 agent_initialization=None,
                 stop_at=None,
                 objects=[],
                 goals=[],
                 background_color=(0, 0, 0),
                 metadata=None,
                 ):

        if behavior is None:
            behavior = []

        self.defined_start = False
        if agent_initialization is not None:
            self.defined_start = True
            self.agent_init = agent_initialization
            if len(agent_initialization) != n_agents:
                raise Exception(
                    f"Length of Predefined Starting Locations ({len(agent_initialization)}) must equal number of agents ({n_agents})")

        self.behavior = behavior
        self.w = size[0]
        self.h = size[1]
        self.population_size = n_agents
        self.seed = seed
        self.padding = padding
        self.agentConfig = agentConfig
        self.radius = np.linalg.norm([self.w / 2, self.h / 2])
        self.show_walls = show_walls
        self.collide_walls = collide_walls
        self.stop_at = stop_at
        self.objects = objects
        self.goals = goals
        self.background_color = background_color
        self.metadata = metadata

        if self.agentConfig:
            self.agentConfig.attach_world_config(self.getShallowCopy())

    def addAgentConfig(self, agent_config):
        self.agentConfig = agent_config
        if self.agentConfig:
            self.agentConfig.attach_world_config(self.getShallowCopy())

    def getShallowCopy(self):
        return RectangularWorldConfig(
            size=(self.w, self.h),
            n_agents=self.population_size,
            seed=self.seed,
            padding=self.padding,
            goals=self.goals,
            objects=self.objects
        )

    def set_attributes(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def as_dict(self):
        return {
            "behavior": [b.as_config_dict() for b in self.behavior],
            "w": self.w,
            "h": self.h,
            "population_size": self.population_size,
            "seed": self.seed,
            "padding": self.padding,
            "agent_config": self.agentConfig.as_dict(),
            "show_walls": self.show_walls,
            "collide_walls": self.collide_walls,
            "stop_at": self.stop_at,
            "objects": [o.as_config_dict() for o in self.objects],
            "goals": [g.as_config_dict() for g in self.goals],
            "background_color": self.background_color,
            "metadata": self.metadata,
            "agent_init": self.agent_init if hasattr(self, "agent_init") else None
        }

    @staticmethod
    def from_dict(d):
        from src.novel_swarms.world.objects.ObjectFactory import ObjectFactory
        from src.novel_swarms.world.goals.GoalFactory import GoalFactory
        from src.novel_swarms.behavior.BehaviorFactory import BehaviorFactory
        from src.novel_swarms.config.AgentConfig import AgentConfigFactory

        objects = [ObjectFactory.create(o) for o in d["objects"]]
        goals = [GoalFactory.create(g) for g in d["goals"]]
        behavior = [BehaviorFactory.create(b) for b in d["behavior"]]
        a_config = AgentConfigFactory.create(d["agent_config"])

        return RectangularWorldConfig(
            size=(d["w"], d["h"]),
            behavior=behavior,
            n_agents=d["population_size"],
            seed=d["seed"],
            padding=d["padding"],
            agentConfig=a_config,
            show_walls=d["show_walls"],
            collide_walls=d["collide_walls"],
            stop_at=d["stop_at"],
            goals=goals,
            objects=objects,
            metadata=d["metadata"],
            agent_initialization=d["agent_init"]
        )

