import math

import pygame
import time
from src.gui.evolutionGUI import EvolutionGUI
from src.novelty.BehaviorDiscovery import BehaviorDiscovery
from src.novelty.GeneRule import GeneRule

FRAMERATE = 60
WORLD_WIDTH = 500
WORLD_HEIGHT = 500
GUI_WIDTH = 200


def main():
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Evolutionary Novelty Search")

    # screen must be global so that other modules can access + draw to the window
    screen = pygame.display.set_mode((WORLD_WIDTH + GUI_WIDTH, WORLD_HEIGHT))

    # define a variable to control the main loop
    running = True
    paused = False
    save_results = True
    display_plots = True

    # Create the GUI
    gui = EvolutionGUI(x=WORLD_WIDTH, y=0, h=WORLD_HEIGHT, w=GUI_WIDTH)
    gui.set_title("Novelty Evolution")

    # Initialize GA
    gene_rules = [
        GeneRule(_max=1.0, _min=-1.0, mutation_step=0.5, round_digits=4),
        GeneRule(_max=1.0, _min=-1.0, mutation_step=0.5, round_digits=4),
        GeneRule(_max=1.0, _min=-1.0, mutation_step=0.5, round_digits=4),
        GeneRule(_max=1.0, _min=-1.0, mutation_step=0.5, round_digits=4),
        # GeneRule(_max=1.0, _min=-1.0, mutation_step=0.5, round_digits=4),
        # GeneRule(_max=1.0, _min=-1.0, mutation_step=0.5, round_digits=4),
        # GeneRule(_max=1.0, _min=-1.0, mutation_step=0.5, round_digits=4),
        # GeneRule(_max=1.0, _min=-1.0, mutation_step=0.5, round_digits=4),
        # GeneRule(_max=(math.pi), _min=(-math.pi), mutation_step=(math.pi / 3), round_digits=6),
        # GeneRule(_max=(math.pi), _min=(-math.pi), mutation_step=(math.pi / 3), round_digits=6),
    ]

    evolution = BehaviorDiscovery(
        generations=50,
        population_size=50,
        crossover_rate=0.7,
        mutation_rate=0.15,
        world_size=[WORLD_WIDTH, WORLD_HEIGHT],
        lifespan=4000,
        agents=30,
        k_neighbors=15,
        genotype_rules=gene_rules
    )

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
            evolution.runSingleGeneration(screen, i=i, seed=i)
            gui.draw(screen=screen)

            pygame.display.flip()

            # Limit the FPS of the simulation to FRAMERATE
            pygame.time.Clock().tick(FRAMERATE)

        screen.fill((0, 0, 0))
        evolution.evaluate(screen=screen)
        gui.draw(screen=screen)
        pygame.display.flip()

        screen.fill((0, 0, 0))
        evolution.evolve()
        gui.draw(screen=screen)
        pygame.display.flip()

        current_time = time.time()
        gui.set_elapsed_time(current_time - last_gen_timestamp)
        last_gen_timestamp = current_time

    if save_results:
        evolution.archive.saveArchive(f"pheno_g{len(gene_rules)}_gen{evolution.total_generations}_pop{len(evolution.population)}")
        evolution.archive.saveGenotypes(f"geno_g{len(gene_rules)}_gen{evolution.total_generations}_pop{len(evolution.population)}")

    if display_plots:
        evolution.results()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
