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
                 ):

        if behavior is None:
            behavior = []

        self.behavior = behavior
        self.w = size[0]
        self.h = size[1]
        self.population_size = n_agents
        self.seed = seed
        self.padding = padding
        self.agentConfig = agentConfig
        self.radius = np.linalg.norm([self.w / 2, self.h / 2])

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
            padding=self.padding
        )
