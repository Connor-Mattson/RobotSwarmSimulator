import pygame
from ..agent.DiffDriveAgent import DifferentialDriveAgent
from .abstractGUI import AbstractGUI
from ..world.World import World


class ControllerGUI(AbstractGUI):
    # Pair the GUI to the World
    world = None
    title = None
    subtitle = None
    selected = None
    text_baseline = 10

    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__(x=x, y=y, w=w, h=h)
        self.time = 0
        self.selected_c = 0

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

    def step(self):
        # super().step()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                c = self.world.population[0].controller
                v = c[self.selected_c]
                if event.key == pygame.K_COMMA:
                    v = max(-1.0, v - 0.05)
                if event.key == pygame.K_PERIOD:
                    v = min(1.0, v + 0.05)                
                for i in range(len(self.world.population)):
                    self.world.population[i].controller[self.selected_c] = v

    def draw(self, screen):
        super().draw(screen)
        self.text_baseline = 10
        if pygame.font:
            if self.title:
                self.appendTextToGUI(screen, self.title, size=20)
            if self.subtitle:
                self.appendTextToGUI(screen, self.subtitle, size=18)

            self.appendTextToGUI(screen, f"Timesteps: {self.time}")
            
            c = self.world.population[0].controller
            self.appendTextToGUI(screen, f"L0: {c[0]}")
            self.appendTextToGUI(screen, f"R0: {c[1]}")
            self.appendTextToGUI(screen, f"L1: {c[2]}")
            self.appendTextToGUI(screen, f"R1: {c[3]}")

            self.appendTextToGUI(screen, "")
            self.appendTextToGUI(screen, f"Selected Elem: {self.selected_c}")
            self.appendTextToGUI(screen, "Press . to increase value by 0.05")
            self.appendTextToGUI(screen, "Press , to decrease value by 0.05")

        else:
            print("NO FONT")

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
