"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

Connor Mattson
University of Utah
September 2022
"""
from src.config.defaults import ConfigurationDefaults
from src.novelty.GeneRule import GeneRule
from src.novelty.evolve import main as evolve
from src.results.results import main as report
from src.behavior.AngularMomentum import AngularMomentumBehavior
from src.behavior.AverageSpeed import AverageSpeedBehavior
from src.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.behavior.RadialVariance import RadialVarianceBehavior
from src.behavior.ScatterBehavior import ScatterBehavior
from src.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.sensors.SensorSet import SensorSet
from src.config.AgentConfig import DiffDriveAgentConfig
from src.config.WorldConfig import RectangularWorldConfig
from src.config.EvolutionaryConfig import GeneticEvolutionConfig

if __name__ == "__main__":

    SEED = None

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
    ])

    agent_config = DiffDriveAgentConfig(
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
        size=(500, 500),
        n_agents=30,
        seed=SEED,
        behavior=phenotype,
        agentConfig=agent_config,
        padding=15
    )

    novelty_config = GeneticEvolutionConfig(
        gene_rules=genotype,
        phenotype_config=phenotype,
        n_generations=10,
        n_population=10,
        crossover_rate=0.7,
        mutation_rate=0.15,
        world_config=world_config,
        k_nn=8,
        simulation_lifespan=3,
        display_novelty=False,
        save_archive=False,
    )

    # Novelty Search through Genetic Evolution
    archive = evolve(config=novelty_config)

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world_config
    results_config.archive = archive

    # Take Results from Evolution, reduce dimensionality, and present User with Clusters.
    report(config=results_config)
