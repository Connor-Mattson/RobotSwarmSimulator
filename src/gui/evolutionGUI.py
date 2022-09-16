import pygame
from ..novelty.BehaviorDiscovery import BehaviorDiscovery
from .abstractGUI import AbstractGUI
from ..world.World import World

class EvolutionGUI(AbstractGUI):

    # Pair the GUI to the World
    world = None
    discovery = None
    title = None
    subtitle = None
    generation_time = None
    text_baseline = 10

    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__(x=x, y=y, w=w, h=h)

    def set_title(self, title, subtitle=None):
        self.title = title
        self.subtitle = subtitle

    def set_world(self, world: World):
        self.world = world

    def set_discovery(self, discovery: BehaviorDiscovery):
        self.discovery = discovery

    def set_elapsed_time(self, time):
        self.generation_time = time

    def draw(self, screen):
        super().draw(screen)
        self.text_baseline = 10
        if pygame.font:
            if(self.title):
                self.appendTextToGUI(screen, self.title, size=20)
            if(self.subtitle):
                self.appendTextToGUI(screen, self.subtitle, size=18)
            if(self.discovery):
                self.appendTextToGUI(screen, "")
                self.appendTextToGUI(screen, f"State: {self.discovery.status}")
                self.appendTextToGUI(screen, f"Generation: {self.discovery.curr_generation}")
                self.appendTextToGUI(screen, f"Population Index: {self.discovery.curr_genome}")
                self.appendTextToGUI(screen, "")
                self.appendTextToGUI(screen, "Best Score (Last Gen): {:0.4f}".format(self.discovery.getBestScore()))
                self.appendTextToGUI(screen, "Avg Score (Last Gen): {:0.4f}".format(self.discovery.getAverageScore()))
                self.appendTextToGUI(screen, f"Crossovers: {self.discovery.crossovers}")
                self.appendTextToGUI(screen, f"Mutations: {self.discovery.mutations}")
                self.appendTextToGUI(screen, "")
                self.appendTextToGUI(screen, f"Archive Size: {len(self.discovery.archive.archive)}")
            if self.generation_time:
                self.appendTextToGUI(screen, "")
                self.appendTextToGUI(screen, "Comp Time: {:0.2f}s".format(self.generation_time))
        else:
            print("NO FONT")

    def appendTextToGUI(self, screen, text, x = None, y = None, color=(255, 255, 255), aliasing=True, size=16):

        if not x:
            x = self.x + 10
        if not y:
            y = self.text_baseline

        font = pygame.font.Font(None, size)
        text = font.render(text, aliasing, color)
        textpos = (x, y)
        screen.blit(text, textpos)
        self.text_baseline += size + 1