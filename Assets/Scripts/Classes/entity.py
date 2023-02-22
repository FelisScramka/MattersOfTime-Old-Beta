import pygame

from pygame.math import Vector2
from Assets.Scripts.Classes.hitbox import Hitbox
from Assets.Scripts.Classes.inventory import Inventory
import Assets.Scripts.Classes.goal as goal
import Assets.Scripts.Classes.item as item

class Entity():
    #Init the entity
    def __init__(self, sprite, x, y, grav_x = 0, grav_y = 0):
        self.sprite = sprite
        
        self.grav = [grav_x, grav_y]
        self.vel = [0, 0]
        self.hitbox = Hitbox(x, y, sprite.get_width(), sprite.get_height())

        self.act = "idle"
        self.anis = {"idle": [sprite]}
        self.ani_i = 0

    #Move the entity horizontally
    def move_x(self, dt):
        self.vel[0] += self.grav[0]
        self.hitbox.x += self.vel[0] * dt

    #Move the entity vertically
    def move_y(self, dt):
        self.vel[1] += self.grav[1]
        self.hitbox.y += self.vel[1] * dt

    def apply_air_res(self, rat_x, rat_y):
        self.vel[0] *= rat_x
        self.vel[1] *= rat_y

    #Draw the entity
    def draw(self, screen, offset = [0, 0], scale = [-1, -1], flip = True):
        try:
            image = self.anis[self.act][self.ani_i]
        except:
            image = self.sprite
        image = pygame.transform.scale(image, scale) if scale[0] > 0 and scale[1] > 0 else self.sprite
        if flip == True:
            if self.vel[0] < 0:
                image = pygame.transform.flip(image, True, False)
        screen.blit(image, (self.hitbox.x + offset[0], self.hitbox.y + offset[1]))

    def add_ani(self, act, sprites):
        self.anis[act] = sprites

    def ani(self):
        self.ani_i = (self.ani_i + 1) % len(self.anis[self.act])

    def set_act(self, act):
        if act in self.anis:
            self.act = act
        else:
            self.act = "idle"
        self.ani_i = 0

class LivingEntity(Entity):
    def __init__(self, sprite, x, y, grav_x = 0, grav_y = 0):
        super(LivingEntity, self).__init__(sprite, x, y, grav_x, grav_y)
        
        self.max_health = 20
        self.health = 20

        self.max_mana = 80
        self.mana = 80

        self.exhaustion = 20

class Enemy(LivingEntity):
    def __init__(self, sprite, x, y, grav_x = 0, grav_y = 0):
        super(Enemy, self).__init__(sprite, x, y, grav_x, grav_y)
        self.goals = []
    def update(self):
        for g in self.goals:
            if g == goal.Move:
                g.update()

class Projectile(Entity):
    def __init__(self, sprite, x, y, life_time = 60, grav_x = 0, grav_y = 0):
        super(Projectile, self).__init__(sprite, x, y, grav_x, grav_y)

        self.damage = 0;
        self.knockback = 0.01;

        self.tick = 0
        self.live_time = life_time

        self.alive = True

    def set_vel(self, x, y):
        self.vel[0] = x
        self.vel[1] = y

    def update(self):
        self.tick += 1
        if self.tick > self.live_time:
            self.alive = False
            self.tick = 0
        

class Player(LivingEntity):
    #Init the player
    def __init__(self, sprite, x, y, grav_x = 0, grav_y = 0):
        super(Player, self).__init__(sprite, x, y, grav_x, grav_y)
        
        self.dashable = True
        self.dash_tick = 0

        self.walljumpable = True
        self.walljump_tick = 0

        self.inventory = Inventory(6, 9)
        self.sel_slot = 1
        self.hand_item = self.inventory.getSlot(self.sel_slot)

        self.alive = True

    #Dash
    def dash(self, x, y):
        if self.dashable == True:
            self.vel[0] += x
            self.vel[1] += y
            self.dashable = False

    def walljump(self, x, y):
        if self.walljumpable == True:
            self.vel[0] = x
            self.vel[1] = y
            self.walljumpable = False

    #Draw the hand
    def draw_hand(self, screen, offset = [0, 0], rotation = 0):
        sprite = pygame.transform.rotate(self.hand_item.sprite, rotation)
        center = [self.hitbox.x + self.hitbox.w / 2, self.hitbox.y + self.hitbox.h / 2]
        screen.blit(sprite, (center[0] - (sprite.get_width() / 2) + 8 + offset[0], center[1] - (sprite.get_height() / 2) + 8 + offset[1]))

    def switch_slot(self, i):
        self.sel_slot = i
        self.hand_item = self.inventory.getSlot(self.sel_slot)
        if isinstance(self.hand_item, item.Pistol):
            self.hand_item.tick = 0
            self.hand_item.shootable = True

    #Update the datas
    def update(self):
        if self.alive:
            if self.health < 0:
                self.alive = False
            if self.health > self.max_health:
                self.health = self.max_health
            
            if self.dashable == False:
                self.dash_tick += 1
            if self.dash_tick >= 54:
                self.dashable = True
                self.dash_tick = 0

            if self.walljumpable == False:
                self.walljump_tick += 1
            if self.walljump_tick >= 12:
                self.walljumpable = True
                self.walljump_tick = 0
                
            if isinstance(self.hand_item, item.Gun):
                if self.hand_item.shootable == False:
                    self.hand_item.tick += 1
                    if self.hand_item.tick >= self.hand_item.interval:
                        self.hand_item.shootable = True
                        self.hand_item.tick = 0
