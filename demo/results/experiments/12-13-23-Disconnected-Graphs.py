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
from src.novel_swarms.world.initialization.FixedInit import FixedInitialization
from src.novel_swarms.behavior import *
from src.novel_swarms.util.processing.multicoreprocessing import MultiWorldSimulation
from src.novel_swarms.agent.control.Controller import Controller
from src.novel_swarms.agent.control.HomogeneousController import HomogeneousController
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.world.simulate import main as sim

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
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
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
        ScatterBehavior(regularize=False)
    ]
    world.population_size = n_agents
    world.stop_at = horizon
    world.init_type.reseed(seed)

    world.factor_zoom(zoom=SCALE)
    world.addAgentConfig(goal_agent)
    world.metadata = {'hash': hash(tuple([n_agents, fov_angle, w, v])), 'fov':fov_angle, 'n':n_agents, 'omega':w, 'v':v}

    # If a configured initialization was called, we assume that we want to find a solution fit
    # to that specific init, therefore, we only evaluate one world, with no attempt to generalize
    return world

def simulate():
    N, PHI = 20, 15
    OMEGA = 30
    V = 1.0
    w = gene_to_world(N, PHI, OMEGA, V, None, seed=0)
    w_out = sim(w, show_gui=True)

if __name__ == "__main__":
    simulate()