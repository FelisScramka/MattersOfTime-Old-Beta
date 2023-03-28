import pygame, random, time, math, sys

#Init pygame
pygame.init()

import Assets.Images.Sprites.tiles as tiles
import Assets.Images.Sprites.animations as animations

import Assets.Sounds.Sfx.sounds as sounds

import Assets.Scripts.Classes.tilemap as tilemap
import Assets.Scripts.Classes.item as item
import Assets.Scripts.Classes.entity as entity
import Assets.Scripts.Classes.hitbox as hitbox
import Assets.Scripts.Classes.camera as camera
import Assets.Scripts.Classes.spark as spark

import Assets.Scripts.Utilities as utils

from pygame.math import Vector2

#Setup the window, display and clock |screen |display |clock
s_w= 960
s_h = 720
screen = pygame.display.set_mode((s_w, s_h))
display = pygame.Surface((s_w / 2, s_h / 2))

clock = pygame.time.Clock()
global dt
dt = 1

#Alternate textures |altTexture |alternateTexture |texture |init
BlankTexture = pygame.Surface((1, 1))
BlankTexture.fill((255, 255, 255))

BlueTexture = pygame.Surface((16, 16))
BlueTexture.fill((0, 0, 255))

GreenTexture = pygame.Surface((16, 16))
GreenTexture.fill((0, 255, 0))

GreenTexture = pygame.Surface((16, 16))
GreenTexture.fill((0, 255, 0))

TileTestTexture = pygame.Surface((32, 32))
TileTestTexture.fill((25, 0, 40))

a = []

#Real textures |officialTexture |texture |init
PlayerTexture = utils.loadImage("Sprites/Entities/Player/0r.png")
DirtTexture = utils.loadImage("Sprites/Tilesets/DirtSet/4.png")

#Create the player |player |init
_p_w = 28
_p_h = 42
p_w = _p_w
p_h = _p_h
p_dir = [0, 0]
Player = entity.Player(utils.scale(BlankTexture, (p_w, p_h)), 16, 16, 0, 0.34001) #0.34001

jumpBuffer = 0
_jumpBuffer = 7

wJumpBuffer = 0
_wJumpBuffer = 5

groundBuffer = 0
_groundBuffer = 7

Player.inventory.slots[0] = item.Pistol()
Player.inventory.slots[1] = item.SMG()
Player.inventory.slots[2] = item.Revolver()
Player.inventory.slots[3] = item.Bow()


Player.add_ani("idle", animations.p_idles)
Player.add_ani("run", animations.p_runs)

Player.add_ani("jump_up_0", [utils.loadImage("Sprites/Entities/Player/jump_up_0.png")])
Player.add_ani("jump_up_1", [utils.loadImage("Sprites/Entities/Player/jump_up_1.png")])
Player.add_ani("jump_down", [utils.loadImage("Sprites/Entities/Player/jump_down.png")])

Player.add_ani("wall", [utils.loadImage("Sprites/Entities/Player/wall.png")])

Player.add_ani("parachute", [utils.loadImage("Sprites/Entities/Player/parachute.png")])

grass_timer = 140

grounded = False
lgrounded = False
walled = False
ledged = False
parachute = False

#Create the map |map |init
t_w = 32
t_h = 32
Tilemap = tilemap.Tilemap(utils.loadImage("Maps/Cave1.png"), 0, 0, t_w, t_h)
Tilemap2 = tilemap.Tilemap(utils.loadImage("Maps/ParalaxCave1.png"), 0, 0, t_w, t_h)

tms = [Tilemap, Tilemap2]

#Add dirt set |tile |init
for tilemap in tms:
    tilemap.addType("Dirt", (255, 255, 255), tiles.dirt4)

    tilemap.addTile("Dirt", "DR", tiles.dirt0)
    tilemap.addTile("Dirt", "LDR", tiles.dirt1)
    tilemap.addTile("Dirt", "DL", tiles.dirt2)
    tilemap.addTile("Dirt", "TRD", tiles.dirt3)
    tilemap.addTile("Dirt", "F", tiles.dirt4)
    tilemap.addTile("Dirt", "DLT", tiles.dirt5)
    tilemap.addTile("Dirt", "TR", tiles.dirt6)
    tilemap.addTile("Dirt", "RTL", tiles.dirt7)
    tilemap.addTile("Dirt", "TL", tiles.dirt8)
    tilemap.addTile("Dirt", "IDR", tiles.dirt9)
    tilemap.addTile("Dirt", "IDL", tiles.dirt10)
    tilemap.addTile("Dirt", "T", tiles.dirt11)
    tilemap.addTile("Dirt", "ITR", tiles.dirt12)
    tilemap.addTile("Dirt", "ITL", tiles.dirt13)
    tilemap.addTile("Dirt", "TD", tiles.dirt14)
    tilemap.addTile("Dirt", "D", tiles.dirt15)
    tilemap.addTile("Dirt", "R", tiles.dirt16)
    tilemap.addTile("Dirt", "LR", tiles.dirt17)
    tilemap.addTile("Dirt", "L", tiles.dirt18)

    tilemap.addType("sDirt", (200, 200, 200), tiles.sdirt0, 1)

    tilemap.addTile("sDirt", "TL", tiles.sdirt0, [16, 16, 16, 16])
    tilemap.addTile("sDirt", "TR", tiles.sdirt1, [0, 16, 16, 16])
    tilemap.addTile("sDirt", "DL", tiles.sdirt2, [16, 0, 16, 16])
    tilemap.addTile("sDirt", "DR", tiles.sdirt3, [0, 0, 16, 16])

    tilemap.addType("Chain", (150, 150, 150), tiles.chain1, 0)

    tilemap.addTile("Chain", "D", tiles.chain0, [-1000, 0, 0, 0], 1)
    tilemap.addTile("Chain", "TD", tiles.chain1, [-1000, 0, 0, 0], 1)
    tilemap.addTile("Chain", "T", tiles.chain2, [-1000, 0, 0, 0], 1)

    tilemap.addTile("Chain", "E", tiles.chain1, [-1000, 0, 0, 0], 1)

#Write the map datas
Tilemap.write()
Tilemap2.write()

sprites = []

sprites.append(Player)
sprites.append(Tilemap)
sprites.append(Tilemap2)

Camera = camera.Camera([int(s_w / 2), int(s_h / 2)])
Camera.objs.append(Player)
Camera.objs.append(Tilemap)
cam_rot = 45
cam_zoom = 1
global fol_obj
fol_obj = Player

sparks = []

click_phase = 0

entities = []

pygame.mixer.pause()

def getCollideable(tilemap, obj, x = True, y = True):
    collides = []
    pos = (obj.hitbox.x + obj.vel[0] * int(x), obj.hitbox.y + obj.vel[1] * int(y))

    #X-axis
    for i in range(0, int(p_h - 1), 15):
        collides.append(tilemap.hitboxs[((pos[0] - 4) // 32, (pos[1] + i) // 32)])
        collides.append(tilemap.hitboxs[((pos[0] + obj.hitbox.w + 4) // 32, (pos[1] + i) // 32)])

    collides.append(tilemap.hitboxs[((pos[0] - 4) // 32, (pos[1] + obj.hitbox.h) // 32)])
    collides.append(tilemap.hitboxs[((pos[0] + obj.hitbox.w + 4) // 32, (pos[1] + obj.hitbox.h) // 32)])

    #Y-axis
    collides.append(tilemap.hitboxs[(pos[0] // 32, (pos[1] - 4) // 32)])
    collides.append(tilemap.hitboxs[(pos[0] // 32, (pos[1] + obj.hitbox.h + 4) // 32)])

    collides.append(tilemap.hitboxs[((pos[0] + obj.hitbox.w) // 32, (pos[1] - 4) // 32)])
    collides.append(tilemap.hitboxs[((pos[0] + obj.hitbox.w) // 32, (pos[1] + obj.hitbox.h + 4) // 32)])

    return collides

def shoot(Player, mouse_pos : Vector2, gun_type):
    if isinstance(Player.hand_item, gun_type):
        if Player.hand_item.shootable:
            shoot_x = (mouse_pos[0] - (Player.hitbox.x + Player.hitbox.w / 2 + scroll[0]) * 2)
            shoot_y = (mouse_pos[1] - (Player.hitbox.y + Player.hitbox.h / 2 + scroll[1]) * 2)
            Player.hand_item.shoot(Player.hitbox.x + Player.hitbox.w / 2, \
                                   Player.hitbox.y + Player.hitbox.h / 2, \
                                   (shoot_x / math.sqrt(shoot_x ** 2 + shoot_y ** 2) * 12 + Player.vel[0]) * Player.hand_item.speed, \
                                   (shoot_y / math.sqrt(shoot_x ** 2 + shoot_y ** 2) * 12) * Player.hand_item.speed)

def charge_bow(Player):
    global dt
    if isinstance(Player.hand_item, item.Bow):
        Player.hand_item.charge = min(Player.hand_item.charge + 1, Player.hand_item.max_charge)

def release_bow(Player, mouse_pos):
    if isinstance(Player.hand_item, item.Bow):
        shoot_x = (mouse_pos[0] - (Player.hitbox.x + Player.hitbox.w / 2 + scroll[0]) * 2)
        shoot_y = (mouse_pos[1] - (Player.hitbox.y + Player.hitbox.h / 2 + scroll[1]) * 2)
        Player.hand_item.shoot(Player.hitbox.x + Player.hitbox.w / 2, \
                               Player.hitbox.y + Player.hitbox.h / 3, \
                               (shoot_x / math.sqrt(shoot_x ** 2 + shoot_y ** 2) * 14 + Player.vel[0]) * Player.hand_item.speed, \
                               (shoot_y / math.sqrt(shoot_x ** 2 + shoot_y ** 2) * 14) * Player.hand_item.speed)

        Player.hand_item.charge = 0

def on_click(Player, mouse_pos):
    if click_phase == 0:
        shoot(Player, mouse_pos, item.FireArmGun)
    else:
        shoot(Player, mouse_pos, item.SMG)
        charge_bow(Player)

collideables = []

last_t = time.time()

def relus(n : int):
    return int(n > 0)

while True:
    mouse_pos = pygame.mouse.get_pos()

    dt = (time.time() - last_t) * 60
    last_t = time.time()
    
    #Fill resize screen a
    display.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click_phase = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if isinstance(Player.hand_item, item.Bow):
                    release_bow(Player, mouse_pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jumpBuffer = _jumpBuffer + min(max(Player.vel[1], 2), 4)
                if not grounded:
                    wJumpBuffer = _wJumpBuffer
            if event.key == pygame.K_t and not grounded and not walled:
                Player.vel[1] += 7.364
                Player.vel[0] *= 0.79
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and not walled:
                if Player.vel[1] < 0:
                    Player.vel[1] *= 0.8721
            if (event.key == pygame.K_a or event.key == pygame.K_d) and grounded:
                Player.vel[0] *= 0.64

    """
    a.append([Player.hitbox.x, Player.hitbox.y])

    for i in a:
        pygame.draw.circle(display, (255, 0, 0), i, 1)
    """

    #pygame.draw.circle(display, (255, 0, 0), camera, 1)
    #pygame.draw.circle(display, (0, 255, 0), (s_w / 4, s_h / 4), 1)
    
    walled = 0

    collideables = getCollideable(Tilemap, Player, True, False)

    lgrounded = grounded

    #Collision resolve for x
    Player.move_x(dt)
    for hb in collideables:
        collide = hb.collide(Player.hitbox)
        if collide:
            if Player.vel[0] < 0:
                Player.hitbox.x = hb.x + hb.w
                walled = -1 if not parachute else 0
            else:
                Player.hitbox.x = hb.x - Player.hitbox.w
                walled = 1 if not parachute else 0
            Player.vel[0] *= 0.874

    collideables = getCollideable(Tilemap, Player, False, True)

    grounded = False

    #Collision resolve for y
    Player.move_y(dt)
    for hb in collideables:
        collide = hb.collide(Player.hitbox)
        if collide:
            if Player.vel[1] < 0:
                Player.vel[1] = -0.024
                Player.hitbox.y = hb.y + hb.h
            else:
                Player.vel[1] = 0.024
                Player.hitbox.y = hb.y - Player.hitbox.h
                grounded = True

    #Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and walled != -1:
        accelx = (0.88842 - int(not(grounded)) * 0.373)
        Player.vel[0] = Player.vel[0] * (0.42 if Player.vel[0] >= 0 else 1)
        Player.vel[0] -= accelx if Player.vel[0] - accelx >= -4.3 else 0
    if keys[pygame.K_d] and walled != 1:
        accelx = (0.88842 - int(not(grounded)) * 0.373)
        Player.vel[0] = Player.vel[0] * (0.42 if Player.vel[0] <= 0 else 1)
        Player.vel[0] += accelx if Player.vel[0] + accelx <= 4.3 else 0
    if keys[pygame.K_f] and not walled:
        if Player.dashable:
            p_side = (1 if Player.vel[0] > 0 else -1)
            
            dash_velx = 8.13413998697 * int(not bool(abs(Player.vel[0]) < 0.858)) * p_side + (0.361 * relus(grounded) * p_side) + (0.01 * relus(walled) * p_side)
            dash_vely = -0.83786337995 * int(not(grounded)) + abs(Player.vel[1]) / -4.246
            
            Player.dash(dash_velx, dash_vely)

            sounds.dash.play()
    if pygame.mouse.get_pressed()[2] and not grounded and not walled:
        if Player.vel[1] > 0:
            Player.vel[1] *= 0.924
        else:
            Player.vel[1] *= 0.994
        Player.vel[0] *= 0.924
        parachute = True
    else:
        parachute = False
    if keys[pygame.K_a] or keys[pygame.K_d]:
        if grounded:
            grass_timer -= abs(Player.vel[0])
        else:
            grass_timer = 75
        if Player.act != "run":
            Player.set_act("run")
    else:
        grass_timer = 75
        if Player.act != "idle":
            Player.set_act("idle")

    #Apply physics
    if grounded:
        groundBuffer = _groundBuffer
        Player.vel[0] -= Player.vel[0] * dt *0.1212
        if lgrounded == False:
            Player.vel[0] *= 0.9

    if walled:
        if Player.vel[1] > 0:
            Player.vel[1] *= 0.9162
        else:
            Player.vel[1] *= 0.971
        Player.vel[0] += walled * 0.02

    Player.apply_air_res(0.9236, 0.993)

    #Mouse presses

    if pygame.mouse.get_pressed()[0]:
        on_click(Player, mouse_pos)
        click_phase = 1

    if grass_timer < 0:
        grass_timer = 75
        random.choice(sounds.dirts).play()

    jumpBuffer = max(jumpBuffer - 1, 0)
    wJumpBuffer = max(wJumpBuffer - 1, 0)
    groundBuffer = max(groundBuffer - 1, 0)
    
    if groundBuffer > 0:
        if _jumpBuffer > jumpBuffer and jumpBuffer > 0:
            jumpBuffer = 0
            groundBuffer = 0
            Player.vel[1] = -8.54421
            Player.vel[0] *= 1.023
            Player.dashable = False
            Player.dash_tick = 48

            sounds.jump.play()
        if Player.vel[1] > 0:
            Player.vel[1] *= 0.992

    if wJumpBuffer > 0 and walled:
        wJumpBuffer = 0
        Player.walljump(Player.vel[0], -7.83)
        Player.dash_tick += 24

    #Hotbar input
    if keys[pygame.K_1]:
        Player.switch_slot(0)
    if keys[pygame.K_2]:
        Player.switch_slot(1)
    if keys[pygame.K_3]:
        Player.switch_slot(2)
    if keys[pygame.K_4]:
        Player.switch_slot(3)

    if not grounded:
        if Player.vel[1] > 1.5:
            if Player.act != "jump_down":
                Player.set_act("jump_down")
        elif 0.1 > Player.vel[1] and Player.vel[1] > -0.06:
            if Player.act != "idle":
                Player.set_act("idle")
                Player.vel[1] *= 0.98979
                Player.vel[0] *= 1.09192
        elif -7 > Player.vel[1]:
            if Player.act != "jump_up_0":
                Player.set_act("jump_up_0")
        elif -1 > Player.vel[1]:
            if Player.act != "jump_up_1":
                Player.set_act("jump_up_1")
        elif -0.1 >= Player.vel[1] and Player.vel[1] >= -1:
            if Player.act != "jump_up_0":
                Player.set_act("jump_up_0")
        else:
            if Player.act != "idle":
                Player.set_act("idle")

    if walled and not grounded:
        if Player.act != "wall":
            Player.set_act("wall")

    if parachute:
        if Player.act != "parachute":
            Player.set_act("parachute")

    p_dir[0] = -1 if Player.vel[0] > 0 else 1
    p_dir[1] = -1 if Player.vel[1] > 0 else 1

    p_w = _p_w + abs(Player.vel[0] * 1.2) - min(abs(Player.vel[1] * 1.2), 8)
    p_h = _p_h - abs(Player.vel[0] * 1.16) + min(abs(Player.vel[1]), 8)

    Player.update()
    Player.ani()

    mouse_angle = math.degrees(math.atan2(mouse_pos[1] - Player.hitbox.y - 8, mouse_pos[0] - Player.hitbox.x - 8))

    if isinstance(Player.hand_item, item.Gun):
        offset = 0
        for i, proj in enumerate(Player.hand_item.projs):
            proj.update()
            if proj.alive == False:
                Player.hand_item.projs.pop(i)

            proj.move_x(dt)
            proj.move_y(dt)
            proj.apply_air_res(0.994, 0.994)

            proj.draw(display, scroll)

            for hb in Tilemap.hitboxs.values():
                if hb.collide(hitbox.Hitbox(proj.hitbox.x + proj.vel[0], proj.hitbox.y + proj.vel[1], proj.hitbox.w, proj.hitbox.h)):
                    try:
                        Player.hand_item.projs.pop(i)
                        sparks.append(spark.Spark(proj.hitbox.x + proj.hitbox.w / 2, \
                                                      proj.hitbox.y + proj.hitbox.h / 2, \
                                                      math.atan2(proj.vel[0], proj.vel[1]) + random.uniform(-0.24, 0.24), \
                                                      1.8, \
                                                      (255, 255, 255)))
                    except:
                        pass

    #Update the map
    #Tilemap2.draw(display, (scroll[0] * 0.82, scroll[1] * 0.96))

    #Iterate through sparks and draw them
    for i, sp in enumerate(sparks):
        sp.move()
        if not sp.alive:
            sparks.pop(i)
        sp.draw(display, scroll)

    #for hb in collideables:
    #    pygame.draw.rect(display, (255, 0, 0), pygame.Rect(hb.x + scroll[0], hb.y + scroll[1], hb.w, hb.h))

    #Player.draw(display, [scroll[0] + (_p_w - p_w) / 2, scroll[1] + (_p_h - p_h)], [p_w, p_h])

    Camera.follow(fol_obj, 0.148)
    Camera.render(display)

    #Player.draw_hand(display, scroll)

    #Blit resize screen
    edit_dis = pygame.transform.scale(display, (s_w, s_h))
    screen.blit(edit_dis, (0, 0))

    pygame.display.set_caption(f"Sawblade - {int(clock.get_fps())}")

    """
    for y in range(screen.get_height()):
        for x in range(screen.get_width()):
            if screen.get_at((x, y)) == (36, 8, 43):
                screen.set_at((x, y), (0, 255, 0))
    """

    #Update the screen
    clock.tick(60)
    pygame.display.update()
