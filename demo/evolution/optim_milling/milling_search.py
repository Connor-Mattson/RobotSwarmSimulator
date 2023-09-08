"""
Find the best Homogeneous Agents
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
        "forward_rate_0": [0, 1 * SCALE],  # Body Lengths / second, will be converted to pixel values during search
        "turning_rate_0": [-1.5, 1.5],  # Radians / second
        "forward_rate_1": [0, 1 * SCALE],  # Body Lengths / second, will be converted to pixel values during search
        "turning_rate_1": [-1.5, 1.5],  # Radians / second
    }
)

PERFECT_CIRCLE_SCORE = 0.0
def FITNESS(world_set):
    total = 0
    for w in world_set:
        total += w.behavior[0].out_average()[1]
    avg = total / len(world_set)
    return avg

def get_world_generator(n_agents, horizon):

    def gene_to_world(genome, hash_val):

        goal_agent = AgentYAMLFactory.from_yaml("demo/configs/flockbots-icra-milling/flockbot.yaml")
        goal_agent.controller = HomogeneousController(genome)
        goal_agent.seed = 0
        goal_agent.rescale(SCALE)

        world = WorldYAMLFactory.from_yaml("demo/configs/flockbots-icra-milling/world.yaml")
        world.seed = 0
        world.behavior = [
            # RadialVarianceBehavior(history=1),
            RadialVarianceBehavior(history=20)
        ]
        world.population_size = n_agents
        world.stop_at = horizon
        world.detectable_walls = True

        world.factor_zoom(zoom=SCALE)
        world.addAgentConfig(goal_agent)
        world.metadata = {'hash': hash(tuple(list(hash_val)))}
        worlds = [world]

        return worlds

    return gene_to_world

def stop_detection_method(world):
    if world.total_steps > 100 and world.behavior[0].out_average()[1] < 0.00002:
        return True
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--name", type=str, help="Name of the experiment", default=None)
    parser.add_argument("--root", type=str, help="Experiment folder root", default=None)
    parser.add_argument("--n", type=int, default=10, help="Number of agents")
    parser.add_argument("--t", type=int, default=1000, help="Environment Horizon")
    parser.add_argument("--processes", type=int, default=1, help="Number of running concurrent processes")
    parser.add_argument("--iters", type=int, default=None, help="Number of Evolutions to consider")
    parser.add_argument("--pop-size", type=int, default=15, help="The size of each generation's population")
    parser.add_argument("--sweep", action="store_true", help="Whether to sweep instead of search")

    args = parser.parse_args()

    exp = Experiment(root="demo/results/out" if not args.root else args.root, title=args.name)

    # Fix the initial conditions if params indicate
    # init = None
    # if args.fixed_config:
    #     init = FixedInitialization("demo/configs/flockbots-icra/init_translated.csv")

    # Save World Config by sampling from generator
    world_gen_example = get_world_generator(args.n, args.t)
    sample_worlds = world_gen_example([-1, -1, -1, -1], [-1, -1, -1, -1])
    sample_worlds[0].stop_at = None
    # sim(world_config=sample_worlds[0], save_every_ith_frame=8, save_duration=4000)

    sample_worlds[0].save_yaml(exp)

    cmaes = CMAES(
        FITNESS,
        genome_to_world=get_world_generator(args.n, args.t),
        dvars=DECISION_VARS,
        num_processes=args.processes,
        show_each_step=True,
        target=PERFECT_CIRCLE_SCORE,
        experiment=exp,
        max_iters=args.iters,
        pop_size=args.pop_size,
        stop_detection_method=stop_detection_method
    )
    if args.sweep:
        cmaes.sweep_parameters([7, 7, 7, 7])
    else:
        cmaes.minimize()
