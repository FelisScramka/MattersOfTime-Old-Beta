from pygame.math import Vector2
import pygame

class Camera():
    def __init__(self, size : list):
        self.pos = Vector2()
        self.surface = pygame.Surface(size)
        self.size = size
        self.objs = []

    def follow(self, obj, intensity : float):
        dist = Vector2(self.size[0] / 2 - obj.hitbox.x - self.pos.x, self.size[1] / 2 - obj.hitbox.y - self.pos.y)
        self.pos += (dist * intensity)

    def render(self, surface : pygame.Surface):
        for obj in self.objs:
            obj.draw(surface, self.pos)
