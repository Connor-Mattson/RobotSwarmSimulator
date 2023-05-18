import random

import numpy as np

from src.novel_swarms.behavior.DistanceToGoal import DistanceToGoal
from src.novel_swarms.behavior.TotalCollisions import TotalCollisionsBehavior
from src.novel_swarms.config.AgentConfig import MazeAgentConfig
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.world.goals.Goal import CylinderGoal
from src.novel_swarms.world.simulate import main as sim

def controller(sensor_states):
    if sensor_states[0] == 0:
        return 0
    if sensor_states[0] == 1:
        return 1
    if sensor_states[0] == 2:
        return 2
def get_heterogeneous_world(genome):

    world_hash = hash(tuple(list(genome)))
    species_A = list(genome[0:4]) + [16.0, 0.02]
    species_B = list(genome[4:8]) + [4.0, -1.2]
    # starting_A = list(genome[8:])

    worlds = []
    goals = [
        # CylinderGoal(50 + (np.random.random() * 900), 50 + (np.random.random() * 900), 20, remove_agents_at_goal=True, range=100),
        CylinderGoal(100, 300, 20, remove_agents_at_goal=True, range=100)
    ]

    SEED = 9
    GUI_PADDING = 15
    BL = 15.1
    N_AGENTS = 12
    WIDTH, HEIGHT = 1000, 1000

    sensors = SensorSet([
        BinaryFOVSensor(
            theta=14 / 2,
            distance=(BL * 13.25),
            bias=4,
            degrees=True,
            false_positive=0.1,
            false_negative=0.05,
            # Rectangle Representing Environment Boundaries
            walls=None,
            wall_sensing_range=(BL * 4),
            time_step_between_sensing=1,
            goal_sensing_range=(BL * 29.13),
            detect_goal_with_added_state=True,
        )
    ],
        custom_state_decision=controller)

    sensor_2 = SensorSet([
        BinaryFOVSensor(
            theta=14 / 2,
            distance=(BL * 13.25),
            bias=4,
            degrees=True,
            false_positive=0.1,
            false_negative=0.05,
            # Rectangle Representing Environment Boundaries
            walls=None,
            wall_sensing_range=(BL * 4),
            time_step_between_sensing=1,
            goal_sensing_range=(BL * 1),
            detect_goal_with_added_state=False,
        )
    ],
        custom_state_decision=controller)

    agent_maze_a = MazeAgentConfig(
        controller=species_A,
        agent_radius=BL / 2,
        # dt=0.13,  # 130ms sampling period
        dt=0.13,
        sensors=sensors,
        seed=SEED,
        idiosyncrasies=True,
        body_filled=True,
        body_color=(255, 0, 0),
        stop_at_goal=False,
    )

    agent_maze_b = MazeAgentConfig(
        controller=species_B,
        agent_radius=BL / 2,
        # dt=0.13,  # 130ms sampling period
        dt=0.13,
        sensors=sensor_2,
        seed=SEED,
        idiosyncrasies=False,
        body_filled=True,
        body_color=(0, 255, 0),
        stop_at_goal=False,
    )
    heterogeneous_swarm_config = HeterogeneousSwarmConfig()
    heterogeneous_swarm_config.add_sub_populuation(agent_maze_a, 3)
    heterogeneous_swarm_config.add_sub_populuation(agent_maze_b, 9)

    G = goals
    objects = []
    behavior = [TotalCollisionsBehavior(), DistanceToGoal(history=1000)]

    np.random.seed(SEED)
    random.seed(SEED)
    # first_agent_pos = [(starting_A[0], starting_A[1], starting_A[2])]
    # init = [(100 + (i * 10), 800 + (i * 10), np.random.random() * 2 * np.pi) for i in range(N_AGENTS - 1)]
    init = [(500, 500, np.random.random() * 2 * np.pi) for _ in range(N_AGENTS)]
    init[0] = (init[0][0], init[0][1], 5.14)
    # init = first_agent_pos + init
    world_config = RectangularWorldConfig(
        size=(WIDTH, HEIGHT),
        n_agents=N_AGENTS,
        seed=SEED,
        behavior=behavior,
        show_walls=False,
        collide_walls=False,
        agent_initialization=init,
        agentConfig=heterogeneous_swarm_config,
        padding=15,
        objects=objects,
        goals=G,
        stop_at=4000,
        metadata={'hash': world_hash}
    )
    return world_config

if __name__ == "__main__":
    g = [0.5012, -1.298, 0.0, -0.9, 13.25, 1.731, 17.53, -0.32]
    # g = [13.25, 1.731, 17.53, -0.32, 13.25, 1.731, 17.53, -0.32, 200.9, 700.57, 4.4]
    w = get_heterogeneous_world(g)
    world_out = sim(w, show_gui=True)
    print(world_out.as_config_dict())
