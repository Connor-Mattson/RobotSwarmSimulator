
import matplotlib.pyplot as plt
import functools
import numpy as np
import os
import time
import pandas as pd
import pygame

from src.novel_swarms.results.Experiment import Experiment
from src.novel_swarms.config.AgentConfig import AgentYAMLFactory
from src.novel_swarms.config.WorldConfig import WorldYAMLFactory
from src.novel_swarms.behavior import *
from src.novel_swarms.util.processing.multicoreprocessing import MultiWorldSimulation
from src.novel_swarms.agent.control.HomogeneousController import HomogeneousController
from src.novel_swarms.world.initialization.NGonInit import NGonInitialization
from src.novel_swarms.world.simulate import Simulation

SCALE = 10
MAX_TIME_LIMIT = 10000

def stop_when_all_subs_below_manifold(world):
    if world.total_steps < 100:
        return False

    pop_below = []
    for sub_population in world.behavior[1].sub_populations:
        pop_below.append(world.meta["fov"] <= (360 / len(sub_population)))
    # Return True only if ALL subpops are below/on the manifold
    all_below = functools.reduce(lambda a, b: a and b, pop_below)
    if all_below:
        if "converged_time" not in world.meta:
            world.meta["converged_time"] = 0
        world.meta["converged_time"] += 1
    else:
        world.meta["converged_time"] = 0
    # print(world.meta["converged_time"])
    return world.meta["converged_time"] > 5000


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
    world.init_type = NGonInitialization(n_agents, radius=31, disturbance_stddev=0.0)
    world.init_type.reseed(seed)

    world.factor_zoom(zoom=SCALE)
    world.addAgentConfig(goal_agent)
    world.metadata = {'hash': hash(tuple([n_agents, fov_angle, w, v])), 'fov': fov_angle, 'n': n_agents, 'omega': w,
                      'v': v}

    # If a configured initialization was called, we assume that we want to find a solution fit
    # to that specific init, therefore, we only evaluate one world, with no attempt to generalize
    return world


def build_dataset():
    time_start = time.time()
    world_processor = MultiWorldSimulation(pool_size=24, single_step=False, with_gui=False)
    exp = Experiment("../out", "subswarm")
    o = exp.add_sub("sweep")

    data = []
    for dt in range(4, 14, 2):
        n = 16
        # Just simulate elements below the 2pi/N manifold
        phi_above_manifold = list(range(23, 40, 3))
        final_phi = list(filter(lambda x: x is not None, phi_above_manifold))

        for phi in final_phi:
            print(f"Running with {n} agents on phi values {phi}, dt={dt / 100}!")
            worlds = [gene_to_world(n, phi, w=30, v=1.0, horizon=MAX_TIME_LIMIT, seed=s, dt=(dt / 100)) for s in
                      range(20)]
            b_ret = world_processor.execute(worlds, world_stop_condition=stop_when_all_subs_below_manifold)
            for w in b_ret:
                b_vec = w.getBehaviorVector()
                sub_b = w.behavior[1]
                class_data = [0, 0, 0]
                for i in sub_b.sub_swarm_classes:
                    class_data[i] += 1
                sub_b_data = class_data + [sum(class_data), max([len(r) for r in sub_b.sub_populations])]
                data.append([w.meta["n"]] + [w.meta["fov"]] + [w.meta["omega"]] + [w.meta["v"]] + [b_vec[0], b_vec[
                    2]] + sub_b_data + [w.total_steps, w.total_steps * w.population[0].dt])

            df = pd.DataFrame(data)
            df.columns = ["n", "fov", "omega", "v", "conn_components", "radius", "no_c", "no_b", "no_a",
                          "subswarms", "max_sub_pop", "timesteps", "time"]
            df.to_csv(os.path.join(o, "genes.csv"))
            print(f"Elapsed Time: f{time.time() - time_start}s")
    exp.write_metadata({})

if __name__ == "__main__":
    N, PHI = 20, 25
    OMEGA = 60  # FREEZE
    V = 3.33  # FREEZE
    GAMMA = 10  # FREEZE
    w = gene_to_world(N, PHI, OMEGA, V, GAMMA, 2000, seed=2, dt=0.01)
    sim = Simulation(w, show_gui=True, stop_detection=None)

    b = np.zeros(len(w.behavior))
    behavior_names = [b.name for b in w.behavior]
    assert len(b) == len(behavior_names)

    print(f"World Width: {sim.world.bounded_width}, World Height: {sim.world.bounded_height}")

    # Interactive Plotting Mode
    plt.ioff()
    b_history = np.array([b])
    while sim.running:
        r = sim.step()
        b_history = np.concatenate((b_history, [sim.world.getBehaviorVector()]), axis=0)
        if r is not None:
            break

    print("Plotting!")
    fig, ax = plt.subplots(len(sim.world.getBehaviorVector()), 1, figsize=(8, 10))
    fig.tight_layout(pad=1.5)
    for i in range(len(ax)):
        ax[i].clear()
        ax[i].set_title(behavior_names[i])
        if len(b_history) > 0:
            ax[i].plot(range(len(b_history) - 1), b_history[1:, i])

    plt.show(block=True)
    pygame.quit()

