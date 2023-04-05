import pygame

from ..gui.abstractGUI import AbstractGUI
from ..config.OutputTensorConfig import OutputTensorConfig
import numpy as np

class World():

    def __init__(self, w=100, h=100, metadata=None):
        self.population = []
        self.behavior = []
        self.objects = []  # A list of obstacles or other objects that belong to the world
        self.goals = []  # A set of goal markers in a world
        self.gui = None
        self.bounded_height = h
        self.bounded_width = w
        self.total_steps = 0
        if metadata is None:
            self.meta = {}
        else:
            self.meta = metadata
    
    def setup(self):
        pass

    def step(self):
        self.total_steps += 1

    def draw(self, screen):
        pass

    def attach_gui(self, gui: AbstractGUI):
        self.gui = gui

    def evaluate(self, steps: int, output_capture: OutputTensorConfig = None, screen=None):
        frame_markers = []
        output = None
        screen = None
        if output_capture is not None:
            if output_capture.total_frames * output_capture.step > steps:
                raise Exception("Error: You have indicated an output capture that is larger than the lifespan of the simulation.")
            start = steps - (output_capture.total_frames * output_capture.step)

            if output_capture.timeless:
                frame_markers = [start]
            else:
                frame_markers = [(start + (output_capture.step * i)) - 1 for i in range(output_capture.total_frames)]

            screen = output_capture.screen

        for step in range(steps):
            self.step()

            if output_capture and output_capture.screen:
                # If start of recording, clear screen
                if frame_markers and step == frame_markers[0]:
                    screen.fill(output_capture.background_color)
                    pygame.display.flip()

                if not output_capture or not output_capture.timeless:
                    screen.fill(output_capture.background_color)

                if frame_markers and step > frame_markers[0]:
                    self.draw(screen)
                    pygame.display.flip()

            if output_capture:
                if not output_capture.timeless and step in frame_markers:
                    if output_capture.colored:
                        screen_capture = pygame.surfarray.array3d(screen)
                    else:
                        screen_capture = pygame.surfarray.array2d(screen)
                    if output is None:
                        output = np.array([screen_capture])
                    else:
                        output = np.concatenate((output, [screen_capture]))

        if output_capture and output_capture.timeless:
            if output_capture.colored:
                output = pygame.surfarray.array3d(screen)
            else:
                output = pygame.surfarray.array2d(screen)

        return output

