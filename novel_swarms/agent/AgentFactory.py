from ..config.AgentConfig import DiffDriveAgentConfig, UnicycleAgentConfig
from .DiffDriveAgent import DifferentialDriveAgent
from .UnicycleAgent import UnicycleAgent


class AgentFactory:
    @staticmethod
    def create(agent_config, name=None):
        if isinstance(agent_config, DiffDriveAgentConfig):
            return DifferentialDriveAgent(config=agent_config)
        if isinstance(agent_config, UnicycleAgentConfig):
            return UnicycleAgent(config=agent_config, name=name)
        raise Exception("Could not Create Agent: Unknown Config Input")
