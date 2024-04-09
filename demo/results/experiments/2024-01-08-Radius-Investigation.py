"""
Find the best Homogeneous Agents
"""
import sys

import numpy as np
import os
import time
import argparse
import pandas as pd
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

def m2BL(m):
    return m / 0.15

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
        Circliness(),
        ScatterBehavior(regularize=False, history=horizon, multiplier=1.5),
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



def simulate():
    exp = Experiment("../out", "mechanics-radius")

    N, PHI = 10, 36.0
    OMEGA = 30
    V = 1.0
    GAMMA = m2BL(1.5)
    DT = 0.13
    w = gene_to_world(N, PHI, OMEGA, V, GAMMA, None, seed=0, dt=DT)
    w_out = sim(w, show_gui=True)

    exp.write_metadata(
        {
            "n": N,
            "phi": PHI,
            "V" : V,
            "omega": OMEGA,
            "gamma": GAMMA,
            "dt": DT
        }
    )
    exp.write_array(w_out.behavior[-1].value_history, "radius_hist.txt")

def plot_data():

    FILE = "../out/mechanics-radius-7/radius_hist.txt"

    y_arr_1 = np.loadtxt(FILE)[0:]
    x_arr_1 = np.array(list(range(len(y_arr_1)))) * 0.05

    FILE = "../out/mechanics-radius-4/radius_hist.txt"

    y_arr_2 = np.loadtxt(FILE)[0:][:5000]
    x_arr_2 = np.array(list(range(len(y_arr_2)))) * 0.13

    FILE = "../out/mechanics-radius-10/radius_hist.txt"
    y_arr_3 = np.loadtxt(FILE)[0:]
    x_arr_3 = np.array(list(range(len(y_arr_3)))) * 0.015

    FILE = "../out/mechanics-radius-11/radius_hist.txt"
    y_arr_4 = np.loadtxt(FILE)[0:]
    x_arr_4 = np.array(list(range(len(y_arr_4)))) * 0.002

    plt.plot(x_arr_4, y_arr_4, label="dt=0.002")
    plt.plot(x_arr_3, y_arr_3, label="dt=0.015")
    plt.plot(x_arr_1, y_arr_1, label="dt=0.05")
    plt.plot(x_arr_2, y_arr_2, label="dt=0.13")

    plt.xlabel("Time (s)")
    plt.ylabel("Milling Radius (cm)")
    plt.title("Milling Radius for N=10 agents as dt changes")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # plot_data()
    simulate()