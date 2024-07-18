from ..config.AgentConfig import DiffDriveAgentConfig, UnicycleAgentConfig, MazeAgentConfig, StaticAgentConfig, \
    LevyAgentConfig, DroneAgentConfig, ModeSwitchingAgentConfig, MechanumAgentConfig
from .DiffDriveAgent import DifferentialDriveAgent
from .UnicycleAgent import UnicycleAgent
from .StaticAgent import StaticAgent
from .MazeAgent import MazeAgent
from .LevyAgent import LevyAgent
from .DroneAgent import DroneAgent
from .ModeSwitchingAgent import ModeSwitchingAgent
from .MechanumAgent import MechanumDriveAgent


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
        if isinstance(agent_config, DroneAgentConfig):
            return DroneAgent(config=agent_config, name=name)
        if isinstance(agent_config, ModeSwitchingAgentConfig):
            return ModeSwitchingAgent(config=agent_config, name=name)
        if isinstance(agent_config, MechanumAgentConfig):
            return MechanumDriveAgent(config=agent_config, name=name)
        raise Exception(f"Could not Create Agent of type: {agent_config.__class__.__name__}")
