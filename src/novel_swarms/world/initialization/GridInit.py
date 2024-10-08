import pygame

from src.novel_swarms.world.initialization.AbstractInit import AbstractInitialization
from src.novel_swarms.world.World import World
import numpy as np
from typing import Tuple, Iterable


class GridInitialization(AbstractInitialization):
    """
    RandomInitialization: A random initialization of the agents in the environment.
    """

    def __init__(self, num_agents: int, grid_size: Tuple[int, int], bb: Tuple[Tuple] = None):
        """
        Initialize the RandomInitialization Class
        @params
        num_agents: The number of agents present in the simulation (int, required)
        bb: A Bounding box of the form ((x1, y1), (x2, y2)), where x1 and y1 are the Upper Left corner and
            x2, y2 are the Bottom Right corner.
        """
        super().__init__()
        self.num_agents = num_agents
        self.grid_size = grid_size
        self.bb = bb

        # Store the initialization information in an iterable
        self.grid_positions = []
        self.positions = []


        # Determine Positions, but don't set them until the user explicitly calls 'set_to_world' method
        self._calculate_positions()

    def _calculate_positions(self):
        """
        Using the bounding box (self.bb) information, randomly sample positions from the rectangle, and orientations from the range [0, 2pi].
        """
        spawn_w, spawn_h = self.bb[1][0] - self.bb[0][0], self.bb[1][1] - self.bb[0][1]
        n, m = self.grid_size[0], self.grid_size[1]

        self.grid_positions = np.array([
            (((spawn_w / n) * (i + 0.5)) + self.bb[0][0], ((spawn_h / m) * (j + 0.5)) + self.bb[0][1], np.random.random() * np.pi * 2) for i in range(n) for j in range(m)
        ])

        indices = np.random.choice(len(self.grid_positions), size=self.num_agents, replace=False)
        self.positions = self.grid_positions[indices][:self.num_agents]

    def draw(self, screen):
        # for g in self.grid_positions:
        #     pygame.draw.circle(screen, (120, 120, 120), (g[0], g[1]), 5)
        pass
