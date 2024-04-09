"""
Find the best Homogeneous Agents for Milling
"""
import numpy as np
import argparse
from src.novel_swarms.optim.CMAES import CMAES
from src.novel_swarms.optim.OptimVar import CMAESVarSet
from src.novel_swarms.results.Experiment import Experiment
from src.novel_swarms.config.AgentConfig import AgentYAMLFactory
from src.novel_swarms.config.WorldConfig import WorldYAMLFactory
from src.novel_swarms.world.initialization.FixedInit import FixedInitialization
from src.novel_swarms.behavior import *
from src.novel_swarms.agent.control.Controller import Controller
from src.novel_swarms.agent.control.HomogeneousController import HomogeneousController
from src.novel_swarms.world.simulate import main as sim

SCALE = 10

DECISION_VARS = CMAESVarSet(
    {
        "forward_rate_0": [-(1.33 * SCALE), 1.33 * SCALE],
        # Body Lengths / second, will be converted to pixel values during search
        "turning_rate_0": [-2.0, 2.0],  # Radians / second
        "forward_rate_1": [-(1.33 * SCALE), 1.33 * SCALE],
        # Body Lengths / second, will be converted to pixel values during search
        "turning_rate_1": [-2.0, 2.0],  # Radians / second
    }
)

PERFECT_CIRCLE_SCORE = -1.0
CIRCLINESS_HISTORY = 450


def FITNESS(world_set):
    total = 0
    for w in world_set:
        total += w.behavior[0].out_average()[1]
    avg = total / len(world_set)
    return -avg


def get_world_generator(n_agents, horizon):
    def gene_to_world(genome, hash_val, reseed=0):
        goal_agent = AgentYAMLFactory.from_yaml("demo/configs/flockbots-icra-milling/flockbot.yaml")
        goal_agent.controller = HomogeneousController(genome)
        goal_agent.seed = 0
        goal_agent.rescale(SCALE)

        world = WorldYAMLFactory.from_yaml("demo/configs/flockbots-icra-milling/world.yaml")
        world.seed = 0
        world.behavior = [
            Circliness(avg_history_max=CIRCLINESS_HISTORY)
        ]
        world.population_size = n_agents
        world.stop_at = horizon
        world.detectable_walls = False
        # Change the initialization seed
        world.init_type.reseed(reseed)


        world.factor_zoom(zoom=SCALE)
        world.addAgentConfig(goal_agent)
        world.metadata = {'hash': hash(tuple(list(hash_val)))}
        worlds = [world]

        return worlds

    return gene_to_world


def m_per_s_to_pixels_per_second(genome):
    genome[0] *= (100 / 15) * SCALE
    genome[2] *= (100 / 15) * SCALE
    return genome


if __name__ == "__main__":
    """
    Example usage:
    `python -m demo.evolution.optim_milling.sim_results --v0 0.1531 --w0 0.3439 --v1 0.1485 --w1 0.1031 --n 10 --t 1000`
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--n", type=int, default=10, help="Number of agents")
    parser.add_argument("--t", type=int, default=1000, help="Environment Horizon")
    parser.add_argument("--v0", type=float, help="Forward_Speed_0", default=None)
    parser.add_argument("--w0", type=float, help="Turning_Rate_0", default=None)
    parser.add_argument("--v1", type=float, help="Forward_Speed_1", default=None)
    parser.add_argument("--w1", type=float, help="Turning_Rate_1", default=None)
    parser.add_argument("--no-stop", action="store_true", help="Whether to stop at T limit or not")

    args = parser.parse_args()

    # Save World Config by sampling from generator
    world_gen_example = get_world_generator(args.n, args.t)

    translated_genome = m_per_s_to_pixels_per_second([args.v0, args.w0, args.v1, args.w1])

    values = []
    for i in range(1000):
        sample_worlds = world_gen_example(translated_genome, [-1, -1, -1, -1], reseed=i)

        if args.no_stop:
            sample_worlds[0].stop_at = None
        else:
            sample_worlds[0].stop_at = args.t

        w = sim(world_config=sample_worlds[0], save_every_ith_frame=2, save_duration=1000, show_gui=False)
        try:
            b = w.behavior[0].out_average()[1]
            values.append(b)
            print(f"Final Circliness for seed {i}: {b}")
        except:
            pass

    print(values)

    import matplotlib.pyplot as plt
    plt.hist(values)
    plt.title("Distribution of Scores running best controller over 1000 different starting seeds")
    plt.xlabel("Circliness (lambda)")
    plt.ylabel("Number of Samples")
    plt.show()

