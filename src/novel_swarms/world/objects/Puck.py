import pygame
import pymunk
from pymunk import Vec2d

def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return y

class Puck:
    def __init__(self, x, y, radius, color, mass=100, moment=100):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.moment = moment
        self.color = color
        self.body = pymunk.Body(mass, moment)
        self.body.position = [x, y]
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.friction = 2.0
        self.shape.collision_type = 2

    def draw(self, screen):
        r = self.radius
        v = self.body.position
        rot = self.body.rotation_vector
        p = int(v.x), int(flipy(v.y))
        p2 = p + Vec2d(rot.x, -rot.y) * r * 0.9
        p2 = int(p2.x), int(p2.y)
        pygame.draw.circle(screen, self.color, p, int(r), 0)

    def step(self):
        self.body.velocity *= 0.99  # Naturally Decelerate if in motion (friction)
