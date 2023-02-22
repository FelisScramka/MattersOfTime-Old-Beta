import pygame

#Load image
def loadImage(name):
    return pygame.image.load(f"Assets/Images/{name}")

#Scale image
def scale(image, scale):
    return pygame.transform.scale(image, scale)
