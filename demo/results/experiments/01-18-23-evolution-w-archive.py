import pygame
from src.novel_swarms.config.OutputTensorConfig import OutputTensorConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.novelty.GeneRule import GeneRule, GeneBuilder, GeneRuleContinuous
from src.novel_swarms.novelty.evolve import main as evolve
from src.novel_swarms.results.results import main as report
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.config.EvolutionaryConfig import GeneticEvolutionConfig

if __name__ == "__main__":

    SEED = None

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
        # BinaryLOSSensor(angle=45),
        # BinaryLOSSensor(angle=45)
        # BinaryFOVSensor(theta=14 / 2, distance=(20 * 13.25), degrees=True)
    ])

    agent_config = ConfigurationDefaults.DIFF_DRIVE_AGENT

    genotype = GeneBuilder(
        heuristic_validation=True,
        round_to_digits=1,
        rules=[
            GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
            GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
            GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
            GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
        ]
    )

    phenotype = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=24,
        seed=SEED,
        behavior=phenotype,
        agentConfig=agent_config,
        padding=15
    )

    pygame.init()
    pygame.display.set_caption("Evolutionary Novelty Search")
    screen = pygame.display.set_mode((world_config.w, world_config.h))

    output_config = OutputTensorConfig(
        timeless=True,
        total_frames=80,
        steps_between_frames=2,
        screen=screen
    )

    # Original Experiment was 50 gens, 50 pop
    novelty_config = GeneticEvolutionConfig(
        gene_builder=genotype,
        phenotype_config=phenotype,
        n_generations=50,
        n_population=50,
        crossover_rate=0.7,
        mutation_rate=0.15,
        world_config=world_config,
        k_nn=15,
        simulation_lifespan=1200,
        display_novelty=False,
        save_archive=True,
        show_gui=False,
        mutation_flip_chance=0.2,
        use_external_archive=True,
        # save_every=1
    )

    # Novelty Search through Genetic Evolution
    archive = evolve(config=novelty_config, output_config=output_config)

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world_config
    results_config.archive = archive

    print(archive.genotypes)

    # Take Results from Evolution, reduce dimensionality, and present User with Clusters.
    report(config=results_config)
