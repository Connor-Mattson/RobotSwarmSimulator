import pygame
from src.world.RectanglularWorld import RectangularWorld

screen = None
FRAMERATE = 30
WORLD_WIDTH = 500
WORLD_HEIGHT = 500

# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    # logo = pygame.image.load("logo32x32.png")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("Swarm Simulation")
     
    # screen must be global so that other modules can access + draw to the window
    global screen
    screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
     
    # define a variable to control the main loop
    running = True

    # Create the simulation world
    world = RectangularWorld(WORLD_WIDTH, WORLD_HEIGHT, pop_size=50)
    world.setup()
     
    # main loop
    while running:

        # Caclulate Steps
        world.step()

        # Draw!
        screen.fill((0, 0, 0))
        world.draw(screen)
        pygame.display.flip()

        # Looped Event Handling
        for event in pygame.event.get():
            # Cancel the game loop if user quits the GUI
            if event.type == pygame.QUIT:
                running = False

        # Limit the FPS of the simulation to FRAMERATE
        pygame.time.Clock().tick(FRAMERATE)
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()