import pygame
import random
import math
from src.agent.Agent import Agent

class DifferentialDriveAgent(Agent):
    
    def __init__(self) -> None:
        super().__init__(random.randint(0, 500), random.randint(0, 500))
        self.radius = 5
        self.angle = 0

    def step(self, check_for_world_boundaries = None) -> None:
        super().step()
        self.x_pos += random.randint(-1, 1)
        self.y_pos += random.randint(-1, 1)
        self.angle += random.randint(-1, 5) * math.pi / 180

        if check_for_world_boundaries != None:
            check_for_world_boundaries(self)

    def draw(self, screen) -> None:
        super().draw(screen)

        # Draw Cell Membrane
        pygame.draw.circle(screen, (255, 255, 255), (self.x_pos, self.y_pos), self.radius, width=1)
        
        # Draw Sensory Vector (Vision Vector)
        mangitude = 7
        head = (self.x_pos, self.y_pos)
        tail = (self.x_pos + (mangitude * math.cos(self.angle)), self.y_pos + (mangitude * math.sin(self.angle)))
        pygame.draw.line(screen, (255, 0, 0), head, tail)
