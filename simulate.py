import math

import pygame
from src.gui.agentGUI import DifferentialDriveGUI
from src.world.RectangularWorld import RectangularWorld

screen = None
FRAMERATE = 128
WORLD_WIDTH = 500
WORLD_HEIGHT = 500
GUI_WIDTH = 200


# define a main function
def main(controller=None, seed=None):
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
    world = RectangularWorld(WORLD_WIDTH, WORLD_HEIGHT, pop_size=30)
    # world.setup(controller=[-0.7, 0.3, 1.0, 1.0])
    # world.setup(controller=[-0.7, -1.0, 1.0, -1.0])

    if controller is not None:
        world.setup(controller=controller, seed=seed)

    # Create the GUI
    gui = DifferentialDriveGUI(x=WORLD_WIDTH, y=0, h=WORLD_HEIGHT, w=GUI_WIDTH)
    gui.set_title("Differential Drive")


    # Attach the world to the gui and visa versa
    gui.set_world(world)
    world.attach_gui(gui)

    total_allowed_steps = None
    steps_taken = 0
    steps_per_frame = 1

    labels = [pygame.K_RETURN, pygame.K_q, pygame.K_0, pygame.K_KP0, pygame.K_1, pygame.K_KP1, pygame.K_2, pygame.K_KP2, pygame.K_3, pygame.K_KP3, pygame.K_4, pygame.K_KP4, pygame.K_5, pygame.K_KP5]

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
                    # print(f"Paused on Simulation Step: {steps_taken}")
                if event.key == pygame.K_RIGHT and paused:
                    # ON Right Arrow Pressed, draw single frame
                    world.step()
                    steps_taken += 1
                    screen.fill((0, 0, 0))
                    world.draw(screen)
                    gui.draw(screen)
                    pygame.display.flip()

                if event.key == pygame.K_r:
                    world.setup(controller=controller, seed=seed)
                    steps_taken = 0

                if event.key == pygame.K_RSHIFT:
                    steps_per_frame *= 2
                    steps_per_frame = min(steps_per_frame, 50)
                if event.key == pygame.K_LSHIFT and steps_per_frame > 1:
                    steps_per_frame /= 2
                    steps_per_frame = round(steps_per_frame)
                if event.key in labels:
                    return event.key, steps_taken

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                world.onClick(pos)

        if paused:
            pygame.time.Clock().tick(FRAMERATE)
            continue

        # Calculate Steps - Stop if we reach desired frame
        for _ in range(steps_per_frame):
            if total_allowed_steps is not None:
                if steps_taken > total_allowed_steps:
                    break
            world.step()
            steps_taken += 1
            # if steps_taken % 1000 == 0:
                # print(f"Total steps: {steps_taken}")

        gui.set_time(steps_taken)

        # Draw!
        screen.fill((0, 0, 0))
        world.draw(screen)
        gui.draw(screen)
        pygame.display.flip()

        # Limit the FPS of the simulation to FRAMERATE
        pygame.time.Clock().tick(FRAMERATE)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    # custom_controller = [-0.4516, -0.5024, -0.2318, 1.0, -1.16*math.pi]

    # Complex Circuits (For n > 30 this is just a circle)
    # Use n = 25
    # custom_controller = [-0.4, -0.5, -0.2318, 1.0, -1.16 * math.pi]

    # Complex Circuits 2
    # custom_controller = [0.6836, 0.95, 0.86, -0.9, -1.72*math.pi]

    # Membrane (for N > 50)
    # custom_controller = [0.6336, 0.95, 0.86, -0.9, -1.72*math.pi]

    # Partner Search (Dependent on stochastic initialization, unreliable)
    # custom_controller = [-0.549, -0.4532, -0.2683, -1.0, -(math.pi/2)]

    # Localized Aggregation
    # custom_controller = [-0.0471, -1.0, -1.0, 0.1820, (-1.3 * math.pi)]

    # Normal Aggregation
    # custom_controller = [-0.7, -1.0, 1.0, -1.0]

    # Normal Cyclic Pursuit
    # custom_controller = [-0.7, 0.3, 1.0, 1.0]

    # custom_controller = [-0.7, -1.0, 1.0, -0.7, -1.0, 1.0, -1.0, -1.0, 0, math.pi]
    custom_controller = [0.47988, 0.10683, 0.42625, 0.32519]


    a = 0.8
    b = 0.6

    # a = 0.4
    # b = 0.8

    custom_controller = [0.9, 0.88, 1.0, 1.0]

    label = main(controller=custom_controller, seed=10)
    print(label)
