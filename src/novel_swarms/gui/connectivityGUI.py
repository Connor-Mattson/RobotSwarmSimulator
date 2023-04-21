import pygame
from ..agent.DiffDriveAgent import DifferentialDriveAgent
from .abstractGUI import AbstractGUI
from ..world.World import World
import numpy as np


class AgentConnectivityGUI(AbstractGUI):
    # Pair the GUI to the World
    world = None
    title = None
    subtitle = None
    selected = None
    text_baseline = 10

    def __init__(self, x=0, y=0, w=0, h=0, n=10):
        super().__init__(x=x, y=y, w=w, h=h)
        self.time = 0
        self.n = n

    def set_selected(self, agent: DifferentialDriveAgent):
        super().set_selected(agent)
        self.selected = agent

    def set_title(self, title, subtitle=None):
        self.title = title
        self.subtitle = subtitle

    def set_world(self, world: World):
        self.world = world

    def set_time(self, time_steps):
        self.time = time_steps

    def draw(self, screen):
        super().draw(screen)
        self.text_baseline = 10
        if pygame.font:
            if self.title:
                self.appendTextToGUI(screen, self.title, size=20)
            if self.subtitle:
                self.appendTextToGUI(screen, self.subtitle, size=18)

            self.appendTextToGUI(screen, f"Timesteps: {self.time}")

        else:
            print("NO FONT")

        if not self.world:
            return

        center = self.x + (self.w // 2), self.y + ((self.h // 2) - self.text_baseline)
        radius = self.w // 3
        node_radius = 8

        angles = [(2 * np.pi / self.n) * i for i in range(self.n)]
        positions = [(center[0] + (radius * np.cos(angle)), center[1] + (radius * np.sin(angle))) for angle in angles]

        for i, position in enumerate(positions):
            pygame.draw.circle(screen, (255, 255, 255), position, node_radius, 0)

        for i, agent in enumerate(self.world.population):
            if agent.agent_in_sight:
                j = int(agent.agent_in_sight.name)
                pygame.draw.line(screen, (255, 255, 255), positions[i], positions[j])


    def appendTextToGUI(self, screen, text, x=None, y=None, color=(255, 255, 255), aliasing=True, size=16):

        if not x:
            x = self.x + 10
        if not y:
            y = self.text_baseline

        font = pygame.font.Font(None, size)
        text = font.render(text, aliasing, color)
        textpos = (x, y)
        screen.blit(text, textpos)
        self.text_baseline += size + 1
