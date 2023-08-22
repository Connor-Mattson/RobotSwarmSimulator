import os
import time
import inspect
import cma
import yaml
import numpy as np
from .OptimVar import CMAESVarSet
from ..util.processing.multicoreprocessing import MultiWorldSimulation
from ..world.simulate import main as sim
from ..results.Experiment import Experiment
from dataclasses import make_dataclass
import pandas as pd


class CMAES:
    def __init__(self,
                 f=None,
                 genome_to_world=None,
                 dvars=None,
                 pop_size=10,
                 max_iters=None,
                 target=0.0,
                 num_processes=1,
                 stop_detection_method=None,
                 show_each_step=False,
                 experiment=None):
        genome_size = len(dvars)
        self.f = f
        self.g_to_w = genome_to_world
        self.x0 = [0.5 for _ in range(genome_size)]
        self.s0 = 0.20
        self.pop = pop_size
        self.bounds = [[0.0 for _ in range(genome_size)], [1.0 for _ in range(genome_size)]]
        self.target = target
        self.n_processes = num_processes
        self.w_stop_method = stop_detection_method
        self.solution_set = {}
        self.show_steps = show_each_step
        self.dvars = dvars
        self.experiment = experiment
        self.max_iters = max_iters
        self.generation = 0

        # Data collection
        if self.experiment is not None:
            dvar_repr = [(f"p_{i}" if self.dvars is None else self.dvars.names[i], float) for i in range(len(self.x0))]
            b_names = self.behavior_names()
            b_repr = [(b_name, float) for b_name in b_names]
            self.hist_point = make_dataclass(
                "CMAESPoint",
                [("gen", int), ("pop", int), ("fitness", float)] + dvar_repr + b_repr
             )
            self.history = []
            self.exp_path = self.experiment.add_sub("CMAES")
            with open(os.path.join(self.exp_path, "optim-config.yaml"), "w") as out_f:
                yaml.dump(self.parameters_dict(), out_f, default_flow_style=False)



    def minimize(self):
        opts = {'seed': 1, 'popsize': self.pop, 'bounds': self.bounds, 'ftarget': self.target, "tolfun": 0, "tolflatfitness": 50, "tolfunhist": 0}
        es = cma.CMAEvolutionStrategy(self.x0, self.s0, opts)
        while not es.stop():
            try:
                solutions = self.ask_for_genomes(es)
                es.tell(solutions, [self.pull_from_solution_set(s) for s in solutions])
                es.disp()
                self.generation += 1
                if self.show_steps:
                    sim(world_config=self.g_to_w(self.dvars.from_normalized_to_scaled(es.best.x), es.best.x)[0], show_gui=True, stop_detection=self.w_stop_method,
                        step_size=10)
                if self.max_iters and self.generation > self.max_iters:
                    break
            except KeyboardInterrupt:
                break

        if self.experiment is not None:
            df = pd.DataFrame(self.history)
            df.to_csv(os.path.join(self.exp_path, "genomes.csv"), index=False)

        es.result_pretty()
        return es.result, es

    def sweep_parameters(self, divisions: list[int]):
        if len(divisions) != len(self.x0):
            raise Exception(f"Divisions should be of size {len(self.x0)}. Not {len(divisions)}")
        spaces = []
        for i, d in enumerate(divisions):
            spaces.append(np.linspace(0, 1, d))
        grid = np.meshgrid(*spaces)
        points = np.array(grid).reshape((len(divisions), -1)).T
        parameters = [self.dvars.from_normalized_to_scaled(p) for p in points]
        processor = MultiWorldSimulation(pool_size=self.n_processes, single_step=False, with_gui=False)

        configs = [self.g_to_w(parameters[i], parameters[i]) for i in range(len(parameters))]
        ret = processor.execute(configs, world_stop_condition=self.w_stop_method, batched=True)

        for i, world_set in enumerate(ret):
            _key = world_set[0].meta["hash"]
            fitness = self.f(world_set)
            behavior = self.average_behaviors(world_set)
            self.solution_set[_key] = fitness
            if self.experiment is not None:
                self.history.append(self.hist_point(self.generation, i, fitness, *parameters[i], *behavior))

        if self.experiment is not None:
            df = pd.DataFrame(self.history)
            df.to_csv(os.path.join(self.exp_path, "genomes.csv"), index=False)

    def ask_for_genomes(self, es):
        parameters = es.ask()
        out = parameters
        if self.dvars:
            parameters = [self.dvars.from_normalized_to_scaled(p) for p in parameters]
        configs = [self.g_to_w(parameters[i], out[i]) for i in range(len(parameters))]
        processor = MultiWorldSimulation(pool_size=self.n_processes, single_step=False, with_gui=False)

        batched_worlds = isinstance(configs[0], list)

        # Blocking MultiProcess Execution
        ret = processor.execute(configs, world_stop_condition=self.w_stop_method, batched=batched_worlds)
        for i, world_set in enumerate(ret):
            _key = world_set[0].meta["hash"] if batched_worlds else world_set.meta["hash"]
            fitness = self.f(world_set)
            behavior = self.average_behaviors(world_set)
            self.solution_set[_key] = fitness
            if self.experiment is not None:
                self.history.append(self.hist_point(self.generation, i, fitness, *parameters[i], *behavior))

        return out
    def pull_from_solution_set(self, x):
        fetch_key = hash(tuple(list(x)))
        retrieval = None
        if fetch_key in self.solution_set:
            retrieval = self.solution_set[fetch_key]

        if retrieval is None:
            wc = self.g_to_w(x)
            world = sim(wc, show_gui=True, stop_detection=self.w_stop_method, step_size=10)
            return self.f(world)
        else:
            return retrieval

    def average_behaviors(self, world_set):
        behaviors = np.zeros(len(world_set[0].behavior), dtype=float)
        for world in world_set:
            behaviors += np.array([world.behavior[i].out_average()[1] for i in range(len(world.behavior))])
        return behaviors / len(world_set)

    def behavior_names(self):
        # Extract a random world
        world_set = self.g_to_w(self.x0, self.x0)
        if isinstance(world_set, list):
            world = world_set[0]
        else:
            world = world_set
        behavior_names = [world.behavior[i].name for i in range(len(world.behavior))]
        return behavior_names

    def parameters_dict(self):
        return {
            "fitness_func": inspect.getsource(self.f).split('\n'),
            "initial_genome": self.x0,
            "initial_sigma": self.s0,
            "population_size": self.pop,
            "bounds": self.bounds,
            "target": self.target,
            "n_processes": self.n_processes,
            "w_stop_method": inspect.getsource(self.w_stop_method).split('\n') if self.w_stop_method is not None else None,
            "show_steps": self.show_steps,
            "dvars": self.dvars.as_dict() if self.dvars else None
        }


def example_A():
    """
    Example: Find a Cyclic Pursuit Controller (A Controller where radial variance => 0)
    """

    def fitness(world_set):
        total = 0
        for w in world_set:
            total += w.behavior[2].out_average()[1]
        return total / len(world_set)

    def get_world(genome, hash_val):
        from ..behavior.AngularMomentum import AngularMomentumBehavior
        from ..behavior.AverageSpeed import AverageSpeedBehavior
        from ..behavior.GroupRotationBehavior import GroupRotationBehavior
        from ..behavior.RadialVariance import RadialVarianceBehavior
        from ..behavior.ScatterBehavior import ScatterBehavior
        from ..sensors.BinaryLOSSensor import BinaryLOSSensor
        from ..sensors.SensorSet import SensorSet
        from ..config.AgentConfig import DiffDriveAgentConfig
        from ..config.WorldConfig import RectangularWorldConfig

        controller = genome
        sensors = SensorSet([
            BinaryLOSSensor(angle=0),
        ])
        agent_config = DiffDriveAgentConfig(
            controller=controller,
            sensors=sensors,
            seed=1,
        )
        behavior = [
            AverageSpeedBehavior(),
            AngularMomentumBehavior(),
            RadialVarianceBehavior(),
            ScatterBehavior(),
            GroupRotationBehavior(),
        ]

        world_config = RectangularWorldConfig(
            size=(500, 500),
            n_agents=15,
            seed=1,
            behavior=behavior,
            agentConfig=agent_config,
            padding=15,
            stop_at=1000,
            metadata={'hash': hash(tuple(list(hash_val)))}
        )
        return [world_config]

    experiment = Experiment(root="demo/results/out", title="CMAES-test-A")
    sample_worlds = get_world([-1, -1, -1, -1], [-1, -1, -1, -1])
    sample_worlds[0].save_yaml(experiment)

    decision_vars = {
        "v0_l": [-1.5, 1.5],
        "v0_r": [-1.5, 1.5],
        "v1_l": [-1.5, 1.5],
        "v1_r": [-1.5, 1.5],
    }
    dvars = CMAESVarSet(decision_vars)

    bounds = [[0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0]]
    optim = CMAES(f=fitness, genome_to_world=get_world, init_sigma=0.5, init_genome=[0.0, 0.0, 0.0, 0.0], pop_size=20,
                  num_processes=12, bounds=bounds, target=0.001, dvars=dvars, experiment=experiment)
    c, _ = optim.minimize()
    return c


def example_B():
    """
    To allow for double summations, you can batch process worlds for one genome. In this example, we seek to find a cyclic pursuit controller that
    is minimized over 10 different seeds.
    """

    def fitness(world_set):
        total = 0
        for w in world_set:
            total += w.behavior[2].out_average()[1]
        return total / len(world_set)

    def get_world(genome, hash_val):
        from ..behavior.AngularMomentum import AngularMomentumBehavior
        from ..behavior.AverageSpeed import AverageSpeedBehavior
        from ..behavior.GroupRotationBehavior import GroupRotationBehavior
        from ..behavior.RadialVariance import RadialVarianceBehavior
        from ..behavior.ScatterBehavior import ScatterBehavior
        from ..sensors.BinaryLOSSensor import BinaryLOSSensor
        from ..sensors.SensorSet import SensorSet
        from ..config.AgentConfig import DiffDriveAgentConfig
        from ..config.WorldConfig import RectangularWorldConfig

        worlds = []
        for seed in range(10):
            controller = genome
            sensors = SensorSet([
                BinaryLOSSensor(angle=0),
            ])
            agent_config = DiffDriveAgentConfig(
                controller=controller,
                sensors=sensors,
                seed=seed,
            )
            behavior = [
                AverageSpeedBehavior(),
                AngularMomentumBehavior(),
                RadialVarianceBehavior(),
                ScatterBehavior(),
                GroupRotationBehavior(),
            ]

            world_config = RectangularWorldConfig(
                size=(500, 500),
                n_agents=15,
                seed=1,
                behavior=behavior,
                agentConfig=agent_config,
                padding=15,
                stop_at=1000,
                metadata={'hash': hash(tuple(list(hash_val)))}
            )
            worlds.append(world_config)
        return worlds


    experiment = Experiment(root="demo/results/out", title="CMAES-test-B")

    decision_vars = {
        "v0_l": [-1.5, 1.5],
        "v0_r": [-1.5, 1.5],
        "v1_l": [-1.5, 1.5],
        "v1_r": [-1.5, 1.5],
    }
    dvars = CMAESVarSet(decision_vars)

    bounds = [[-1.0, -1.0, -1.0, -1.0], [1.0, 1.0, 1.0, 1.0]]
    optim = CMAES(f=fitness, genome_to_world=get_world, pop_size=20,
                  num_processes=12, bounds=bounds, target=0.001, experiment=experiment, dvars=dvars)
    c, _ = optim.minimize()
    return c


if __name__ == "__main__":
    print(example_B())
