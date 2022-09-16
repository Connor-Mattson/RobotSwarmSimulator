import pygame
from ..gui.agentGUI import DifferentialDriveGUI
from .WorldFactory import WorldFactory

screen = None
FRAMERATE = 128
GUI_WIDTH = 200


def main(world_config):
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Swarm Simulation")

    # screen must be global so that other modules can access + draw to the window
    global screen
    screen = pygame.display.set_mode((world_config.w + GUI_WIDTH, world_config.h))

    # define a variable to control the main loop
    running = True
    paused = False

    # Create the simulation world
    world = WorldFactory.create(world_config)

    # Create the GUI
    gui = DifferentialDriveGUI(x=world_config.w, y=0, h=world_config.h, w=GUI_WIDTH)
    gui.set_title("Differential Drive")

    # Attach the world to the gui and vice versa
    gui.set_world(world)
    world.attach_gui(gui)

    total_allowed_steps = None
    steps_taken = 0
    steps_per_frame = 1

    labels = [pygame.K_RETURN, pygame.K_q, pygame.K_0, pygame.K_KP0, pygame.K_1, pygame.K_KP1, pygame.K_2, pygame.K_KP2,
              pygame.K_3, pygame.K_KP3, pygame.K_4, pygame.K_KP4, pygame.K_5, pygame.K_KP5]

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
                    world = WorldFactory.create(world_config)
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
                # noinspection PyTypeChecker
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
