import pygame

from src.gui.abstractGUI import AbstractGUI
from src.config.OutputTensorConfig import OutputTensorConfig
import numpy as np

class World():

    def __init__(self, w, h):
        self.population = []
        self.behavior = []
        self.bounded_width = 100
        self.bounded_height = 100
        self.gui = None
        self.bounded_height = h
        self.bounded_width = w
        pass
    
    def setup(self):
        pass

    def step(self):
        pass

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
                    screen.fill((0, 0, 0))
                    pygame.display.flip()

                if not output_capture or not output_capture.timeless:
                    screen.fill((0, 0, 0))

                if frame_markers and step > frame_markers[0]:
                    self.draw(screen)
                    pygame.display.flip()

            if output_capture:
                if step in frame_markers:
                    screen_capture = pygame.surfarray.array2d(screen)
                    if output is None:
                        output = np.array([screen_capture])
                    else:
                        output = np.concatenate((output, [screen_capture]))

        return output

