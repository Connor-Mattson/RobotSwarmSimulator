"""
Find the best Homogeneous Agents
"""
import sys

import numpy as np
import os
import time
import argparse
import pandas as pd
import seaborn as sns
from matplotlib.colors import LogNorm
from src.novel_swarms.optim.CMAES import CMAES
from src.novel_swarms.optim.OptimVar import CMAESVarSet
from src.novel_swarms.results.Experiment import Experiment
from src.novel_swarms.config.AgentConfig import AgentYAMLFactory
from src.novel_swarms.config.WorldConfig import WorldYAMLFactory
from src.novel_swarms.world.initialization.NGonInit import NGonInitialization
from src.novel_swarms.behavior import *
from src.novel_swarms.util.processing.multicoreprocessing import MultiWorldSimulation
from src.novel_swarms.agent.control.Controller import Controller
from src.novel_swarms.agent.control.HomogeneousController import HomogeneousController
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.world.simulate import main as sim
import matplotlib.pyplot as plt

SCALE = 10
MAX_TIME_LIMIT = 100000

def stop_when_radius_converges(world):
    """
    Compute the instantaneous R.O.C. for the Scatter (Radius) behavior
    """
    radius_h = world.behavior[-1].value_history
    THRESHOLD = 5e-2
    if world.total_steps > 300 and len(radius_h) > 200:
        roc = radius_h[-1] - radius_h[0]
        # print(roc)
        if roc < 0:
            return True
    return False

def gene_to_world(n_agents, fov_angle, w=30, v=1.0, gamma=10, horizon=2000, seed=0):

    goal_agent = AgentYAMLFactory.from_yaml("demo/configs/swarm-mechanics/flockbot.yaml")
    goal_agent.controller = HomogeneousController([v * SCALE, -np.radians(w), v * SCALE, np.radians(w)])
    goal_agent.sensors.sensors[0].theta = np.radians(fov_angle / 2)
    goal_agent.sensors.sensors[0].r = gamma
    goal_agent.sensors.sensors[0].detect_edges = False
    goal_agent.sensors.sensors[0].store_history = True
    goal_agent.seed = 0
    goal_agent.rescale(SCALE)

    world = WorldYAMLFactory.from_yaml("demo/configs/swarm-mechanics/world.yaml")
    world.seed = 0
    world.behavior = [
        # AverageSpeedBehavior(),
        # AngularMomentumBehavior(),
        # RadialVarianceBehavior(),
        # ScatterBehavior(),
        # GroupRotationBehavior(),
        # AlgebraicConn(history=1, r_disk_size=10 * SCALE),
        # AlgebraicConn(history=500, r_disk_size=10 * SCALE),
        AlgebraicConn(history=500, r_disk_size=10 * SCALE, track_components=True),
        # SubBehaviors(r_disk_size=10*SCALE, behavior_classes=[
        #     AverageSpeedBehavior(history=1),
        #     AngularMomentumBehavior(history=1),
        #     RadialVarianceBehavior(history=1),
        #     ScatterBehavior(history=1),
        #     GroupRotationBehavior(history=1),
        #     Circliness(history=1),
        # ]),
        SensorSignalBehavior(history=100, show=False, sensor_index=0),
        Circliness(),
        ScatterBehavior(regularize=False, history=201),
        # ScatterBehavior(regularize=False, history=20000),
        # TotalCollisionsBehavior(),
    ]
    world.population_size = n_agents
    world.stop_at = horizon

    # Smallest Radius Possible
    r = 1 / (2 * np.sin(np.pi / n_agents))
    world.init_type = NGonInitialization(n_agents, radius=r)

    world.factor_zoom(zoom=SCALE)
    world.addAgentConfig(goal_agent)
    world.metadata = {'hash': hash(tuple([n_agents, fov_angle, w, v])), 'fov':fov_angle, 'n':n_agents, 'omega':w, 'v':v, 'gamma':gamma}

    # If a configured initialization was called, we assume that we want to find a solution fit
    # to that specific init, therefore, we only evaluate one world, with no attempt to generalize
    return world

def build_dataset():
    time_start = time.time()
    world_processor = MultiWorldSimulation(pool_size=24, single_step=False, with_gui=False)

    phi = 12
    n = 12

    exp = Experiment("../out", f"r-{n}-{phi}")
    o = exp.add_sub("sweep")

    data = []

    # Just simulate elements below the 2pi/N manifold
    gamma = [3.33333 * i for i in range(1, 7)]

    worlds = [gene_to_world(n, phi, w=30, v=1.0, gamma=g, horizon=MAX_TIME_LIMIT) for g in gamma]
    b_ret = world_processor.execute(worlds, world_stop_condition=stop_when_radius_converges)
    for w in b_ret:
        data.append([w.meta["n"], w.meta["fov"], w.meta["omega"], w.meta["v"], w.meta["gamma"]] + list(w.getBehaviorVector()) + [w.total_steps, w.total_steps * w.population[0].dt])

    df = pd.DataFrame(data)
    df.columns = ["n", "fov", "omega", "v", "gamma", "conn_components", "circliness", "radius", "timesteps", "time"]
    df.to_csv(os.path.join(o, "genes.csv"))
    print(f"Elapsed Time: f{time.time() - time_start}s")
    exp.write_metadata({})


def plot_data():

    x = [0.5 * i for i in range(1, 7)]

    df_1 = pd.read_csv("../out/r-12-30/sweep/genes.csv").to_numpy()
    df_1[:, -3] *= .015
    plt.plot(x, df_1[:, -3], linestyle='--', marker='o', label="$\phi$ = 30")

    df_1 = pd.read_csv("../out/r-12-29/sweep/genes.csv").to_numpy()
    df_1[:, -3] *= .015
    plt.plot(x, df_1[:, -3], linestyle='--', marker='o', label="$\phi$ = 29")

    df_1 = pd.read_csv("../out/r-12-28/sweep/genes.csv").to_numpy()
    df_1[:, -3] *= .015
    plt.plot(x, df_1[:, -3], linestyle='--', marker='o', label="$\phi$ = 28")

    df_1 = pd.read_csv("../out/r-12-27/sweep/genes.csv").to_numpy()
    df_1[:, -3] *= .015
    plt.plot(x, df_1[:, -3], linestyle='--', marker='o', label="$\phi$ = 27")

    df_1 = pd.read_csv("../out/r-12-24/sweep/genes.csv").to_numpy()
    df_1[:, -3] *= .015
    plt.plot(x, df_1[:, -3], linestyle='--', marker='o', label="$\phi$ = 24")

    # df_1 = pd.read_csv("../out/r-12-30/sweep/genes.csv").to_numpy()
    # df_1[:, -3] *= .015
    # plt.plot(x, df_1[:, -3], linestyle='--', marker='o', label="$\phi$ = 30")

    plt.xlabel("Vision Distance (meters)")
    plt.ylabel("Milling Radius (meters)")


    plt.legend()
    plt.show()

def simulate_termination():
    OMEGA = 20
    V = 0.0
    GAMMA = 10
    w = gene_to_world(N, PHI, OMEGA, V, GAMMA, MAX_TIME_LIMIT, seed=0)
    w_out = sim(w, show_gui=True, stop_detection=None)
    print(w_out.total_steps)
    print(w_out.behavior[-1].out_current()[1])

if __name__ == "__main__":
    # build_dataset()
    # plot_data()
    simulate_termination()