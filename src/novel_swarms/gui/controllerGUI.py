import math

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
        self.show_compass = True

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

    def pass_key_events(self, event):
        if event.type == pygame.KEYDOWN:
            c = self.world.population[0].controller
            v = c[self.selected_c]
            if event.key == pygame.K_COMMA:
                # v = max(-1.0, v - 0.1)
                v = v - 0.1
                self.set_controller_v(v)
            if event.key == pygame.K_PERIOD:
                # v = min(1.0, v + 0.1)
                v = v + 0.1
                self.set_controller_v(v)
            if event.key == pygame.K_a:
                self.selected_c = 0
            if event.key == pygame.K_s:
                self.selected_c = 1
            if event.key == pygame.K_d:
                self.selected_c = 2
            if event.key == pygame.K_f:
                self.selected_c = 3

    def set_controller_v(self, v):
        for i in range(len(self.world.population)):
            self.world.population[i].controller[self.selected_c] = v

    def draw(self, screen):
        super().draw(screen)
        self.text_baseline = 10
        c = self.world.population[0].controller
        if pygame.font:
            if self.title:
                self.appendTextToGUI(screen, self.title, size=20)
            if self.subtitle:
                self.appendTextToGUI(screen, self.subtitle, size=18)

            self.appendTextToGUI(screen, f"Timesteps: {self.time}")

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

        if self.show_compass:
            r = self.w / 3
            center = (self.x + (self.w / 2), self.text_baseline + r + 10)
            pygame.draw.circle(screen, (255, 255, 255), center, r, width=3)

            BL = 7
            v_on = ((c[2] + c[3]) / 2)
            w_on = ((c[3] - c[2]) / BL)

            v_off = ((c[0] + c[1]) / 2)
            w_off = ((c[1] - c[0]) / BL)

            m_v = max(abs(v_on), abs(v_off))
            v_on *= r / m_v
            v_off *= r / m_v

            d_on = (math.cos(w_on + (math.pi / 2)) * v_on, math.sin(w_on + (math.pi / 2)) * v_on)
            d_off = (math.cos(w_off + (math.pi / 2)) * v_off, math.sin(w_off + (math.pi / 2)) * v_off)

            p_on = (d_on[0] + center[0], d_on[1] + center[1])
            p_off = (d_off[0] + center[0], d_off[1] + center[1])

            pygame.draw.line(screen, (255, 0, 0), center, p_on, width=5)
            pygame.draw.line(screen, (0, 255, 0), center, p_off, width=5)


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
