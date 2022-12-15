import pygame
from pygame import Rect

class AbstractGUI:

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def set_selected(self, agent):
        #print("Attaching New Agent")
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, color=(10,10,10), rect=Rect((self.x, self.y),(self.w, self.h)))