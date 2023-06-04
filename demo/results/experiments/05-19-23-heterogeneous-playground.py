from src.novel_swarms.config.AgentConfig import MazeAgentConfig
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.world.simulate import main as sim
import numpy as np

def sim_heterogeneous_maze_world(c_A, c_B, n_A, n_B):
    agent_A = MazeAgentConfig(controller=c_A, sensors=ConfigurationDefaults.FLOCKBOT_SENSOR_SET, dt=0.13, body_color=(255, 0, 0), body_filled=True, agent_radius=15.1/2)
    agent_B = MazeAgentConfig(controller=c_B, sensors=ConfigurationDefaults.FLOCKBOT_SENSOR_SET, dt=0.13, body_color=(0, 255, 0), body_filled=True, agent_radius=15.1/2)

    h_config = HeterogeneousSwarmConfig()
    h_config.add_sub_populuation(agent_A, n_A)
    h_config.add_sub_populuation(agent_B, n_B)

    world = ConfigurationDefaults.RECTANGULAR_WORLD
    world.agentConfig = h_config
    world.behavior = ConfigurationDefaults.BEHAVIOR_VECTOR
    world.collide_walls = False
    world.show_walls = False
    world.population_size = n_A + n_B

    init = []
    init += [(250, 250, 0) for _ in range(n_A)]
    init += [(250, 250, 0) for _ in range(n_B)]
    init = None

    world.agent_init = []
    world.w = 500
    world.h = 500
    world.defined_start = True

    agent_A.attach_world_config(world)
    agent_B.attach_world_config(world)

    w = sim(world, show_gui=True)
    return w


def test():
    c_A = [-10.0, 0.15, 0.0, 1.0]
    c_B = [10.07, 1.47, 10.43, -1.12]
    n_A, n_B = 10, 12
    sim_heterogeneous_maze_world(c_A, c_B, n_A, n_B)


def explore():
    N_COMBINATIONS = [
        (1, 29), (5, 25), (10, 20), (15, 15)
    ]

    KNOWN_BEHAVIORS = {
        "CYCLIC_CW": [18.07, 1.47, 18.43, -1.12],
        "CYCLIC_CCW": [18.07, -1.47, 18.43, 1.12],
        "DISPERSAL_CW": [8.9, 4, -6.0, 4],
        "DISPERSAL_CCW": [8.9, -4, -6.0, -4],
        "AGGREGATION_CW": [-8.5, 0.15, 0.0, 1.0],
        "AGGREGATION_CCW": [-8.5, -0.15, 0.0, -1.0],
        "RANDOM_BEHAVIOR": [-7.9, -3.75, 1.35, -2.85],
    }

    for n_A, n_B in N_COMBINATIONS:
        for k1 in KNOWN_BEHAVIORS.keys():
            for k2 in KNOWN_BEHAVIORS.keys():
                if k1 == k2: continue
                c_A, c_B = KNOWN_BEHAVIORS[k1], KNOWN_BEHAVIORS[k2]
                sim_heterogeneous_maze_world(c_A, c_B, n_A, n_B)


if __name__ == "__main__":
    test()
    # explore()
