import random

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

def get_homogeneous_world(genome):

    gene = list(genome) + [4.0, 0.0]
    worlds = []
    goals = [
        CylinderGoal(700, 200, 20, remove_agents_at_goal=True, range=100),
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
            controller=gene,
            agent_radius=BL / 2,
            # dt=0.13,  # 130ms sampling period
            dt=0.5,
            sensors=sensors,
            seed=SEED,
            idiosyncrasies=False,
            body_filled=True,
            body_color=(255, 0, 0),
            stop_at_goal=False,
        )

        G = [goal]
        objects = []
        behavior = [TotalCollisionsBehavior()]

        init = [(200, 700, np.random.random() * (np.pi / 2)) for i in range(N_AGENTS)]
        world_config = RectangularWorldConfig(
            size=(WIDTH, HEIGHT),
            n_agents=N_AGENTS,
            seed=SEED,
            behavior=behavior,
            show_walls=False,
            collide_walls=False,
            agent_initialization=init,
            agentConfig=agent_maze_a,
            padding=15,
            objects=objects,
            goals=G,
            stop_at=1800,
            metadata={'hash': hash(tuple(list(genome)))}
        )
        worlds.append(world_config)
    return worlds

def get_heterogeneous_world(genome):

    world_hash = hash(tuple(list(genome)))
    genome = scale_type_3_genome(genome)
    species_A = list(genome[0:4]) + [4.0, 0.0]
    species_B = list(genome[4:8]) + [4.0, 0.0]
    starting_A = list(genome[8:])

    worlds = []
    goals = [
        CylinderGoal(500, 500, 20, remove_agents_at_goal=True, range=100),
        # CylinderGoal(650, 350, 20, remove_agents_at_goal=True, range=100),
        # CylinderGoal(750, 200, 20, remove_agents_at_goal=True, range=100)
    ]
    for goal in goals:
        SEED = 1
        GUI_PADDING = 15
        BL = 15.1
        N_AGENTS = 24
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

        sensor_2 = SensorSet([
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
                goal_sensing_range=(BL * 1),
                detect_goal_with_added_state=True,
            )
        ],
            custom_state_decision=controller)

        agent_maze_a = MazeAgentConfig(
            controller=species_A,
            agent_radius=BL / 2,
            # dt=0.13,  # 130ms sampling period
            dt=0.26,
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
            # dt=0.13,  # 130ms sampling period
            dt=0.26,
            sensors=sensor_2,
            seed=SEED,
            idiosyncrasies=False,
            body_filled=True,
            body_color=(0, 255, 0),
            stop_at_goal=False,
        )
        heterogeneous_swarm_config = HeterogeneousSwarmConfig()
        heterogeneous_swarm_config.add_sub_populuation(agent_maze_a, 1)
        heterogeneous_swarm_config.add_sub_populuation(agent_maze_b, 11)

        G = [goal]
        objects = []
        behavior = [TotalCollisionsBehavior(), DistanceToGoal(history=1000)]

        np.random.seed(SEED)
        random.seed(SEED)
        first_agent_pos = [(starting_A[0], starting_A[1], starting_A[2])]
        # init = [(100 + (i * 10), 800 + (i * 10), np.random.random() * 2 * np.pi) for i in range(N_AGENTS - 1)]
        init = [(100, 800, np.random.random() * 2 * np.pi) for _ in range(N_AGENTS - 1)]
        init = first_agent_pos + init
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
        worlds.append(world_config)
    return worlds

def get_distance_running_world(genome):

    world_hash = hash(tuple(list(genome)))
    genome = scale_type_2_genome(genome)
    species_A = list(genome[0:4]) + [4.0, 0.0]
    species_B = list(genome[4:8]) + [4.0, 0.0]

    worlds = []
    goals = []

    SEED = 1
    GUI_PADDING = 15
    BL = 15.1
    N_AGENTS = 24
    WIDTH, HEIGHT = 2000, 1000

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

    sensor_2 = SensorSet([
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
            goal_sensing_range=(BL * 1),
            detect_goal_with_added_state=True,
        )
    ],
        custom_state_decision=controller)

    agent_maze_a = MazeAgentConfig(
        controller=species_A,
        agent_radius=BL / 2,
        # dt=0.13,  # 130ms sampling period
        dt=0.26,
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
        # dt=0.13,  # 130ms sampling period
        dt=0.26,
        sensors=sensor_2,
        seed=SEED,
        idiosyncrasies=False,
        body_filled=True,
        body_color=(0, 255, 0),
        stop_at_goal=False,
    )
    heterogeneous_swarm_config = HeterogeneousSwarmConfig()
    heterogeneous_swarm_config.add_sub_populuation(agent_maze_a, 0)
    heterogeneous_swarm_config.add_sub_populuation(agent_maze_b, 24)

    G = []
    objects = []
    behavior = [TotalCollisionsBehavior()]

    np.random.seed(SEED)
    random.seed(SEED)
    # first_agent_pos = [(starting_A[0], starting_A[1], starting_A[2])]
    init = [(200 + (i * 30), 800, np.random.random() * 2 * np.pi) for i in range(N_AGENTS)]
    # init = [(1500, 500, np.random.random() * 2 * np.pi) for _ in range(N_AGENTS)]
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
        stop_at=2500,
        metadata={'hash': world_hash}
    )
    worlds.append(world_config)
    return worlds

def evolve_goal_proximity_heterogeneous():
    def fitness(world_set):
        total = 0
        for w in world_set:
            total_dist_to_goal = 0
            for agent in w.population:
                dist = np.linalg.norm((np.array(w.goals[0].center) - agent.getPosition())) - w.goals[0].range
                total_dist_to_goal += max(0, dist)
            collisions_penalty = w.behavior[0].out_current()[1] / 100
            time_penalty = w.behavior[1].out_average()[1]
            total += (total_dist_to_goal / len(w.population)) + collisions_penalty + time_penalty
        return total / len(world_set)

    MAX_V, MAX_OMEGA = 20.0, 2.0
    MIN_V = -20.0
    bounds = [[MIN_V, -MAX_OMEGA, MIN_V, -MAX_OMEGA, MIN_V, -MAX_OMEGA, MIN_V, -MAX_OMEGA], [MAX_V, MAX_OMEGA, MAX_V, MAX_OMEGA, MAX_V, MAX_OMEGA, MAX_V, MAX_OMEGA]]
    x0 = [0.0 for _ in range(8)]
    optim = CMAES(f=fitness, genome_to_world=get_heterogeneous_world, init_sigma=3.0, init_genome=x0, pop_size=5, num_processes=10, bounds=bounds, target=0, show_each_step=False)
    c, _ = optim.minimize()
    return c

def evolve_goal_proximity_heterogeneous_with_positional_init():
    def fitness(world_set):
        total = 0
        for w in world_set:
            total_dist_to_goal = 0
            for agent in w.population:
                dist = np.linalg.norm((np.array(w.goals[0].center) - agent.getPosition())) - w.goals[0].range
                total_dist_to_goal += max(0, dist)
            penalty = w.behavior[0].out_current()[1] / 100
            # penalty = 0
            total += (total_dist_to_goal / len(w.population)) + penalty
        return total / len(world_set)

    bounds = [[0 for _ in range(11)], [1 for _ in range(11)]]
    x0 = [0.5 for _ in range(11)]
    optim = CMAES(f=fitness, genome_to_world=get_heterogeneous_world, init_sigma=0.16, init_genome=x0, pop_size=16, num_processes=16, bounds=bounds, target=0, show_each_step=False)
    c, _ = optim.minimize()
    return c

def evolve_x_dist_heterogeneous_with_positional_init():
    def fitness(world_set):
        total = 0
        for w in world_set:
            total_x = 0
            for agent in w.population:
                total_x += agent.getPosition()[0]
            penalty = w.behavior[0].out_current()[1] / 10
            # penalty = 0
            total += (total_x / len(w.population)) - penalty
        return -(total / len(world_set))

    bounds = [[0 for _ in range(8)], [1 for _ in range(8)]]
    x0 = [0.5 for _ in range(8)]
    optim = CMAES(f=fitness, genome_to_world=get_distance_running_world, init_sigma=0.16, init_genome=x0, pop_size=32, num_processes=16, bounds=bounds, target=-10000, show_each_step=False)
    c, _ = optim.minimize()
    return c

def evolve_goal_proximity_homogeneous():
    def fitness(world_set):
        total = 0
        for w in world_set:
            total_dist_to_goal = 0
            for agent in w.population:
                dist = np.linalg.norm((np.array(w.goals[0].center) - agent.getPosition())) - w.goals[0].range
                total_dist_to_goal += max(0, dist)
            penalty = w.behavior[0].out_current()[1] / 100
            # penalty = 0
            total += (total_dist_to_goal / len(w.population)) + penalty
        return total / len(world_set)

    MAX_V, MAX_OMEGA = 20.0, 2.0
    MIN_V = -20.0
    bounds = [[MIN_V, -MAX_OMEGA, MIN_V, -MAX_OMEGA], [MAX_V, MAX_OMEGA, MAX_V, MAX_OMEGA]]
    x0 = [-4.35744979e+00,  1.44512778e-02, -1.36536727e+01,  6.79787074e-03]
    optim = CMAES(f=fitness, genome_to_world=get_homogeneous_world, init_sigma=3.0, init_genome=x0, pop_size=30, num_processes=15, bounds=bounds, target=0, show_each_step=False)
    c, _ = optim.minimize()
    return c

def lerp(x, _min, _max):
    return (x * (_max - _min)) + _min

def scale_type_2_genome(g):
    MIN_V, MAX_V = -20.0, 20.0
    MIN_W, MAX_W = -2.0, 2.0
    g_0, g_2, g_4, g_6 = lerp(g[0], MIN_V, MAX_V), lerp(g[2], MIN_V, MAX_V), lerp(g[4], MIN_V, MAX_V), lerp(g[6], MIN_V, MAX_V)
    g_1, g_3, g_5, g_7 = lerp(g[1], MIN_W, MAX_W), lerp(g[3], MIN_W, MAX_W), lerp(g[5], MIN_W, MAX_W), lerp(g[7], MIN_W, MAX_W)
    return [g_0, g_1, g_2, g_3, g_4, g_5, g_6, g_7]

def scale_type_3_genome(g):
    MIN_V, MAX_V = -20.0, 20.0
    MIN_W, MAX_W = -2.0, 2.0
    X_MIN, X_MAX = 0, 150
    Y_MIN, Y_MAX = 600, 750
    ROT_MIN, ROT_MAX = 0, np.pi * 2
    g_0, g_2, g_4, g_6 = lerp(g[0], MIN_V, MAX_V), lerp(g[2], MIN_V, MAX_V), lerp(g[4], MIN_V, MAX_V), lerp(g[6], MIN_V, MAX_V)
    g_1, g_3, g_5, g_7 = lerp(g[1], MIN_W, MAX_W), lerp(g[3], MIN_W, MAX_W), lerp(g[5], MIN_W, MAX_W), lerp(g[7], MIN_W, MAX_W)
    g_8, g_9, g_10 = lerp(g[8], X_MIN, X_MAX), lerp(g[9], Y_MIN, Y_MAX), lerp(g[10], ROT_MIN, ROT_MAX)
    return [g_0, g_1, g_2, g_3, g_4, g_5, g_6, g_7, g_8, g_9, g_10]

def simulate_result(g):
    w = evolve_goal_proximity_heterogeneous_with_positional_init(g)
    simulate(w[0], show_gui=True)

if __name__ == "__main__":
    # c = evolve_goal_proximity_heterogeneous_with_positional_init()
    # evolve_x_dist_heterogeneous_with_positional_init()

    c = [0.5012, -1.298, -10.21, -0.9, 13.25, 1.731, 17.53, -0.32, 73.9, 638.57, 4.4]
    # c = [0.95199212, 0.86892135, 0.96099064, 0.21897237, 0.93191356, 0.38231108, 0.85665234, 0.73857901]
    # c = [0.75411337, 0.49950559, 0.34436176, 0.76382902, 0.43953329, 0.01289864, 0.002985, 0.7177732]
    print(f"FOUND: {c}")
    print(f"REAL FORM: {scale_type_3_genome(c)}")
    simulate_result(c)
    # evolve_goal_proximity_heterogeneous()