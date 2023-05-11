from src.novel_swarms.behavior.DistanceToGoal import DistanceToGoal
from src.novel_swarms.behavior.AgentsAtGoal import AgentsAtGoal, PercentageAtGoal
from src.novel_swarms.world.goals.Goal import CylinderGoal
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig, StaticAgentConfig, UnicycleAgentConfig, LevyAgentConfig, MazeAgentConfig
from src.novel_swarms.behavior.TotalCollisions import TotalCollisionsBehavior
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

def get_world(genome):

    worlds = []
    goals = [
        CylinderGoal(250, 200, 20, remove_agents_at_goal=True, range=100),
        CylinderGoal(650, 350, 20, remove_agents_at_goal=True, range=100),
        # CylinderGoal(750, 200, 20, remove_agents_at_goal=True, range=100)
    ]
    for goal in goals:
        SEED = 1
        GUI_PADDING = 15
        BL = 15.1
        N_AGENTS = 10
        WIDTH, HEIGHT = 1000, 1000

        sensors = SensorSet(
            [
                BinaryFOVSensor(
                    theta=14 / 2,
                    distance=(BL * 13.25),
                    bias=0,
                    degrees=True,
                    false_positive=0.0,
                    false_negative=0.0,
                    # Rectangle Representing Environment Boundaries
                    walls=[[GUI_PADDING, GUI_PADDING], [GUI_PADDING + WIDTH, GUI_PADDING + HEIGHT]],
                    wall_sensing_range=(BL * 4),
                    time_step_between_sensing=1,
                    goal_sensing_range=(BL * 29.13),
                    detect_goal_with_added_state=True,
                )
            ],
            custom_state_decision=controller
        )

        agent_maze = MazeAgentConfig(
            controller=genome,
            agent_radius=BL / 2,
            dt=0.13,  # 130ms sampling period
            sensors=sensors,
            seed=SEED,
            idiosyncrasies=False,
            body_filled=True,
            body_color=(255, 0, 0),
            stop_at_goal=False,
        )

        G = [goal]
        objects = []
        behavior = [
            TotalCollisionsBehavior()
        ]

        init = [(400, 900, np.random.random() * 2 * np.pi) for i in range(N_AGENTS)]
        world_config = RectangularWorldConfig(
            size=(WIDTH, HEIGHT),
            n_agents=N_AGENTS,
            seed=SEED,
            behavior=behavior,
            show_walls=True,
            collide_walls=True,
            agent_initialization=init,
            agentConfig=agent_maze,
            padding=15,
            objects=objects,
            goals=G,
            stop_at=6000,
            metadata={'hash': hash(tuple(list(genome)))}
        )
        worlds.append(world_config)
    return worlds


def get_heterogeneous_world(genome):

    species_A = list(genome[0:4]) + [4.0, 0.0]

    species_B = list(genome[4:8]) + [4.0, 0.0]

    worlds = []
    goals = [
        CylinderGoal(250, 200, 20, remove_agents_at_goal=True, range=100),
        CylinderGoal(650, 350, 20, remove_agents_at_goal=True, range=100),
        # CylinderGoal(750, 200, 20, remove_agents_at_goal=True, range=100)
    ]
    for goal in goals:
        SEED = 1
        GUI_PADDING = 15
        BL = 15.1
        N_AGENTS = 12
        WIDTH, HEIGHT = 1000, 1000

        sensors = SensorSet([
            BinaryFOVSensor(
                theta=14 / 2,
                distance=(BL * 13.25),
                bias=0,
                degrees=True,
                false_positive=0.0,
                false_negative=0.0,
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
        heterogeneous_swarm_config = HeterogeneousSwarmConfig()
        heterogeneous_swarm_config.add_sub_populuation(agent_maze_a, 6)
        heterogeneous_swarm_config.add_sub_populuation(agent_maze_b, 6)

        G = [goal]
        objects = []
        behavior = [TotalCollisionsBehavior()]

        init = [(500, 900, np.random.random() * 2 * np.pi) for i in range(N_AGENTS)]
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
            metadata={'hash': hash(tuple(list(genome)))}
        )
        worlds.append(world_config)
    return worlds

def evolve_goal_proximity():
    def fitness(world_set):
        total = 0
        for w in world_set:
            total_dist_to_goal = 0
            for agent in w.population:
                dist = np.linalg.norm((np.array(w.goals[0].center) - agent.getPosition())) - w.goals[0].range
                total_dist_to_goal += max(0, dist)
            penalty = w.behavior[0].out_current()[1] / 100
            total += (total_dist_to_goal / len(w.population)) + penalty
        return total / len(world_set)

    MAX_V, MAX_OMEGA = 20.0, 2.0
    MIN_V = 0
    bounds = [[MIN_V, -MAX_OMEGA, MIN_V, -MAX_OMEGA, MIN_V, -MAX_OMEGA, MIN_V, -MAX_OMEGA], [MAX_V, MAX_OMEGA, MAX_V, MAX_OMEGA, MAX_V, MAX_OMEGA, MAX_V, MAX_OMEGA]]
    x0 = [0.47830279, -0.32490957,  0.92724408,  0.99523116,  0.31646829,  0.39684449, 0.0, 0.0]
    optim = CMAES(f=fitness, genome_to_world=get_heterogeneous_world, init_sigma=3.0, init_genome=x0, pop_size=12, num_processes=12, bounds=bounds, target=0, show_each_step=False)
    c, _ = optim.minimize()
    return c

if __name__ == "__main__":
    evolve_goal_proximity()