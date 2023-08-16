"""
Find the best Levy Agents
"""

import argparse
from src.novel_swarms.optim.CMAES import CMAES
from src.novel_swarms.optim.OptimVar import CMAESVarSet
from src.novel_swarms.results.Experiment import Experiment
from src.novel_swarms.config.AgentConfig import AgentYAMLFactory
from src.novel_swarms.config.WorldConfig import WorldYAMLFactory
from src.novel_swarms.world.initialization.FixedInit import FixedInitialization
from src.novel_swarms.behavior import *

DECISION_VARS = CMAESVarSet(
    {
        "forward_rate": [0, 1],
        "turning_rate": [-1.5, 1.5],
    }
)

PERFECT_SCORE = -1.0
def FITNESS(world_set):
    total = 0
    for w in world_set:
        total -= w.behavior[0].out_average()[1]
    avg = total / len(world_set)
    return avg

def get_world_generator(n_agents, horizon, init=None, walls=True):
    def gene_to_world(genome, hash_val):
        SCALE = 10
        levy_agent = AgentYAMLFactory.from_yaml("demo/configs/flockbots-icra/levy.yaml")
        levy_agent.seed = 0
        levy_agent.forward_rate = genome[0]
        levy_agent.turning_rate = genome[1]
        levy_agent.rescale(SCALE)

        world = WorldYAMLFactory.from_yaml("demo/configs/flockbots-icra/world.yaml")
        world.seed = 0
        world.behavior = [
            AgentsAtGoal(as_percent=True, history=1),
            PercentageAtGoal(0.5),
            PercentageAtGoal(0.8),
            PercentageAtGoal(1.0)
        ]
        world.population_size = n_agents
        world.stop_at = horizon
        if init is not None:
            world.init_type = init

        if not walls:
            world.collide_walls = False
            world.show_walls = False
            world.detectable_walls = False
        else:
            world.detectable_walls = True

        world.factor_zoom(zoom=SCALE)
        world.addAgentConfig(levy_agent)
        world.metadata = {'hash': hash(tuple(list(hash_val)))}

        # If a configured initialization was called, we assume that we want to find a solution fit
        # to that specific init, therefore, we only evaluate one world, with no attempt to generalize
        worlds = []
        if init is not None:
            worlds = [world]

        # Otherwise, we'll attempt to find a general solution, invariant to starting position.
        else:
            for seed in range(3):
                world_config = world.getDeepCopy()
                world_config.seed = seed
                world_config.init_type.reseed(seed)
                world_config.behavior = [
                    AgentsAtGoal(as_percent=True, history=1),
                    PercentageAtGoal(0.5),
                    PercentageAtGoal(0.8),
                    PercentageAtGoal(1.0)
                ]
                worlds.append(world_config)

        return worlds

    return gene_to_world



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--name", type=str, help="Name of the experiment", default=None)
    parser.add_argument("--root", type=str, help="Experiment folder root", default=None)
    parser.add_argument("--fixed-config", action="store_true", help="Use the predefined init")
    parser.add_argument("--n", type=int, default=10, help="Number of agents")
    parser.add_argument("--t", type=int, default=1000, help="Environment Horizon")
    parser.add_argument("--processes", type=int, default=1, help="Number of running concurrent processes")
    parser.add_argument("--iters", type=int, default=None, help="Number of Evolutions to consider")
    parser.add_argument("--pop-size", type=int, default=15, help="The size of each generation's population")
    parser.add_argument("--no-walls", action="store_true", help="Whether to include detectable walls")
    parser.add_argument("--sweep", action="store_true", help="Whether to sweep instead of search")

    args = parser.parse_args()

    exp = Experiment(root="demo/results/out" if not args.root else args.root, title=args.name)

    # Fix the initial conditions if params indicate
    init = None
    if args.fixed_config:
        init = FixedInitialization("demo/configs/flockbots-icra/init_translated.csv")

    # Save World Config by sampling from generator
    world_gen_example = get_world_generator(-1, -1, init=init, walls=(not args.no_walls))
    sample_worlds = world_gen_example([-1, -1, -1, -1], [-1, -1, -1, -1])
    sample_worlds[0].save_yaml(exp)

    cmaes = CMAES(
        FITNESS,
        genome_to_world=get_world_generator(args.n, args.t, init=init, walls=(not args.no_walls)),
        dvars=DECISION_VARS,
        num_processes=args.processes,
        show_each_step=False,
        target=PERFECT_SCORE,
        experiment=exp,
        max_iters=args.iters,
        pop_size=args.pop_size,
    )
    if args.sweep:
        cmaes.sweep_parameters([20, 20])
    else:
        cmaes.minimize()
