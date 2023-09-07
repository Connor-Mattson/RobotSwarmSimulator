import time
import pygame
import os
from ..config.EvolutionaryConfig import GeneticEvolutionConfig
from ..gui.evolutionGUI import EvolutionGUI
from .BehaviorDiscovery import BehaviorDiscovery

FRAMERATE = 200
GUI_WIDTH = 200


def multi_evolve(config: GeneticEvolutionConfig, output_config=None, heterogeneous=False):

    save_results = config.save_archive
    display_plots = config.display_novelty
    trial_name = f"{str(int(time.time()))}"

    # Initialize GA
    gene_builder = config.gene_builder
    evolution = BehaviorDiscovery(
        generations=config.generations,
        population_size=config.population,
        crossover_rate=config.crossover_rate,
        mutation_rate=config.mutation_rate,
        world_config=config.world_config,
        lifespan=config.lifespan,
        k_neighbors=config.k,
        genome_builder=gene_builder,
        behavior_config=config.behavior_config,
        mutation_flip_chance=config.mutation_flip_chance,
        allow_external_archive=config.use_external_archive,
        genome_dependent_world=config.world_metadata,
        seed=config.seed,
    )

    last_gen_timestamp = time.time()

    # Generation Loop
    for generation in range(evolution.total_generations):
        evolution.multithreadEntirePopulation(threads=12)
        evolution.evaluate()
        evolution.evolve()
        current_time = time.time()
        print(f"Generation {generation} completed in {current_time - last_gen_timestamp}")
        last_gen_timestamp = current_time
        if save_results and config.save_every is not None:
            if generation % config.save_every == 0:
                evolution.archive.saveArchive(f"b_{trial_name}_{generation}")
                evolution.archive.saveGenotypes(f"g_{trial_name}_{generation}")

    if save_results:
        evolution.archive.saveArchive(f"b_{trial_name}_final")
        evolution.archive.saveGenotypes(f"g_{trial_name}_final")

    if display_plots:
        evolution.results()

    return evolution.archive
