import pygame

class AreaGoal:
    def __init__(self, x, y, w, h, color=(0, 255, 0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, width=0)

    def agent_achieved_goal(self, agent):
        pos = [agent.x_pos, agent.y_pos]
        return self.rect.collidepoint(pos)