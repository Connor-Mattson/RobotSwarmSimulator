import pygame
import math
from novel_swarms.config.OutputTensorConfig import OutputTensorConfig
from novel_swarms.config.defaults import ConfigurationDefaults
from novel_swarms.novelty.GeneRule import GeneRule, GeneBuilder, GeneRuleContinuous
from novel_swarms.novelty.evolve import main as evolve
from novel_swarms.results.results import main as report
from novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig
from novel_swarms.config.EvolutionaryConfig import GeneticEvolutionConfig

if __name__ == "__main__":

    SEED = None

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
        BinaryLOSSensor(angle=(math.pi / 3)),
        # BinaryLOSSensor(angle=45),
        # BinaryLOSSensor(angle=45)
        # BinaryFOVSensor(theta=14 / 2, distance=(20 * 13.25), degrees=True)
    ])

    agent_config = ConfigurationDefaults.DIFF_DRIVE_AGENT
    agent_config.sensors = sensors

    genotype = GeneBuilder(
        heuristic_validation=False,
        round_to_digits=1,
        rules=[
            GeneRuleContinuous(_max=0.5, _min=0.5, mutation_step=0.4, round_digits=1, allow_mutation=False),
            GeneRuleContinuous(_max=0.9, _min=0.9, mutation_step=0.4, round_digits=1, allow_mutation=False),
            GeneRuleContinuous(_max=1.0, _min=1.0, mutation_step=0.4, round_digits=1, allow_mutation=False),
            GeneRuleContinuous(_max=1.0, _min=1.0, mutation_step=0.4, round_digits=1, allow_mutation=False),
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
        n_generations=30,
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
        use_external_archive=False,
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
