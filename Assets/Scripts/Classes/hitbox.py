import pygame
from pygame.math import Vector2

class Hitbox():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def collide(self, hitbox):
        if (self.x < hitbox.x + hitbox.w) & \
            (self.x + self.w > hitbox.x) & \
            (self.y < hitbox.y + hitbox.h) & \
            (self.y + self.h > hitbox.y):
            return True
        return False
