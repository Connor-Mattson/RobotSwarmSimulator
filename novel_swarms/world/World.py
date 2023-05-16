import pygame

from ..gui.abstractGUI import AbstractGUI
from ..config.OutputTensorConfig import OutputTensorConfig
import numpy as np
import math
from scipy.ndimage.filters import gaussian_filter
from PIL import Image

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
    returns the sum of all of the agents within a 100x100 box centered at that index.
    Overflow is accounted for in evaluate_denisty_map
    """
    @staticmethod
    def _scan_kernel(point_map, h, w):
        # Get window area
        row_start = h - 50
        row_end = h + 50
        col_start = w - 50
        col_end = w + 50
        kernel_size = 101

        sigma = 20 # Standard deviation of gaussian blur
        kernel = np.zeros((kernel_size, kernel_size)) # Create a 100x100 kernel
        kernel[kernel_size // 2, kernel_size // 2] = 1 # Set center of kernel window to 1
        kernel = gaussian_filter(kernel, sigma=sigma) # Apply gaussian blur out from center
        window = point_map[row_start:row_end + 1, col_start:col_end + 1] * kernel
        return np.sum(window)

    """
    Helper function for evaluate_density_map
    Normalizes the density map so that all of the values in the map are between 0 and 1.
    """
    @staticmethod
    def _normalize_density_map(density_map):
        return density_map / np.max(density_map)


    """
    IMPORTANT: In order for this function to work, density_map_on MUST be set to True in world/simulate.py
    This is an alternative version of evaluate that outputs a density map of the agents over a specified
    number of steps. Skip specifies the frequency at which data should be collected.
    For example, if step = 50 and skip = 10, then the density map will contain the positions of agents at
    steps 0, 10, 20, 30, 40
    
    Padding = 50
    Stride = 5
    Kernel = 100
    """
    def evaluate_density_map(self, steps: int, filepath="density.png", skip=10, stride=5):
        # Keeps track of the number of agents at each point. Padded by 50 on all sides
        point_map = np.zeros((self.bounded_height + 100, self.bounded_width + 100), dtype=int)

        # Populate the point map by stepping, getting the positions of agents at each step, and adding them to the map
        for step in range(steps * skip):
            self.step()
            if step % skip == 0:  # If we should collect data about the agents' positions
                for agent in self.population:
                    x = math.floor(agent.getPosition()[0] + 50)
                    y = math.floor(agent.getPosition()[1] + 50)
                    point_map[y, x] += 1
        # Create density map with all density starting at 0
        # Dimensions of the map will be significantly smaller than the dimensions of the arena because stride = 5
        output_shape = (math.floor(self.bounded_height / stride), math.floor(self.bounded_width / stride))
        output = np.zeros(output_shape, dtype=float)
        output_h = 0
        output_w = 0
        # Iterate over the point map using a stride of 5
        for h in range(50, self.bounded_height + 50, stride):
            for w in range(50, self.bounded_width + 50, stride):
                # The value at output[output_h, output_w] represents the density of agents at that point
                output[output_w, output_h] = self._scan_kernel(point_map, h, w)
                output_w += 1
            output_h += 1
            output_w = 0
        # Ensures that all values in the map are between 0 and 1 so that we can represent it as a single-channel image

        imgarray = self._normalize_density_map(output) * 255
        img = Image.fromarray(imgarray.astype('uint8'), 'L')
        img.save(filepath)

    @staticmethod
    def _make_circle_mask(radius=5):
        mask = np.zeros((radius * 2, radius * 2), dtype=int)
        for (h, w), _ in np.ndenumerate(mask):
            y = (h + 1) - 5
            x = (w + 1) - 5
            dist = math.sqrt(math.pow(y, 2) + math.pow(x, 2))
            if dist > 5:
                mask[h, w] = 1
        return mask

    @staticmethod
    def _add_circle_mask(output, x, y, mask):
        region = output[y:y + 10, x:x + 10]
        output[y:y + 10, x:x + 10] *= mask
        return output

    def _collect_data(self, output):
        circle_mask = self._make_circle_mask()
        new_output = output
        for agent in self.population:
            agent_position = agent.getPosition()
            x = int(agent_position[0])
            y = int(agent_position[1])
            new_output = self._add_circle_mask(output, x - 5, y - 5, circle_mask)
        return new_output

    def evaluate_trails(self, steps: int, skip=3, filepath="trails.png"):
        output = np.ones((500, 500), dtype=int)
        for i in range(steps * skip):
            self.step()
            if i % skip == 0:
                output = self._collect_data(output)
        output *= 255
        img = Image.fromarray(output.astype('uint8'), 'L')
        img.save("trails.png")

    def evaluate(
            self,
            steps: int,
            output_capture: OutputTensorConfig = None,
            screen=None,
            alternative_approach=None,
            save_to=None
    ):
        # Alternative approach query
        if alternative_approach == "density-map":
            self.evaluate_density_map(steps, filepath=save_to)
        if alternative_approach == "evaluate-trails":
            self.evaluate_trails(steps, filepath=save_to)

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



