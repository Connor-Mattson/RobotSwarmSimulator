import pygame
from pygame import Rect

class AbstractGUI:

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.track_all_events = False
        self.track_all_mouse = False

    def set_selected(self, agent):
        #print("Attaching New Agent")
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, color=(10,10,10), rect=Rect((self.x, self.y),(self.w, self.h)))

    def recieve_events(self, events):
        pass

    def recieve_mouse(self, mouse_rel):
        pass

    def set_screen(self, screen):
        self.screen = screen

    def set_world(self, world):
        pass

    def set_time(self, time):
        pass

    def step(self):
        pass

    def pass_key_events(self, events):
        pass
