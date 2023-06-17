"""
DO NOT ALTER THIS FILE.
This file should remain a constant reference to the experiments conducted in Brown et al.
Please create your own file for experiments or alter 'demo/evolution/playground.py' instead.
"""
from src.novel_swarms.novelty.GeneRule import GeneRule, GeneRuleContinuous
from src.novel_swarms.novelty.evolve import main as evolve
from src.novel_swarms.results.results import main as report
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.config.EvolutionaryConfig import GeneticEvolutionConfig

if __name__ == "__main__":

    # Use the default Differential Drive Agent, initialized with a single sensor and normal physics
    agent_config = ConfigurationDefaults.DIFF_DRIVE_AGENT

    # Create a Genotype Ruleset that matches the size and boundaries of your robot controller _max and _min represent
    # the maximum and minimum acceptable values for that index in the genome. mutation_step specifies the largest
    # possible step in any direction that the genome can experience during mutation.
    genotype = [
        GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=4),
        GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=4),
        GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=4),
        GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=4),
    ]

    # Use the default Behavior Vector (from Brown et al.) to measure the collective swarm behaviors
    phenotype = ConfigurationDefaults.BEHAVIOR_VECTOR

    # Define an empty Rectangular World with size (w, h) and n agents.
    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=30,
        behavior=phenotype,
        agentConfig=agent_config,
        padding=15
    )

    # Define the breath and depth of novelty search with n_generations and n_populations
    # Modify k_nn to change the number of nearest neighbors used in calculating novelty.
    # Increase simulation_lifespan to allow agents to interact with each other for longer.
    # Set save_archive to True to save the resulting archive to /out.
    novelty_config = GeneticEvolutionConfig(
        gene_rules=genotype,
        phenotype_config=phenotype,
        n_generations=100,
        n_population=100,
        crossover_rate=0.7,
        mutation_rate=0.15,
        world_config=world_config,
        k_nn=15,
        simulation_lifespan=1200,
        display_novelty=False,
        save_archive=False,
        show_gui=True
    )

    # Novelty Search through Genetic Evolution
    archive = evolve(config=novelty_config)

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world_config
    results_config.archive = archive

    # Take Results from Evolution, reduce dimensionality, and present User with Clusters.
    report(config=results_config)
