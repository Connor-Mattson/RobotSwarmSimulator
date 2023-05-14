import pygame

from ..gui.abstractGUI import AbstractGUI
from ..config.OutputTensorConfig import OutputTensorConfig
import numpy as np
import math
from scipy.ndimage.filters import gaussian_filter

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

    """
    Helper function for evaluate_density_map
    Given a matrix indicating the number of agents at each point, along with an index of that matrix,
    returns the sum of all of the agents within a 60x60 box centered at that index.
    Overflow is accounted for in evaluate_denisty_map
    """
    def _scan_kernel(self, point_map, h, w):
        row_start = w - 50
        row_end = w + 50
        col_start = h - 50
        col_end = h + 50
        kernel_size = 101
        sigma = 20
        kernel = np.zeros((kernel_size, kernel_size))
        kernel[kernel_size // 2, kernel_size // 2] = 1
        kernel = gaussian_filter(kernel, sigma=sigma)
        window = point_map[row_start:row_end + 1, col_start:col_end + 1] * kernel
        return np.sum(window)

        # center = 24
        # tally = 0
        # for (i, j), point in np.ndenumerate(window):
        #     if point == 0:
        #         continue
        #     distance_from_center = math.sqrt((i - center) ** 2 + (j - center) ** 2)
        #     score = 0
        #     if distance_from_center != 0:
        #         score = 100 / distance_from_center
        #     else:
        #         score = 100
        #     tally += score
        #
        # return tally

    """
    Helper function for evaluate_density_map
    Normalizes the density map so that all of the values in the map are between 0 and 1.
    """
    def _normalize_density_map(self, density_map):
        print(np.max(density_map))
        return density_map / np.max(density_map)


    """
    This is an alternative version of evaluate that outputs a density map of the agents over a specified
    number of steps. This is achieved through pooling.
    Padding = 30
    Stride = 20
    Kernel = ~60
    """
    def evaluate_density_map(self, steps: int):
        # Keeps track of the number of agents at each point. Padded by 30 on all sides
        point_map = np.zeros((self.bounded_height + 100, self.bounded_width + 100), dtype=int)

        # Populate the point map by stepping, getting the poisitions of agents at each step, and adding them to the map
        for step in range(steps):
            self.step()
            for agent in self.population:
                x = math.floor(agent.getPosition()[0] + 50)
                y = math.floor(agent.getPosition()[1] + 50)
                point_map[y, x] += 1
        step = 5
        # Create density map with all density starting at 0
        # Dimensions of the map will be significantly smaller than the dimensions of the arena because step size = 20
        output_shape = (math.floor(self.bounded_height / step), math.floor(self.bounded_height / step))
        output = np.zeros(output_shape, dtype=float)
        output_h = 0
        output_w = 0
        # Iterate over the point map by step of 20
        for h in range(50, self.bounded_height, step):
            output_h += 1
            for w in range(50, self.bounded_width, step):
                # The value at output[output_h, output_w] is the sum of points in the kernel at point_map[h, w]
                output[output_h, output_w] = self._scan_kernel(point_map, h, w)
                output_w += 1
            output_w = 0
        # Ensures that all values in the map are between 0 and 1
        print(output.shape)
        return self._normalize_density_map(output)

    def evaluate(self, steps: int, output_capture: OutputTensorConfig = None, screen=None, alternative_approach=None):
        # Alternative approach query
        if alternative_approach == "density-map":
            return self.evaluate_density_map(steps)
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
                if not output_capture.timeless and step in frame_markers:
                    screen_capture = pygame.surfarray.array2d(screen)
                    if output is None:
                        output = np.array([screen_capture])
                    else:
                        output = np.concatenate((output, [screen_capture]))

        if output_capture and output_capture.timeless:
            output = pygame.surfarray.array2d(screen)

        return output



