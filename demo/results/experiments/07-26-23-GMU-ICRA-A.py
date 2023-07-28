from src.novel_swarms.world.simulate import main as sim
from src.novel_swarms.config.AgentConfig import LevyAgentConfig, MazeAgentConfig, UnicycleAgentConfig
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.agent.LevyAgent import LevyAgent
from src.novel_swarms.agent.UnicycleAgent import UnicycleAgent
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.world.initialization.RandomInit import RectRandomInitialization
from src.novel_swarms.world.goals.Goal import CylinderGoal
from src.novel_swarms.behavior import *

if __name__ == "__main__":

    # Initialize Conical Sensors
    sensors = SensorSet([
        BinaryFOVSensor(
            theta=18,
            degrees=True,
            distance=8.5,
            show=True,
        )
    ])

    # Initialize Intelligent Agent
    agent_i = UnicycleAgentConfig(
        agent_radius=2,
        controller=[0.15, 1.0, 0.15, -1.0],
        sensors=sensors,
        body_color=(255, 0, 0),
        body_filled=True
    )
    
    # Initialize Random Agent (Levy Agent)
    agent_r = LevyAgentConfig(
        config=agent_i,
        step_scale=30.0,
        forward_rate=0.30,
        levy_constant=1.2,
    )
    
    # Initialize World
    N_AGENTS = 50
    env = RectangularWorldConfig(
        size=(500, 500),
        behavior=[
            DistanceToGoal(),
        ],
        agentConfig=agent_r,
        n_agents=N_AGENTS,
        seed=10,
        init_type=RectRandomInitialization(
            num_agents=N_AGENTS,
            bb=((50, 350), (150, 450))
        ),
        goals=[CylinderGoal(400, 100, r=8.5, range=40.0)]
    )

    sim(world_config=env, gui=None)


