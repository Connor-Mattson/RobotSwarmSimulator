import pygame
from ..gui.agentGUI import DifferentialDriveGUI
from .WorldFactory import WorldFactory
from ..util.timer import Timer

FRAMERATE = 200

class Simulation:
    def __init__(self, world_config, show_gui=True, gui=None, stop_detection=None, world_key_events=False, gui_key_events=False, subscribers=None, save_duration=1200, save_every_ith_frame=3, save_time_per_frame=50, step_size=1, auto_start_gif=None, start_paused=False):
        self.world_config = world_config
        self.stop_detection = stop_detection
        self.world_key_events = world_key_events
        self.gui_key_events = gui_key_events
        self.save_duration = save_duration
        self.save_every_ith_frame = save_every_ith_frame
        self.save_time_per_frame = save_time_per_frame
        self.auto_start_gif = auto_start_gif

        # initialize the pygame module
        if show_gui:
            pygame.init()
            pygame.display.set_caption("Swarm Simulation")

        # screen must be global so that other modules can access + draw to the window
        gui_width = 200
        if gui:
            gui_width = gui.w
        if show_gui:
            self.screen = pygame.display.set_mode((world_config.w + gui_width, world_config.h))

        # define a variable to control the main loop
        self.running = True
        self.paused = start_paused
        self.draw_world = True

        # Create the simulation world
        self.world = WorldFactory.create(world_config)

        # Attach any subscribers to the world
        self.world_subscribers = []
        if subscribers:
            self.world_subscribers = subscribers

        # Create the GUI
        self.gui = gui
        if show_gui and not gui:
            self.gui = DifferentialDriveGUI(x=world_config.w, y=0, h=world_config.h, w=gui_width)

        # Attach the world to the gui and vice versa
        if self.gui:
            self.gui.set_world(self.world)
            self.gui.set_screen(self.screen)
            self.world.attach_gui(self.gui)

        self.total_allowed_steps = world_config.stop_at
        self.steps_taken = 0
        self.steps_per_frame = step_size

        self.labels = [pygame.K_RETURN, pygame.K_q, pygame.K_0, pygame.K_KP0, pygame.K_1, pygame.K_KP1, pygame.K_2,
                  pygame.K_KP2,
                  pygame.K_3, pygame.K_KP3, pygame.K_4, pygame.K_KP4, pygame.K_5, pygame.K_KP5]

    def spin(self):
        while self.running:
            ret = self.step()
            if ret is not None:
                return ret

    def record_gif(self):
        from .subscribers.World2Gif import World2Gif
        self.world_subscribers.append(World2Gif(duration=self.save_duration, every_ith_frame=self.save_every_ith_frame,
                                                time_per_frame=self.save_time_per_frame))

    def step(self, per_step_draw=True, stall=False):
        if self.gui:
            for event in pygame.event.get():
                # Cancel the game loop if user quits the GUI
                if event.type == pygame.QUIT:
                    return self.world
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                        # print(f"Paused on Simulation Step: {steps_taken}")
                    if event.key == pygame.K_RIGHT and self.paused:
                        # ON Right Arrow Pressed, draw single frame
                        self.world.step()
                        self.steps_taken += 1
                        self.gui.set_time(self.steps_taken)
                        self.screen.fill(self.world_config.background_color)
                        if self.gui and self.screen:
                            if self.draw_world:
                                self.world.draw(self.screen)
                            self.gui.draw(self.screen)
                        pygame.display.flip()
                    if event.key == pygame.K_r:
                        self.world = WorldFactory.create(self.world_config)
                        self.steps_taken = 0
                    if event.key == pygame.K_RSHIFT:
                        self.steps_per_frame *= 2
                        self.steps_per_frame = min(self.steps_per_frame, 100)
                    if event.key == pygame.K_LSHIFT and self.steps_per_frame > 1:
                        self.steps_per_frame /= 2
                        self.steps_per_frame = round(self.steps_per_frame)
                    if event.key == pygame.K_w:
                        draw_world = not self.draw_world
                    if event.key == pygame.K_F3:
                        from .WorldIO import WorldIO
                        WorldIO.save_world(self.world)
                    if event.key == pygame.K_F4:
                        self.record_gif()
                    if self.world_key_events:
                        self.world.handle_key_press(event)
                    if self.gui and self.gui_key_events:
                        self.gui.pass_key_events(event)
                    if event.key in self.labels:
                        return event.key, self.steps_taken

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.world.onClick(pos)

            if self.world_key_events:
                keys = pygame.key.get_pressed()
                self.world.handle_held_keys(keys)

            if self.paused:
                pygame.time.Clock().tick(FRAMERATE)
                return

        # Calculate Steps - Stop if we reach desired frame
        if not stall:
            for _ in range(self.steps_per_frame):

                if self.stop_detection is not None and self.stop_detection(self.world):
                    running = False
                    return self.world

                if self.total_allowed_steps is not None:
                    # noinspection PyTypeChecker
                    if self.steps_taken > self.total_allowed_steps:
                        running = False
                        return self.world

                self.world.step()

                # Broadcast to any world subscribers
                _ = [sub.notify(self.world, self.screen) for sub in self.world_subscribers]

                self.steps_taken += 1
                # if steps_taken % 1000 == 0:
                # print(f"Total steps: {steps_taken}")

        # Draw!
        if self.gui and self.screen and per_step_draw:
            self.gui.set_time(self.steps_taken)
            self.screen.fill(self.world_config.background_color)
            if self.draw_world:
                self.world.draw(self.screen)
            # gui.step()
            if self.gui.track_all_mouse:
                self.gui.recieve_mouse(pygame.mouse.get_rel())
            if self.gui.track_all_events:
                self.gui.recieve_events(pygame.event.get())
            self.gui.draw(self.screen)

        # Determine whether to automatically call a gif save here
        if self.auto_start_gif is not None and self.auto_start_gif == self.world.total_steps:
            self.record_gif()

        # Limit the FPS of the simulation to FRAMERATE
        if self.gui:
            pygame.display.flip()
            pygame.time.Clock().tick(FRAMERATE)


class DirectEvaluation:
    def __init__(self, world_config, show_gui=True, gui=None, output_capture=None, stop_detection=None, world_key_events=False, gui_key_events=False):
        self.world_config = world_config
        self.stop_detection = stop_detection
        self.world_key_events = world_key_events
        self.gui_key_events = gui_key_events
        self.output = output_capture

        # initialize the pygame module
        if show_gui:
            pygame.init()
            pygame.display.set_caption("Swarm Simulation")

        # screen must be global so that other modules can access + draw to the window
        gui_width = 200
        if gui:
            gui_width = gui.w
        if show_gui:
            self.screen = pygame.display.set_mode((world_config.w + gui_width, world_config.h))
            self.output.screen = self.screen

        # define a variable to control the main loop
        self.running = True
        self.draw_world = True

        # Create the simulation world
        self.world = WorldFactory.create(world_config)

    def evaluate(self):
        return self.world, self.world.evaluate(self.world_config.stop_at, output_capture=self.output, screen=self.screen)


def main(world_config, show_gui=True, gui=None, stop_detection=None, world_key_events=False, gui_key_events=False, subscribers=None, save_duration=1200, save_every_ith_frame=3, save_time_per_frame=50, step_size=1, auto_start_gif=None, start_paused=False):
    simulation = Simulation(world_config, show_gui, gui, stop_detection, world_key_events, gui_key_events, subscribers, save_duration, save_every_ith_frame, save_time_per_frame, step_size, auto_start_gif, start_paused)
    return simulation.spin()