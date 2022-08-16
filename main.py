import pygame
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
    # load and set the logo
    # logo = pygame.image.load("logo32x32.png")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("Swarm Simulation")
     
    # screen must be global so that other modules can access + draw to the window
    global screen
    screen = pygame.display.set_mode((WORLD_WIDTH + GUI_WIDTH, WORLD_HEIGHT))
     
    # define a variable to control the main loop
    running = True
    paused = False

    # Create the simulation world
    world = RectangularWorld(WORLD_WIDTH, WORLD_HEIGHT, pop_size=4)
    world.setup()

    # Create the GUI
    gui = DifferentialDriveGUI(x=WORLD_WIDTH, y=0, h=WORLD_HEIGHT, w=GUI_WIDTH)
    gui.set_title("Differential Drive", subtitle="Goal: Aggregation")
   
    # Attach the world to the gui and visa versa
    gui.set_world(world)
    world.attach_gui(gui)
     
    # Main loop
    while running:

        # Looped Event Handling
        for event in pygame.event.get():
            # Cancel the game loop if user quits the GUI
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                world.onClick(pos)

        if(paused):
            pygame.time.Clock().tick(FRAMERATE)
            continue

        # Caclulate Steps
        STEPS = 1
        for _ in range(STEPS):
            world.step()

        # Draw!
        screen.fill((0, 0, 0))
        world.draw(screen)
        gui.draw(screen)
        pygame.display.flip()

        # Limit the FPS of the simulation to FRAMERATE
        pygame.time.Clock().tick(FRAMERATE)
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()