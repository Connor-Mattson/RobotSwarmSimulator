from src.config.AgentConfig import *
from src.agent.DiffDriveAgent import DifferentialDriveAgent


class AgentFactory:
    @staticmethod
    def create(agent_config):
        if isinstance(agent_config, DiffDriveAgentConfig):
            return DifferentialDriveAgent(config=agent_config)

