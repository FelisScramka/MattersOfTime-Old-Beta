import pygame

offset = 0
size = 32

image = input("Enter name of the image that you wanna chop: ") + ".png"
name = input("Enter your output file name: ")

def slice(surface, x_size, y_size):
    sprites = []
    for y in range(surface.get_height() // y_size):
        for x in range(surface.get_width() // x_size):
            sprites.append(clip(surface, x * x_size, y * y_size, x_size, y_size))
    return sprites

def clip(surface, x, y, x_size, y_size):
    handle_surface = surface.copy()
    clipRect = pygame.Rect(x,y,x_size,y_size)
    handle_surface.set_clip(clipRect)
    image = surface.subsurface(handle_surface.get_clip())
    return image.copy()

for index, sprite in enumerate(slice(pygame.image.load(image), 16, 16)):
    pixels = []
    save = True
    convertSurf = pygame.Surface((sprite.get_width(), sprite.get_height()))
    convertSurf.blit(sprite, (0, 0))
    for y in range(convertSurf.get_height()):
        for x in range(convertSurf.get_width()):
            pixels.append(convertSurf.get_at((x, y)))
    for pixel in pixels:
        if pixel == (0, 0, 0):
            save = False
        else:
            save = True
            break
    if save:
        pygame.image.save(pygame.transform.scale(sprite, (size, size)), f"DirtSet/{name}{index - offset}.png")
    else:
        offset += 1
