import pygame


class ClusterPoint:
    def __init__(self, x, y, color=(255, 255, 255), genome=None):

        if genome is None:
            genome = []

        self.x = x
        self.y = y
        self.color = color
        self.radius = 1
        self.genome = genome
        self.is_highlighted = False

    def draw(self, screen):
        filled = 0 if self.is_highlighted else 1
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, width=filled)

    def getGenome(self):
        return self.genome
