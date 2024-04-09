
import matplotlib.pyplot as plt
import functools
import numpy as np
import os
import time
import pandas as pd
from src.novel_swarms.results.Experiment import Experiment
from src.novel_swarms.config.AgentConfig import AgentYAMLFactory
from src.novel_swarms.config.WorldConfig import WorldYAMLFactory
from src.novel_swarms.behavior import *
from src.novel_swarms.util.processing.multicoreprocessing import MultiWorldSimulation
from src.novel_swarms.agent.control.HomogeneousController import HomogeneousController
from src.novel_swarms.world.initialization.NGonInit import NGonInitialization
from src.novel_swarms.world.simulate import Simulation

SCALE = 10

def gene_to_world(n_agents, fov_angle, w=30, v=1.0, gamma=10, horizon=2000, seed=0, dt=0.13):
    goal_agent = AgentYAMLFactory.from_yaml("demo/configs/swarm-mechanics/flockbot.yaml")
    goal_agent.controller = HomogeneousController([v * SCALE, -np.radians(w), v * SCALE, np.radians(w)])
    goal_agent.sensors.sensors[0].theta = np.radians(fov_angle / 2)
    goal_agent.sensors.sensors[0].r = gamma
    goal_agent.sensors.sensors[0].detect_edges = False
    goal_agent.seed = 0
    goal_agent.dt = dt
    goal_agent.rescale(SCALE)

    world = WorldYAMLFactory.from_yaml("demo/configs/swarm-mechanics/world.yaml")
    world.seed = 0
    world.behavior = [
        AverageSpeedBehavior(history=1),
        AngularMomentumBehavior(history=1),
        RadialVarianceBehavior(history=1),
        ScatterBehavior(history=1),
        GroupRotationBehavior(history=1),
        # AlgebraicConn(history=1, r_disk_size=10.5 * SCALE),
        Circliness(history=1),
        # ScatterBehavior(regularize=False, history=1),
    ]
    world.population_size = n_agents
    world.stop_at = horizon
    world.init_type = NGonInitialization(n_agents, radius=31, disturbance_stddev=0.05)
    world.init_type.reseed(seed)

    world.factor_zoom(zoom=SCALE)
    world.addAgentConfig(goal_agent)
    world.metadata = {'hash': hash(tuple([n_agents, fov_angle, w, v])), 'fov': fov_angle, 'n': n_agents, 'omega': w,
                      'v': v}

    # If a configured initialization was called, we assume that we want to find a solution fit
    # to that specific init, therefore, we only evaluate one world, with no attempt to generalize
    return world


def build_dataset():
    MAX_TIME_LIMIT = 20000
    time_start = time.time()
    world_processor = MultiWorldSimulation(pool_size=24, single_step=False, with_gui=False)
    exp = Experiment("../out", "macrostate")
    o = exp.add_sub("sweep")

    N, PHI = 20, 25
    OMEGA = 60  # FREEZE
    V = 3.33  # FREEZE
    GAMMA = 10  # FREEZE

    data = []
    worlds = [gene_to_world(N, PHI, w=OMEGA, v=V, gamma=GAMMA, horizon=MAX_TIME_LIMIT, seed=s, dt=0.01) for s in range(20)]
    b_ret = world_processor.execute(worlds)
    for w in b_ret:
        b_vec = w.getBehaviorVector()
        data.append([w.meta["n"]] + [w.meta["fov"]] + [w.meta["omega"]] + [w.meta["v"]] + list(b_vec) + [w.total_steps, w.total_steps * w.population[0].dt, w.population[0].dt])

    df = pd.DataFrame(data)
    df.columns = ["n", "fov", "omega", "v", "avg_speed", "angular_momentum", "radial_variance", "scatter", "group_rotation", "circliness",
                  "timesteps", "time", "dt"]

    df.to_csv(os.path.join(o, "genes.csv"))

    np_data = np.array(data)
    for col in [4, 5, 6, 7, 8, 9]:
        print(f"{df.columns[col]} --- mean: {np.mean(np_data[:, col])}, std dev: {np.std(np_data[:, col])}")

    print(f"Elapsed Time: f{time.time() - time_start}s")


if __name__ == "__main__":
    build_dataset()

