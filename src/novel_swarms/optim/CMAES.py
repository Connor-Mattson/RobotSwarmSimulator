import cma
import numpy as np
from ..util.processing.multicoreprocessing import MultiWorldSimulation
from ..world.simulate import main as sim

class CMAES:
    def __init__(self,
                 f=None,
                 genome_to_world=None,
                 init_genome=None,
                 init_sigma=None,
                 pop_size=10,
                 bounds=None,
                 target=0.0,
                 num_processes=1,
                 stop_detection_method=None,
                 show_each_step=False,
                 sigma_vec = None):
        self.f = f
        self.g_to_w = genome_to_world
        self.x0 = init_genome
        self.s0 = init_sigma
        self.pop = pop_size
        self.bounds = bounds
        self.target = target
        self.n_processes = num_processes
        self.w_stop_method = stop_detection_method
        self.solution_set = {}
        self.show_steps = show_each_step
        self.sigma_vec = sigma_vec

    def minimize(self):
        opts = {'popsize': self.pop, 'bounds': self.bounds, 'ftarget': self.target, }
        es = cma.CMAEvolutionStrategy(self.x0, self.s0, opts)
        while not es.stop():
            solutions = self.ask_for_genomes(es)
            es.tell(solutions, [self.pull_from_solution_set(s) for s in solutions])
            es.disp()
            print(f"Current Best: {es.best.x}")
            if self.show_steps:
                sim(self.g_to_w(es.best.x)[0], show_gui=True, stop_detection=self.w_stop_method, step_size=10)

        es.result_pretty()
        return es.result, es

    def ask_for_genomes(self, es):
        parameters = es.ask()
        configs = [self.g_to_w(parameter) for parameter in parameters]
        processor = MultiWorldSimulation(pool_size=self.n_processes, single_step=False, with_gui=False)

        batched_worlds = isinstance(configs[0], list)

        # Blocking MultiProcess Execution
        ret = processor.execute(configs, world_stop_condition=self.w_stop_method, batched=batched_worlds)
        for world in ret:
            _key = world[0].meta["hash"] if batched_worlds else world.meta["hash"]
            self.solution_set[_key] = self.f(world)

        return parameters

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

def example_A():
    """
    Example: Find a Cyclic Pursuit Controller (A Controller where radial variance => 0)
    """
    def fitness(world):
        return world.behavior[2].out_average()[1]

    def get_world(genome):
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
            metadata={'hash': hash(tuple(list(genome)))}
        )
        return [world_config]

    bounds = [[-1.0, -1.0, -1.0, -1.0], [1.0, 1.0, 1.0, 1.0]]
    optim = CMAES(f=fitness, genome_to_world=get_world, init_sigma=0.5, init_genome=[0.0, 0.0, 0.0, 0.0], pop_size=20, num_processes=12, bounds=bounds, target=0.001)
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

    def get_world(genome):
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
                metadata={'hash': hash(tuple(list(genome)))}
            )
            worlds.append(world_config)
        return worlds

    bounds = [[-1.0, -1.0, -1.0, -1.0], [1.0, 1.0, 1.0, 1.0]]
    optim = CMAES(f=fitness, genome_to_world=get_world, init_sigma=0.25, init_genome=[0.0, 0.0, 0.0, 0.0], pop_size=20, num_processes=12, bounds=bounds, target=0.001)
    c, _ = optim.minimize()
    return c

if __name__ == "__main__":
    print(example_B())
