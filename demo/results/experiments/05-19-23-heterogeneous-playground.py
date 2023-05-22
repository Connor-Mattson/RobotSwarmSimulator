from src.novel_swarms.config.AgentConfig import MazeAgentConfig
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.world.simulate import main as sim

def sim_heterogeneous_maze_world(c_A, c_B, n_A, n_B):
    agent_A = MazeAgentConfig(controller=c_A, sensors=ConfigurationDefaults.FLOCKBOT_SENSOR_SET, dt=0.13, body_color=(255, 0, 0), body_filled=True)
    agent_B = MazeAgentConfig(controller=c_B, sensors=ConfigurationDefaults.FLOCKBOT_SENSOR_SET, dt=0.13, body_color=(0, 255, 0), body_filled=True)

    h_config = HeterogeneousSwarmConfig()
    h_config.add_sub_populuation(agent_A, n_A)
    h_config.add_sub_populuation(agent_B, n_B)

    world = ConfigurationDefaults.RECTANGULAR_WORLD
    world.agentConfig = h_config
    world.behavior = ConfigurationDefaults.BEHAVIOR_VECTOR
    world.collide_walls = False
    world.show_walls = False
    world.agent_init = [(250, 250, 0) for _ in range(n_A + n_B)]
    world.w = 1000
    world.h = 1000
    world.defined_start = True

    agent_A.attach_world_config(world)
    agent_B.attach_world_config(world)

    w = sim(world, show_gui=True)
    return w

if __name__ == "__main__":
    c_A = [18.07, 1.47, 18.43, -1.12]
    c_B = [17.2, -1.47, 14.26, 0.954]
    n_A, n_B = 15, 15
    sim_heterogeneous_maze_world(c_A, c_B, n_A, n_B)