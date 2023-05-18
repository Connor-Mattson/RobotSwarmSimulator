import pygame
import numpy as np
from src.novel_swarms.util.collider.CircularCollider import CircularCollider


class AbstractGoal:
    def __init__(self):
        pass

    def draw(self, screen):
        pass

    def agent_achieved_goal(self, agent):
        pass


class AreaGoal(AbstractGoal):
    def __init__(self, x, y, w, h, color=(0, 255, 0), remove_agents_at_goal=False):
        super().__init__()
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


class CylinderGoal(AbstractGoal):
    def __init__(self, x, y, r, color=(0, 255, 0), range=100, remove_agents_at_goal=False):
        super().__init__()
        self.center = [x, y]
        self.r = r
        self.color = color
        self.remove_at = remove_agents_at_goal
        self.agents_seen = set()
        self.range = range

    def draw(self, screen):
        # Draw Inclusive Range
        pygame.draw.circle(screen, (0, 50, 0), self.center, self.range, width=0)
        pygame.draw.circle(screen, self.color, self.center, self.r, width=0)

    def agent_achieved_goal(self, agent):
        if np.linalg.norm(agent.getPosition() - np.array(self.center)) < self.range:
            return True
        return False

    def add_achieved_agent(self, agent_id):
        self.agents_seen.add(agent_id)

    def get_count(self):
        return len(self.agents_seen)

    def get_collider(self):
        return CircularCollider(self.center[0], self.center[1], self.r)

    def as_config_dict(self):
        return {
            "type": "CylinderGoal",
            "center": self.center,
            "r": self.r,
            "color": self.color,
            "remove_at": self.remove_at,
            "range": self.range
        }
