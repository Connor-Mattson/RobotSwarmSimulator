from .AbstractBehavior import AbstractBehavior
import numpy as np
from ripser import ripser
import pygame

class PersistentHomology(AbstractBehavior):
    def __init__(self, history_size=100, dims=0, draw_cycles=False, max_death=False):
        super().__init__(name=f"{dims}D Elements", history_size=history_size)
        self.population = []
        self.pointset = []
        self.rips_data = None
        self.dims = dims
        self.draw_cycles = draw_cycles
        self.max_death = max_death

    def attach_world(self, world):
        self.population = world.population

    def calculate(self):
        try:
            self.pointset = np.array([[p.x_pos, p.y_pos] for p in self.population])
            self.rips_data = ripser(self.pointset, maxdim=self.dims + 1, do_cocycles=True)
            dgms = self.rips_data["dgms"]

            if self.max_death and len(dgms[-1]) > 0:
                death_max_values = np.max(dgms[-1], axis=0)
                max_v = death_max_values[1]
                self.set_value(max_v)
            else:
                self.set_value(len(dgms[-1]))
        except Exception as e:
            print(f"Persistent Homology Error: {e}")
            self.set_value(np.nan)

    def draw(self, screen):
        if self.draw_cycles:
            cocycles = self.rips_data["cocycles"]
            color = (255, 0, 255) if self.dims == 0 else (255, 0, 0)
            if len(cocycles[-1]) > 0:
                for cycle in cocycles[-1]:
                    for step in cycle:
                        width, step = step[-1], step[:-1]
                        for i in range(len(step)):
                            agent_i, agent_j = self.population[step[i]], self.population[step[len(step) % (i + 1)]]
                            pygame.draw.line(screen, color, agent_i.getPosition(), agent_j.getPosition(), width)
