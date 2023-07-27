import warnings
import numpy as np
from src.novel_swarms.world.initialization.AbstractInit import AbstractInitialization
from src.novel_swarms.world.initialization.RandomInit import RectRandomInitialization

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
                 init_type: AbstractInitialization = None,
                 stop_at=None,
                 objects=[],
                 goals=[],
                 background_color=(0, 0, 0),
                 metadata=None,
                 ):

        if behavior is None:
            behavior = []

        self.defined_start = False

        # TODO: Deprecate Agent Initialization
        if agent_initialization is not None:
            warnings.warn("The agent_initialization parameter (WorldConfig Class) will be deprecated in an upcoming version. Use Initialization Typing Instead (param init_type).")
            self.defined_start = True
            self.agent_init = agent_initialization
            if len(agent_initialization) != n_agents:
                raise Exception(f"Length of Predefined Starting Locations ({len(agent_initialization)}) must equal number of agents ({n_agents})")
        
        elif init_type is None:
            init_type = RectRandomInitialization(n_agents, ((0, 0), size))
        
        self.init_type = init_type
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
