from src.novel_swarms.agent.control.HomogeneousController import HomogeneousController
from src.novel_swarms.config.EvolutionaryConfig import GeneticEvolutionConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.novelty.GeneRule import GeneBuilder, GeneRule
from src.novel_swarms.novelty.NoveltyArchive import NoveltyArchive
from src.novel_swarms.results.Experiment import Experiment
from src.novel_swarms.config.AgentConfig import AgentYAMLFactory
from src.novel_swarms.config.WorldConfig import WorldYAMLFactory
from src.novel_swarms.util.processing.multicoreprocessing import MultiWorldSimulation
from src.novel_swarms.world.initialization.FixedInit import FixedInitialization
from src.novel_swarms.novelty.multi_evolve import multi_evolve
from src.novel_swarms.novelty.evolve import main as single_thread_evolve
from src.novel_swarms.results.results import main as report
from src.novel_swarms.behavior import *
from src.novel_swarms.behavior.AlgebraicConnectivity import AlgebraicConn
from src.novel_swarms.world.simulate import main as sim
import numpy as np

FIXED_START_FILE = "../../../demo/configs/flockbots-icra/init_translated.csv"
T, N = 3000, 13
GEN, POP = 100, 100

if __name__ == "__main__":

    flockbot = AgentYAMLFactory.from_yaml("../../../demo/configs/flockbots-ns/flockbot.yaml")
    flockbot.sensors.sensors[0].false_positive = 0
    flockbot.sensors.sensors[0].false_negative = 0
    flockbot.seed = 0
    flockbot.rescale(10)

    world = WorldYAMLFactory.from_yaml("../../../demo/configs/flockbots-ns/world.yaml")
    world.seed = 0
    world.behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
        AlgebraicConn(history=1, r_disk_size=160)
    ]

    world.population_size = N
    world.stop_at = T

    # print(world.init_type.positions)
    world.factor_zoom(zoom=10)
    world.addAgentConfig(flockbot)

    v_speeds = [i for i in range(1, 11, 1)]
    w_rates = [i / 10 for i in range(-15, 16, 2)]

    archive = NoveltyArchive()
    for v0 in v_speeds:
        for w0 in w_rates:
            for v1 in v_speeds:
                population_size = len(w_rates)
                behaviors = np.array([[-1.0 for j in range(len(world.behavior))] for i in range(population_size)])
                world_executables = []
                for i, w1 in enumerate(w_rates):
                    genome = [v0, w0, v1, w1]
                    config = world.getDeepCopy()
                    config.agentConfig = config.agentConfig.getDeepCopy()
                    config.agentConfig.controller = genome
                    config.agentConfig.attach_world_config(config)
                    config.metadata["key"] = i
                    config.metadata["genome"] = genome
                    world_executables.append(config)

                multi_sim = MultiWorldSimulation(pool_size=24)
                world_outs = multi_sim.execute(world_executables)

                for w in world_outs:
                    print(f"Returned data for world {w.meta['key']}: {w.getBehaviorVector()}")
                    behaviors[w.meta['key']] = w.getBehaviorVector()
                    archive.addToArchive(w.getBehaviorVector(), w.meta["genome"])

                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(f"Done with Set: [{v0}, {w0}, {v1}, x]")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    archive.saveArchive("sweep_out_b")
    archive.saveGenotypes("sweep_out_g")

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world
    results_config.archive = archive

    # Take Results from Evolution, reduce dimensionality, and present User with Clusters.
    report(config=results_config)

