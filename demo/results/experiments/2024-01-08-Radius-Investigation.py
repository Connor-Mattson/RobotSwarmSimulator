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
        AlgebraicConn(history=1, r_disk_size=10 * SCALE),
        AlgebraicConn(history=500, r_disk_size=10 * SCALE),
        # AlgebraicConn(history=500, r_disk_size=10 * SCALE, track_components=True),
        SubBehaviors(r_disk_size=10*SCALE, behavior_classes=[
            AverageSpeedBehavior(history=1),
            AngularMomentumBehavior(history=1),
            RadialVarianceBehavior(history=1),
            ScatterBehavior(history=1),
            GroupRotationBehavior(history=1),
        ]),
        ScatterBehavior(regularize=False, history=100),
        # ScatterBehavior(regularize=False, history=20000),
        # TotalCollisionsBehavior(),
    ]
    world.population_size = n_agents
    world.stop_at = horizon
    world.init_type = NGonInitialization(n_agents, radius=47.95/15)

    world.factor_zoom(zoom=SCALE)
    world.addAgentConfig(goal_agent)
    world.metadata = {'hash': hash(tuple([n_agents, fov_angle, w, v])), 'fov':fov_angle, 'n':n_agents, 'omega':w, 'v':v}

    # If a configured initialization was called, we assume that we want to find a solution fit
    # to that specific init, therefore, we only evaluate one world, with no attempt to generalize
    return world



def simulate():
    exp = Experiment("../out", "mechanics-radius")

    N, PHI = 20, 18
    OMEGA = 30
    V = 1.0
    w = gene_to_world(N, PHI, OMEGA, V, None, seed=0)
    w_out = sim(w, show_gui=True)

    exp.write_metadata(
        {
            "n": N,
            "phi": PHI,
            "V" : V,
            "omega": OMEGA,
        }
    )
    exp.write_array(w_out.behavior[-1].value_history, "radius_hist.txt")

def plot_data():

    FILE = "../out/mechanics-radius-11/radius_hist.txt"
    nparr_1 = np.loadtxt(FILE)[0:]
    nparr_1 *= 1.5

    FILE = "../out/mechanics-radius-4/radius_hist.txt"
    nparr_2 = np.loadtxt(FILE)[0:]
    nparr_2 *= 1.5

    FILE = "../out/mechanics-radius-5/radius_hist.txt"
    nparr_3 = np.loadtxt(FILE)[0:]
    nparr_3 *= 1.5

    FILE = "../out/mechanics-radius-6/radius_hist.txt"
    nparr_4 = np.loadtxt(FILE)[0:]
    nparr_4 *= 1.5

    FILE = "../out/mechanics-radius-7/radius_hist.txt"
    nparr_5 = np.loadtxt(FILE)[0:]
    nparr_5 *= 1.5

    # FILE = "../out/mechanics-radius-10/radius_hist.txt"
    # nparr_6 = np.loadtxt(FILE)[500:]
    # nparr_6 *= 1.5

    t_arr = np.array(list(range(0, len(nparr_2))), dtype=float)
    t_arr *= 0.13

    t_arr_2 = np.array(list(range(0, len(nparr_1))), dtype=float)
    t_arr_2 *= 0.02

    plt.plot(t_arr, nparr_2, label="n=6, $\phi$=60")
    plt.plot(t_arr, nparr_4, label="n=8, $\phi$=45")
    plt.plot(t_arr, nparr_3, label="n=12, $\phi$=30")
    plt.plot(t_arr, nparr_5, label="n=15, $\phi$=24")
    plt.plot(t_arr_2, nparr_1, label="n=20, $\phi$=18")
    # plt.plot(t_arr_2, nparr_6, label="n=24, $\phi$=15")

    plt.xlabel("Time (s)")
    plt.ylabel("Milling Radius (cm)")
    plt.title("Milling Radius over Time (varying N, seed=0)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # plot_data()
    simulate()