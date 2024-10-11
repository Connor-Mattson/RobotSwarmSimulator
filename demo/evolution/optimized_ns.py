"""
An Optimized Version of Novelty Search that utilizes multi-threading
"""
from src.novel_swarms.config.AgentConfig import HeroRobotConfig
from src.novel_swarms.novelty.GeneRule import GeneRule, GeneRuleContinuous
from src.novel_swarms.novelty.optim_evolve import main as evolve
from src.novel_swarms.results.results import main as report
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.config.EvolutionaryConfig import GeneticEvolutionConfig
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.world.initialization.GridInit import GridInitialization
from src.novel_swarms.behavior import *
import os

if __name__ == "__main__":
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

    sensors = SensorSet([
        BinaryFOVSensor(theta=0.12, distance=100 * 3, show=False),
    ])

    agent_config = HeroRobotConfig(
        controller=None,
        sensors=sensors,
        trace_length=0,
        body_filled=True,
        dt=0.1,
    )

    # Create a Genotype Ruleset that matches the size and boundaries of your robot controller _max and _min represent
    # the maximum and minimum acceptable values for that index in the genome. mutation_step specifies the largest
    # possible step in any direction that the genome can experience during mutation.
    genotype = [
        GeneRuleContinuous(_max=27.0, _min=-27.0, mutation_step=3, round_digits=3, exclude=[[-15, 15]]),
        GeneRuleContinuous(_max=1.6, _min=-1.6, mutation_step=0.6, round_digits=3, exclude=[[-0.4, 0.4]]),
        GeneRuleContinuous(_max=27.0, _min=-27.0, mutation_step=3, round_digits=3, exclude=[[-15, 15]]),
        GeneRuleContinuous(_max=1.6, _min=-1.6, mutation_step=0.6, round_digits=3, exclude=[[-0.4, 0.4]]),
    ]

    # Use the default Behavior Vector (from Brown et al.) to measure the collective swarm behaviors
    phenotype = [
        AverageSpeedBehavior(normalization_constant=2.7),
        AngularMomentumBehavior(normalization_constant=2.7),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(normalization_constant=2.7),
    ]

    # Define an empty Rectangular World with size (w, h) and n agents.
    num_agents = 8
    world_config = RectangularWorldConfig(
        size=(171 * 3, 142 * 3),
        n_agents=num_agents,
        seed=0,
        behavior=phenotype,
        agentConfig=agent_config,
        padding=15,
        init_type=GridInitialization(
            num_agents=num_agents,
            grid_size=(4, 3),
            bb=((25 * 3, 30 * 3), (146 * 3, 111 * 3))
        ),
        stop_at=None,
    )

    # Define the breath and depth of novelty search with n_generations and n_populations
    # Modify k_nn to change the number of nearest neighbors used in calculating novelty.
    # Increase simulation_lifespan to allow agents to interact with each other for longer.
    # Set save_archive to True to save the resulting archive to /out.
    novelty_config = GeneticEvolutionConfig(
        gene_rules=genotype,
        phenotype_config=phenotype,
        n_generations=50,
        n_population=50,
        crossover_rate=0.7,
        mutation_rate=0.15,
        world_config=world_config,
        k_nn=15,
        simulation_lifespan=605,
        display_novelty=False,
        save_archive=True,
        show_gui=True
    )

    # Novelty Search through Genetic Evolution
    archive = evolve(config=novelty_config)

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world_config
    results_config.archive = archive

    # Take Results from Evolution, reduce dimensionality, and present User with Clusters.
    report(config=results_config)
