import pygame

def load(name):
    return pygame.mixer.Sound(name)

dirts = [load("Assets/Sounds/Sfx/DirtStep/0.wav"), load("Assets/Sounds/Sfx/DirtStep/1.wav"), load("Assets/Sounds/Sfx/DirtStep/2.wav")]
for sfx in dirts:
    sfx.set_volume(0.1)

dash = load("Assets/Sounds/Sfx/Dash/0.wav")
dash.set_volume(0.68)

jump = load("Assets/Sounds/Sfx/DirtStep/0.wav")
jump.set_volume(0.1)
