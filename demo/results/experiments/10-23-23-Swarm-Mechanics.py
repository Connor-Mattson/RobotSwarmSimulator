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

def gene_to_world(n_agents, fov_angle, w=30, v=1.0, horizon=2000):

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
        AlgebraicConn(history=500, r_disk_size=10 * SCALE, track_components=True),
        ScatterBehavior(regularize=False)
    ]
    world.population_size = n_agents
    world.stop_at = horizon
    world.init_type.reseed(0)

    world.factor_zoom(zoom=SCALE)
    world.addAgentConfig(goal_agent)
    world.metadata = {'hash': hash(tuple([n_agents, fov_angle])), 'fov':fov_angle, 'n':n_agents, 'omega':w, 'v':v}

    # If a configured initialization was called, we assume that we want to find a solution fit
    # to that specific init, therefore, we only evaluate one world, with no attempt to generalize
    return world

def build_dataset():
    time_start = time.time()
    world_processor = MultiWorldSimulation(pool_size=24, single_step=False, with_gui=False)
    exp = Experiment(root="demo/results/out", title=f"SM-{str(int(time.time()))}")
    o = exp.add_sub("sweep")

    data = []
    # Replace mid value with 31
    for n in range(4, 31, 2):
        for omega in range(20, 91, 10):
            for v in range(10, 21, 2):
                print(f"Running with {n} agents and omega= {omega} and velocity {v}!")
                worlds = [gene_to_world(n, phi, w=omega, v=(v / 20), horizon=3500) for phi in range(3, 76, 3)]
                b_ret = world_processor.execute(worlds)
                for w in b_ret:
                    data.append([w.meta["n"]] + [w.meta["fov"]] + [w.meta["omega"]] + [w.meta["v"]] + list(w.getBehaviorVector()))

            df = pd.DataFrame(data)
            df.columns = ["n", "fov", "omega", "v", "average_speed", "angular_momentum", "radial_variance", "scatter", "group_rotation",
                          "lambda_2", "lambda_2_500", "conn_components", "radius"]
            df.to_csv(os.path.join(o, "genes.csv"))
            print(f"Elapsed Time: f{time.time() - time_start}s")
    # 2 Hours for 2409

def simulate():
    N, PHI = 34, 15
    OMEGA = 30
    V = 1.0
    w = gene_to_world(N, PHI, OMEGA, V, None)
    sim(w)

if __name__ == "__main__":
    simulate()