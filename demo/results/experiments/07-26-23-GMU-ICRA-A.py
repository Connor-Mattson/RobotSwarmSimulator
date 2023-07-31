from src.novel_swarms.world.simulate import main as sim
from src.novel_swarms.config.AgentConfig import LevyAgentConfig, MazeAgentConfig, UnicycleAgentConfig
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.agent.LevyAgent import LevyAgent
from src.novel_swarms.agent.UnicycleAgent import UnicycleAgent
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.world.initialization.RandomInit import RectRandomInitialization

if __name__ == "__main__":

    # Initialize Conical Sensors
    sensors = SensorSet([
        BinaryFOVSensor(
            theta=18,
            distance=8.5
        )
    ])

    # Initialize Intelligent Agent
    agent_i = UnicycleAgentConfig(
        agent_radius=1,
        controller=[0.15, 1.0, 0.15, -1.0],
        sensors=sensors
    )
    
    # Initialize Random Agent (Levy Agent)
    agent_r = LevyAgentConfig(
        config=agent_i
    )
    
    # Initialize World
    N_AGENTS = 15
    env = RectangularWorldConfig(
        size=(500, 500),
        agentConfig=agent_r,
        n_agents=N_AGENTS,
        seed=10,
        init_type=RectRandomInitialization(
            num_agents=N_AGENTS,
            bb=((50, 350), (150, 450))
        )
    )

    sim(world_config=env, gui=None)


