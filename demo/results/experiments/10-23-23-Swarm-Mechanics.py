"""
Find the best Homogeneous Agents
"""
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

DECISION_VARS = CMAESVarSet(
    {
        "forward_rate_0": [0, 1 * SCALE],
        "turning_rate_0": [-1.5, 1.5],
        "forward_rate_1": [0, 1 * SCALE],
        "turning_rate_1": [-1.5, 1.5],
    }
)

def gene_to_world(n_agents, fov_angle, horizon=2000):

    goal_agent = AgentYAMLFactory.from_yaml("demo/configs/swarm-mechanics/flockbot.yaml")
    goal_agent.controller = HomogeneousController([1 * SCALE, -np.radians(30), 1 * SCALE, np.radians(30)])
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
        AlgebraicConn(history=500, r_disk_size=10 * SCALE, track_components=True),
        ScatterBehavior(regularize=False)
    ]
    world.population_size = n_agents
    world.stop_at = horizon
    world.init_type.reseed(0)

    world.factor_zoom(zoom=SCALE)
    world.addAgentConfig(goal_agent)
    world.metadata = {'hash': hash(tuple([n_agents, fov_angle])), 'fov':fov_angle, 'n':n_agents}

    # If a configured initialization was called, we assume that we want to find a solution fit
    # to that specific init, therefore, we only evaluate one world, with no attempt to generalize
    return world

def build_dataset():
    world_processor = MultiWorldSimulation(pool_size=24, single_step=False, with_gui=False)
    exp = Experiment(root="demo/results/out", title=f"SM-{str(int(time.time()))}")
    o = exp.add_sub("sweep")

    data = []
    for n in range(4, 37, 2):
        print(f"Running with f{n} agents!")
        worlds = [gene_to_world(n, phi, 2000) for phi in range(3, 76, 3)]
        b_ret = world_processor.execute(worlds)
        for w in b_ret:
            data.append([w.meta["n"]] + [w.meta["fov"]] + list(w.getBehaviorVector()))

    df = pd.DataFrame(data)
    df.columns = ["n", "fov", "average_speed", "angular_momentum", "radial_variance", "scatter", "group_rotation",
                  "lambda_2", "lambda_2_500", "conn_components", "radius"]
    df.to_csv(os.path.join(o, "genes.csv"))


def simulate():
    N, PHI = 20, 6
    w = gene_to_world(N, PHI, None)
    sim(w)

if __name__ == "__main__":
    simulate()