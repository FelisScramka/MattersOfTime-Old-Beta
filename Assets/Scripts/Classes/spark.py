import pygame, math
from pygame.math import Vector2

from Assets.Scripts.Classes.hitbox import Hitbox

class Spark():
    def __init__(self, x, y, angle, speed, color, scale = 1):
        self.hitbox = Hitbox(x, y, 1, 1)
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True

    def point_towards(self, angle, rate):
        rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sign = 1
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self):
        return [math.cos(self.angle + math.pi) * self.speed, math.sin(self.angle) * self.speed]

    def move(self):
        movement = self.calculate_movement()
        self.hitbox.y += movement[0]
        self.hitbox.x += movement[1]

        self.speed *= 0.91

        if self.speed <= 0.06:
            self.alive = False

    def draw(self, screen, offset = [0, 0]):
        if self.alive:
            points = [
                [self.hitbox.x + math.cos(self.angle + math.pi / 2) * self.speed * self.scale + offset[0], self.hitbox.y + math.sin(self.angle + math.pi / 2) * self.speed * self.scale + offset[1]],
                [self.hitbox.x + math.cos(self.angle + math.pi) * self.speed * self.scale * 0.3 + offset[0], self.hitbox.y + math.sin(self.angle + math.pi) * self.speed * self.scale * 0.3 + offset[1]],
                [self.hitbox.x - math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 3.5 + offset[0], self.hitbox.y - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 3.5 + offset[1]],
                [self.hitbox.x + math.cos(self.angle - math.pi) * self.speed * self.scale * 0.3 + offset[0], self.hitbox.y - math.sin(self.angle + math.pi) * self.speed * self.scale * 0.3 + offset[1]],
                ]
            pygame.draw.polygon(screen, self.color, points)
