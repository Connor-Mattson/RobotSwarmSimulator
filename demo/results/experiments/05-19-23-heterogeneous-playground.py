from src.novel_swarms.config.AgentConfig import MazeAgentConfig
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.world.simulate import main as sim

def sim_heterogeneous_maze_world(c_A, c_B, n_A, n_B):
    agent_A = MazeAgentConfig(controller=c_A, sensors=ConfigurationDefaults.FLOCKBOT_SENSOR_SET, dt=0.5)
    agent_B = MazeAgentConfig(controller=c_B, sensors=ConfigurationDefaults.FLOCKBOT_SENSOR_SET, dt=0.5)

    h_config = HeterogeneousSwarmConfig()
    h_config.add_sub_populuation(agent_A, n_A)
    h_config.add_sub_populuation(agent_B, n_B)

    world = ConfigurationDefaults.RECTANGULAR_WORLD
    world.agentConfig = h_config
    world.behavior = ConfigurationDefaults.BEHAVIOR_VECTOR
    world.collide_walls = True
    world.show_walls = True

    agent_A.attach_world_config(world)
    agent_B.attach_world_config(world)

    w = sim(world, show_gui=True)
    return w

if __name__ == "__main__":
    c_A = [12.5, 0.5, 12.5, -0.5]
    c_B = [4.5, -0.2, -3.0, -0.2]
    n_A, n_B = 10, 10
    sim_heterogeneous_maze_world(c_A, c_B, n_A, n_B)