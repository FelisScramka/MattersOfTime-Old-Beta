import pygame, random
import Assets.Scripts.Classes.entity as entity

BlankTexture = pygame.Surface((16, 16))
BlankTexture.fill((200, 0, 0))

BlankTexture2 = pygame.Surface((16, 16))
BlankTexture2.fill((145, 0, 0))

BlankTexture3 = pygame.Surface((16, 16))
BlankTexture3.fill((90, 0, 0))

BlankBulletTexture = pygame.Surface((4, 4))
BlankBulletTexture.fill((200, 0, 0))

class Item():
    def __init__(self, name, sprite, icon):
        self.name = name
        self.sprite = sprite
        self.icon = icon

        self.angle  = 0

RedTexture = pygame.Surface((16, 16))
RedTexture.fill((255, 0, 0))

Air = Item("Air", RedTexture, RedTexture)

class Stick(Item):
    def __init__(self):
        super(Stick, self).__init__("Stick", BlankTexture, BlankTexture)

class Gun(Item):
    def __init__(self, name, sprite, icon, interval, shake_rate, speed = 1):
        super(Gun, self).__init__(name, sprite, icon)

        self.interval = interval
        self.tick = 0
        self.shootable = True

        self.shake_rate = shake_rate
        self.speed = speed
        
        self.projs = []
        
    def shoot(self, x, y, vel_x = 0, vel_y = 0, grav_y = 0.02):
        if self.shootable:
            proj = entity.Projectile(BlankBulletTexture, x, y, 60, 0, grav_y)
            proj.set_vel(vel_x + random.uniform(-self.shake_rate, self.shake_rate), vel_y + random.uniform(-self.shake_rate, self.shake_rate))
            self.projs.append(proj)
            self.shootable = False

class Bow(Gun):
    def __init__(self):
        super(Bow, self).__init__("Bow", BlankTexture, BlankTexture, 0, 0, 1)

        self.charge = 0
        self.max_charge = 20

    def shoot(self, x, y, vel_x = 0, vel_y = 0):
        super(Bow, self).shoot(x, y, vel_x * self.charge / self.max_charge, vel_y * self.charge / self.max_charge, 0.266)


class FireArmGun(Gun):
    def __init__(self, name, sprite, icon, interval, shake_rate, speed):
        super(FireArmGun, self).__init__(name, sprite, icon, interval, shake_rate, speed)

class Pistol(FireArmGun):
    def __init__(self):
        super(Pistol, self).__init__("Pistol", BlankTexture, BlankTexture, 5, 1.2, 0.96)

class SMG(Gun):
    def __init__(self):
        super(SMG, self).__init__("SubMachineGun", BlankTexture2, BlankTexture2, 4, 0.6, 1.3)

class Revolver(FireArmGun):
    def __init__(self):
        super(Revolver, self).__init__("Revolver", BlankTexture3, BlankTexture3, 28, 0.3, 1.46)
