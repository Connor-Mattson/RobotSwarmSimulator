import pygame
from ..gui.agentGUI import DifferentialDriveGUI
from .WorldFactory import WorldFactory
from ..util.timer import Timer

screen = None
FRAMERATE = 200

def main(world_config, show_gui=True, gui=None, stop_detection=None, step_size=1):
    # initialize the pygame module
    if show_gui:
        pygame.init()
        pygame.display.set_caption("Swarm Simulation")

    # screen must be global so that other modules can access + draw to the window
    global screen
    gui_width = 200
    if gui:
        gui_width = gui.w
    if show_gui:
        screen = pygame.display.set_mode((world_config.w + gui_width, world_config.h))

    # define a variable to control the main loop
    running = True
    paused = False
    draw_world = True

    # Create the simulation world
    world = WorldFactory.create(world_config)

    # Create the GUI
    if show_gui and not gui:
        gui = DifferentialDriveGUI(x=world_config.w, y=0, h=world_config.h, w=gui_width)

    # Attach the world to the gui and vice versa
    if gui:
        gui.set_world(world)
        world.attach_gui(gui)

    total_allowed_steps = world_config.stop_at
    steps_taken = 0
    steps_per_frame = step_size

    labels = [pygame.K_RETURN, pygame.K_q, pygame.K_0, pygame.K_KP0, pygame.K_1, pygame.K_KP1, pygame.K_2, pygame.K_KP2,
              pygame.K_3, pygame.K_KP3, pygame.K_4, pygame.K_KP4, pygame.K_5, pygame.K_KP5]

    # Main loop
    time_me = Timer("World Step")
    while running:
        # Looped Event Handling
        if gui:
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
                        gui.set_time(steps_taken)
                        screen.fill(world_config.background_color)
                        if gui and screen:
                            if draw_world:
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
                    if event.key == pygame.K_w:
                        draw_world = not draw_world
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

            if stop_detection is not None and stop_detection(world):
                running = False
                return world

            if total_allowed_steps is not None:
                # noinspection PyTypeChecker
                if steps_taken > total_allowed_steps:
                    running = False
                    return world

            world.step()
            steps_taken += 1
            # if steps_taken % 1000 == 0:
            # print(f"Total steps: {steps_taken}")

        # Draw!
        if gui and screen:
            gui.set_time(steps_taken)
            screen.fill(world_config.background_color)
            if draw_world:
                world.draw(screen)
            gui.draw(screen)

        # Limit the FPS of the simulation to FRAMERATE
        if gui:
            pygame.display.flip()
            pygame.time.Clock().tick(FRAMERATE)


