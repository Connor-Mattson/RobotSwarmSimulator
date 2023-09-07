from src.novel_swarms.agent.control.HomogeneousController import HomogeneousController
from src.novel_swarms.config.EvolutionaryConfig import GeneticEvolutionConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.novelty.GeneRule import GeneBuilder, GeneRule
from src.novel_swarms.results.Experiment import Experiment
from src.novel_swarms.config.AgentConfig import AgentYAMLFactory
from src.novel_swarms.config.WorldConfig import WorldYAMLFactory
from src.novel_swarms.world.initialization.FixedInit import FixedInitialization
from src.novel_swarms.novelty.multi_evolve import multi_evolve
from src.novel_swarms.novelty.evolve import main as single_thread_evolve
from src.novel_swarms.results.results import main as report
from src.novel_swarms.behavior import *
from src.novel_swarms.behavior.AlgebraicConnectivity import AlgebraicConn
from src.novel_swarms.world.simulate import main as sim

FIXED_START_FILE = "../../../demo/configs/flockbots-icra/init_translated.csv"
T, N = 3000, 13
GEN, POP = 100, 100

if __name__ == "__main__":

    FLOCKBOT_CONTROL_PARAMETERS = GeneBuilder(
        round_to_digits=None,
        rules=[
            GeneRule(discrete_domain=[i for i in range(0, 11, 1)], step_size=4, allow_mutation=True),
            GeneRule(discrete_domain=[i / 10 for i in range(-15, 16, 1)], step_size=4, allow_mutation=True),
            GeneRule(discrete_domain=[i for i in range(0, 11, 1)], step_size=4, allow_mutation=True),
            GeneRule(discrete_domain=[i / 10 for i in range(-15, 16, 1)], step_size=4, allow_mutation=True),
        ]
    )

    flockbot = AgentYAMLFactory.from_yaml("../../../demo/configs/flockbots-ns/flockbot.yaml")
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

    # world.agentConfig.controller = [10.0, -0.5, 10.0, 0.5]
    # sim(world)

    novelty_config = GeneticEvolutionConfig(
        gene_builder=FLOCKBOT_CONTROL_PARAMETERS,
        phenotype_config=world.behavior,
        n_generations=GEN,
        n_population=POP,
        crossover_rate=0.7,
        mutation_rate=0.15,
        world_config=world,
        k_nn=15,
        simulation_lifespan=T,
        display_novelty=False,
        save_archive=True,
        show_gui=True
    )

    archive = multi_evolve(novelty_config)
    # archive = single_thread_evolve(novelty_config)

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world
    results_config.archive = archive

    # Take Results from Evolution, reduce dimensionality, and present User with Clusters.
    report(config=results_config)

