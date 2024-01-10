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

def gene_to_world(n_agents, fov_angle, w=30, v=1.0, horizon=2000, seed=0):

    goal_agent = AgentYAMLFactory.from_yaml("demo/configs/swarm-mechanics/flockbot.yaml")
    goal_agent.controller = HomogeneousController([v * SCALE, -np.radians(w), v * SCALE, np.radians(w)])
    goal_agent.sensors.sensors[0].theta = np.radians(fov_angle / 2)

    goal_agent.sensors.sensors[0].detect_edges = False
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
        # ]),
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
    world.metadata = {'hash': hash(tuple([n_agents, fov_angle, w, v])), 'fov':fov_angle, 'n':n_agents, 'omega':w, 'v':v}

    # If a configured initialization was called, we assume that we want to find a solution fit
    # to that specific init, therefore, we only evaluate one world, with no attempt to generalize
    return world

def build_dataset():
    time_start = time.time()
    world_processor = MultiWorldSimulation(pool_size=24, single_step=False, with_gui=False)
    exp = Experiment("../out", "r-convergence")
    o = exp.add_sub("sweep")

    data = []
    for n in range(6, 31, 1):
        # Just simulate elements below the 2pi/N manifold
        phi_below_manifold = [phi if phi <= (360 / n) else None for phi in range(3, 76, 1)]
        final_phi = list(filter(lambda x: x is not None, phi_below_manifold))
        print(f"Running with {n} agents on phi values {final_phi}!")

        worlds = [gene_to_world(n, phi, w=30, v=1.0, horizon=MAX_TIME_LIMIT) for phi in final_phi]
        b_ret = world_processor.execute(worlds, world_stop_condition=stop_when_radius_converges)
        for w in b_ret:
            data.append([w.meta["n"]] + [w.meta["fov"]] + [w.meta["omega"]] + [w.meta["v"]] + list(w.getBehaviorVector()) + [w.total_steps, w.total_steps * w.population[0].dt])

        df = pd.DataFrame(data)
        df.columns = ["n", "fov", "omega", "v", "conn_components", "radius", "timesteps", "time"]
        df.to_csv(os.path.join(o, "genes.csv"))
        print(f"Elapsed Time: f{time.time() - time_start}s")
    exp.write_metadata({})


def plot_data():

    df = pd.read_csv("../out/r-convergence-5/sweep/genes.csv")
    df = df.pivot(index="fov", columns="n", values="radius")
    ax = sns.heatmap(df, annot=True, cmap="crest", fmt=".2f", norm=LogNorm(), cbar=False)
    ax.invert_yaxis()
    # plt.xlabel("Time (s)")
    # plt.ylabel("Milling Radius (cm)")
    plt.title("Milling Radius (cm)")
    plt.show()

def simulate_termination():
    N, PHI = 7, 27
    OMEGA = 30
    V = 1.0
    w = gene_to_world(N, PHI, OMEGA, V, MAX_TIME_LIMIT, seed=0)
    w_out = sim(w, show_gui=True, stop_detection=None)
    print(w_out.total_steps)

if __name__ == "__main__":
    build_dataset()
    # plot_data()
    # simulate_termination()