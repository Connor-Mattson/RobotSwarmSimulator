import pygame

class AreaGoal:
    def __init__(self, x, y, w, h, color=(0, 255, 0), remove_agents_at_goal = False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.remove_at = remove_agents_at_goal
        self.agents_seen = set()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, width=0)

    def agent_achieved_goal(self, agent):
        pos = [agent.x_pos, agent.y_pos]
        return self.rect.collidepoint(pos)

    def add_achieved_agent(self, agent_id):
        self.agents_seen.add(agent_id)

    def get_count(self):
        return len(self.agents_seen)
