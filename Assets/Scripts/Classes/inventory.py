import pygame
import Assets.Scripts.Classes.item as Item

RedTexture = pygame.Surface((16, 16))
RedTexture.fill((255, 0, 0))

BlueTexture = pygame.Surface((16, 16))
BlueTexture.fill((0, 255, 0))

class Inventory():
    def __init__(self, row, col):
        self._row = row
        self._col = col
        self.slots = []
        for i in range (1, row * col):
            self.slots.append(Item.Air)
    def getSlot(self, i):
        return self.slots[i]
    def setSlot(self, i, value):
        self.slots[i] = value
