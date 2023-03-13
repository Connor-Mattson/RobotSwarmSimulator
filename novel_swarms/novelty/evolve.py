import time
import pygame
import os
from ..config.EvolutionaryConfig import GeneticEvolutionConfig
from ..gui.evolutionGUI import EvolutionGUI
from .BehaviorDiscovery import BehaviorDiscovery

FRAMERATE = 200
GUI_WIDTH = 200


def main(config: GeneticEvolutionConfig, output_config=None):

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Evolutionary Novelty Search")

    # screen must be global so that other modules can access + draw to the window
    width = config.world_config.w
    if config.show_gui:
        width += GUI_WIDTH
    screen = pygame.display.set_mode((width, config.world_config.h))

    # define a variable to control the main loop
    running = True
    paused = False
    save_results = config.save_archive
    display_plots = config.display_novelty

    # Create the GUI
    if config.show_gui:
        gui = EvolutionGUI(x=config.world_config.w, y=0, h=config.world_config.h, w=GUI_WIDTH)
        gui.set_title("Novelty Evolution")

    # Create a trial folder in the specified location
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
        genome_dependent_world=config.world_metadata
    )

    if config.show_gui:
        gui.set_discovery(evolution)
    last_gen_timestamp = time.time()

    # Generation Loop
    for generation in range(evolution.total_generations):

        if not running:
            break

        evolution.curr_generation = generation

        # Population loop
        for i, genome in enumerate(evolution.population):
            # Looped Event Handling
            for event in pygame.event.get():
                # Cancel the game loop if user quits the GUI
                if event.type == pygame.QUIT:
                    running = False

            if not running:
                break

            screen.fill((0, 0, 0))

            evolution.curr_genome = i
            evolution.runSinglePopulation(screen=screen, i=i, seed=i, output_config=output_config)

            if config.show_gui:
                gui.draw(screen=screen)

            pygame.display.flip()

            # Limit the FPS of the simulation to FRAMERATE
            pygame.time.Clock().tick(FRAMERATE)

        screen.fill((0, 0, 0))
        evolution.evaluate()
        if config.show_gui:
            gui.draw(screen=screen)
        pygame.display.flip()

        evolution.evolve()
        if config.show_gui:
            screen.fill((0, 0, 0))
            gui.draw(screen=screen)
            pygame.display.flip()

        current_time = time.time()
        if config.show_gui:
            gui.set_elapsed_time(current_time - last_gen_timestamp)
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
