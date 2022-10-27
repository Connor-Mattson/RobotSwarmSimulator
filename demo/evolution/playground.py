"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

Connor Mattson
University of Utah
September 2022
"""
from novel_swarms.config.defaults import ConfigurationDefaults
from novel_swarms.novelty.GeneRule import GeneRule
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
        # BinaryLOSSensor(angle=0),
        BinaryFOVSensor(theta=14 / 2, distance=(10 * 13.25), degrees=True)
    ])

    agent_config = DiffDriveAgentConfig(
        agent_radius=5,
        wheel_radius=(10 * 0.44),
        sensors=sensors,
        seed=SEED,
    )

    genotype = [
        GeneRule(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=4),
        GeneRule(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=4),
        GeneRule(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=4),
        GeneRule(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=4),
    ]

    phenotype = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    world_config = RectangularWorldConfig(
        size=(315, 315),
        n_agents=9,
        seed=SEED,
        behavior=phenotype,
        agentConfig=agent_config,
        padding=15
    )

    novelty_config = GeneticEvolutionConfig(
        gene_rules=genotype,
        phenotype_config=phenotype,
        n_generations=100,
        n_population=100,
        crossover_rate=0.7,
        mutation_rate=0.15,
        world_config=world_config,
        k_nn=15,
        simulation_lifespan=600,
        display_novelty=True,
        save_archive=True,
        show_gui=True,
        save_every=1
    )

    # Novelty Search through Genetic Evolution
    archive = evolve(config=novelty_config)

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world_config
    results_config.archive = archive

    # Take Results from Evolution, reduce dimensionality, and present User with Clusters.
    report(config=results_config)
