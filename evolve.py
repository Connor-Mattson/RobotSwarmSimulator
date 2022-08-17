import pygame
from sklearn.metrics import rand_score
from src.gui.evolutionGUI import EvolutionGUI
from src.novelty.BehaviorDiscovery import BehaviorDiscovery
from src.gui.agentGUI import DifferentialDriveGUI
from src.world.RectangularWorld import RectangularWorld

screen = None
FRAMERATE = 60
WORLD_WIDTH = 500
WORLD_HEIGHT = 500
GUI_WIDTH = 200

# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Evolutionary Novelty Search")
     
    # screen must be global so that other modules can access + draw to the window
    global screen
    screen = pygame.display.set_mode((WORLD_WIDTH + GUI_WIDTH, WORLD_HEIGHT))
     
    # define a variable to control the main loop
    running = True
    paused = False

    # Create the GUI
    gui = EvolutionGUI(x=WORLD_WIDTH, y=0, h=WORLD_HEIGHT, w=GUI_WIDTH)
    gui.set_title("Novelty Evolution")

    # Initialize GA
    evolution = BehaviorDiscovery(
        generations=40,
        population_size=40,
        crossover_rate=0.8,
        mutation_rate=0.1,
        world_size=[WORLD_WIDTH, WORLD_HEIGHT],
        lifespan=10,
        agents=30,
        k_neighbors=15
    )

    gui.set_discovery(evolution)
     
    # Generation Loop
    for generation in range(evolution.total_generations):

        evolution.curr_generation = generation

        # Population loop
        for i, genome in enumerate(evolution.population):
            # Looped Event Handling
            for event in pygame.event.get():
                # Cancel the game loop if user quits the GUI
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused

            if(paused):
                pygame.time.Clock().tick(FRAMERATE)
                continue

            screen.fill((0, 0, 0))

            evolution.curr_genome = i
            evolution.runSingleGeneration(screen, i=i)
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

    evolution.results()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()