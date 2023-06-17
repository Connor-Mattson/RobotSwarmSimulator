from src.novel_swarms.behavior.Centroid import Centroid
from src.novel_swarms.behavior.DistanceToGoal import DistanceToGoal
from src.novel_swarms.behavior.AgentsAtGoal import AgentsAtGoal, PercentageAtGoal
from src.novel_swarms.behavior.TotalCollisions import TotalCollisionsBehavior
from src.novel_swarms.world.goals.Goal import CylinderGoal
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig, StaticAgentConfig, UnicycleAgentConfig, LevyAgentConfig, MazeAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from src.novel_swarms.optim.CMAES import CMAES
import numpy as np


def controller(sensor_states):
    if sensor_states[0] == 0:
        return 0
    if sensor_states[0] == 1:
        return 1
    if sensor_states[0] == 2:
        return 2
def get_heterogeneous_world(genome):

    species_A = list(genome[0:4]) + [4.0, 0.0]
    species_B = list(genome[4:8]) + [4.0, 0.0]

    worlds = []
    goals = [
        CylinderGoal(250, 200, 20, remove_agents_at_goal=True, range=100),
        # CylinderGoal(650, 350, 20, remove_agents_at_goal=True, range=100),
        # CylinderGoal(0, 1000, 20, remove_agents_at_goal=True, range=100),
        # CylinderGoal(1000, 0, 20, remove_agents_at_goal=True, range=100),
        # CylinderGoal(750, 200, 20, remove_agents_at_goal=True, range=100)
    ]
    for goal in goals:
        SEED = 1
        GUI_PADDING = 15
        BL = 15.1

        WIDTH, HEIGHT = 1000, 1000

        sensors = SensorSet([
            BinaryFOVSensor(
                theta=14 / 2,
                distance=(BL * 13.25),
                bias=0,
                degrees=True,
                # false_positive=0.0,
                # false_negative=0.0,
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

        agent_maze_a = MazeAgentConfig(
            controller=species_A,
            agent_radius=BL / 2,
            dt=0.13,  # 130ms sampling period
            sensors=sensors,
            seed=SEED,
            idiosyncrasies=False,
            body_filled=True,
            body_color=(255, 0, 0),
            stop_at_goal=False,
        )

        agent_maze_b = MazeAgentConfig(
            controller=species_B,
            agent_radius=BL / 2,
            dt=0.13,  # 130ms sampling period
            sensors=sensors,
            seed=SEED,
            idiosyncrasies=False,
            body_filled=True,
            body_color=(0, 255, 0),
            stop_at_goal=False,
        )

        NUM_A, NUM_B = 1, 11
        heterogeneous_swarm_config = HeterogeneousSwarmConfig()
        heterogeneous_swarm_config.add_sub_populuation(agent_maze_a, NUM_A)
        heterogeneous_swarm_config.add_sub_populuation(agent_maze_b, NUM_B)

        G = goals
        objects = []
        behavior = [
            TotalCollisionsBehavior(),
            # DistanceToGoal(),
            Centroid(history=10),
        ]

        N_AGENTS = NUM_A + NUM_B
        np.random.seed(SEED)
        r = 80
        pi_frac = 2 * (np.pi / N_AGENTS)
        center_x, center_y = 500, 500
        init = [(center_x + r * np.cos(pi_frac * i), center_y + r * np.sin(pi_frac * i), i * pi_frac) for i in range(N_AGENTS)]
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
            metadata={'hash': hash(tuple(list(genome)))}
        )
        worlds.append(world_config)
    return worlds

def run_simulation():
    # genome = [11.94, -0.48, 2.80, 0.38, 12.82, -0.66, 0.13, -1.41]
    # genome = [14.09449214, -0.09365658, 13.13571482,  1.09531036, 13.28770632, -0.08053101, 8.05740008,  0.69650941]
    # genome = [11.94, -0.48, 2.80, 0.38, -7.5, -1.2, -7.5, 0.0]


    genome = [0.5012, -1.298, -10.21, -0.9, 5, -0.1745, 5, -0.1745, 73.9, 638.57, 4.4]
    # genome = [1.91, 1.14, -0.90, -0.12, 7.58, 0.41, -6.26, -0.89]

    # genome = [11.94, -0.48, 2.80, 0.38, -8, -0.15, -6, 0.87]
    worlds = get_heterogeneous_world(genome)
    simulate(worlds[0], show_gui=True, world_key_events=False, step_size=5)

if __name__ == "__main__":
    run_simulation()