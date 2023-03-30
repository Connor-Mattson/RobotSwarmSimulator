from ..config.AgentConfig import DiffDriveAgentConfig, UnicycleAgentConfig, MazeAgentConfig, StaticAgentConfig, LevyAgentConfig
from .DiffDriveAgent import DifferentialDriveAgent
from .UnicycleAgent import UnicycleAgent
from .StaticAgent import StaticAgent
from .MazeAgent import MazeAgent
from .LevyAgent import LevyAgent


class AgentFactory:
    @staticmethod
    def create(agent_config, name=None):
        if isinstance(agent_config, DiffDriveAgentConfig):
            return DifferentialDriveAgent(config=agent_config)
        if isinstance(agent_config, UnicycleAgentConfig):
            return UnicycleAgent(config=agent_config, name=name)
        if isinstance(agent_config, MazeAgentConfig):
            return MazeAgent(config=agent_config, name=name)
        if isinstance(agent_config, StaticAgentConfig):
            return StaticAgent(config=agent_config, name=name)
        if isinstance(agent_config, LevyAgentConfig):
            return LevyAgent(config=agent_config, name=name)
        raise Exception("Could not Create Agent: Unknown Config Input")
