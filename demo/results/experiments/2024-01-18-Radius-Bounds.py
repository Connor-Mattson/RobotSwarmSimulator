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


def plot_data():

    bounds_x = np.arange(2.0, 30.0, 0.5)
    upper_bound_y = np.array([150 / (2 * np.sin(np.pi / x)) for x in bounds_x])
    lower_bound_y = np.array([15 / (2 * np.sin(np.pi / x)) for x in bounds_x])

    df_1 = pd.read_csv("../out/SM-Full-Run/sweep/genes.csv")
    df_1 = df_1.loc[df_1['conn_components'] == 1.0]
    df_1 = df_1.loc[df_1['radial_variance'] < 0.002]
    scatter_x = df_1["n"]
    scatter_y = df_1["radius"] * 1.5  # 1.5 converts from pixels to cm

    fig, ax = plt.subplots()
    ax.plot(bounds_x, upper_bound_y, label="Proposed Upper Bound")
    ax.plot(bounds_x, lower_bound_y, label="Proposed Lower Bound")
    ax.scatter(scatter_x, scatter_y, marker="x", alpha=0.45, label="Experiment Radii", c="gray")

    plt.xlabel("Number of Agents")
    plt.ylabel("Milling Radius (cm)")
    plt.title(f"Empirical Assessment of Radius Bounds ({len(df_1)} experiments)")

    plt.legend()
    plt.show()

def plot_GMU_comparison():
    # data_x = list(range(2, 30, 1))
    # data_y = [(((0.1583 * i) + 0.043) * 150) for i in data_x]
    # fig, ax = plt.subplots()

    # upper_bound_y = np.array([150 / (2 * np.sin(np.pi / x)) for x in data_x])

    # GAMMA = 150
    # measured_GMU_x = [6, 8, 10, 12]
    # measured_GMU_y = [
    #     0.9931 * GAMMA + 0.0042,
    #     1.3008 * GAMMA - 0.0038,
    #     1.6146 * GAMMA - 0.0156,
    #     1.9334 * GAMMA - 0.0346
    # ]
    #
    # ax.plot(data_x, data_y, label="Vega et al.")
    # ax.plot(data_x, data_y, label="Upper Bound")
    # ax.scatter(measured_GMU_x, measured_GMU_y, marker="x", label="GMU measurements")
    # plt.legend()
    # plt.show()
    data_x = list(range(2, 30, 1))
    data_y = list(range(50, 300, 25))
    X, Y = np.meshgrid(data_x, data_y)
    Z = ((0.1583 * X) + 0.043) * Y

    fig = plt.figure(figsize=(12,12))
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, cmap='summer', rstride=1, cstride=1, alpha=None)

    ax.set_xlabel("Number of Agents")
    ax.set_ylabel("Vision Distance, $\gamma$ (cm)")
    ax.set_zlabel("Milling Radius (cm)")
    plt.title("Vega et. al Manifold Prediction")
    plt.show()

    data_x = list(range(2, 30, 1))
    data_y = list(range(50, 300, 25))
    X, Y = np.meshgrid(data_x, data_y)
    Z = Y / (2 * np.sin(np.pi / X))

    fig = plt.figure(figsize=(12, 12))
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, cmap='plasma', rstride=1, cstride=1, alpha=None)

    ax.set_xlabel("Number of Agents")
    ax.set_ylabel("Vision Distance, $\gamma$ (cm)")
    ax.set_zlabel("Milling Radius (cm)")
    plt.title("Derived Manifold Prediction")
    plt.show()


# def simulate_termination():
#     OMEGA = 20
#     V = 0.0
#     GAMMA = 10
#     w = gene_to_world(N, PHI, OMEGA, V, GAMMA, MAX_TIME_LIMIT, seed=0)
#     w_out = sim(w, show_gui=True, stop_detection=None)
#     print(w_out.total_steps)
#     print(w_out.behavior[-1].out_current()[1])

if __name__ == "__main__":
    # build_dataset()
    # plot_data()
    plot_GMU_comparison()
    # simulate_termination()