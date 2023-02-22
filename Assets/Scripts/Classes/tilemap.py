import pygame
from pygame.math import Vector2

from Assets.Scripts.Classes.hitbox import Hitbox

class Tilemap():
    #Init tilemap
    def __init__(self, map_sprite, x, y, size_x, size_y):
        self.map = map_sprite
        
        self.data = {}
        
        self.hitboxs = {}
        self.types = {}
        
        self.size = [size_x, size_y]
        
        self.hitbox = Hitbox(x, y, 0, 0)

    #Add tile type
    def addType(self, name, color, image, typet = 0, col_t = 0):
        self.types[name] = {"color": color, "image": image, "type": typet, "tiles": {}, "col_t": col_t}

    #Add tile to type
    def addTile(self, name, ttype, image, hitbox = [0, 0, 0, 0], mode = 0):
        if hitbox[2] == 0 and mode == 0:
            hitbox[2] = self.size[0]
        if hitbox[3] == 0 and mode == 0:
            hitbox[3] = self.size[1]
        self.types[name]["tiles"][ttype] = [image, hitbox]

    #Update the data                            
    def write(self):
        self.data = {}
        self.hitboxs = {}
        
        image = None
        tiletype = None
        
        scaleMap = pygame.Surface((self.map.get_width() + 2, self.map.get_height() + 2))
        scaleMap.blit(self.map, (1, 1))
        
        for y in range(self.map.get_height()):
            for x in range(self.map.get_width()):
                c = self.map.get_at((x, y))
                self.hitboxs[(x, y)] = Hitbox(0, 0, 0, 0)
                
                for tile in self.types.values():
                    if c != tile["color"]:
                        continue
                    
                    Left = scaleMap.get_at([x, y + 1])
                    Right = scaleMap.get_at([x + 2, y + 1])
                    Up = scaleMap.get_at([x + 1, y])
                    Down = scaleMap.get_at([x + 1, y + 2])

                    LeftUp = scaleMap.get_at([x, y])
                    RightUp = scaleMap.get_at([x + 2, y])
                    LeftDown = scaleMap.get_at([x, y + 2])
                    RightDown = scaleMap.get_at([x + 2, y + 2])

                    checkc = c if tile["type"] == 0 else (0, 0, 0)

                    if Left != checkc and Right != checkc and Up != checkc and Down != checkc:
                        tiletype = "E"
                    elif Left == checkc and LeftUp != checkc and Up == checkc and Down == checkc and Right == checkc and RightDown == checkc:
                        tiletype = "ITL"
                    elif Right == checkc and RightUp != checkc and Up == checkc and Down == checkc and Left == checkc and LeftDown == checkc:
                        tiletype = "ITR"
                    elif Left == checkc and LeftDown != checkc and Down == checkc and Up == checkc and Right == checkc and RightUp == checkc:
                        tiletype = "IDL"
                    elif Right == checkc and RightDown != checkc and Down == checkc and Up == checkc and Left == checkc and LeftUp == checkc:
                        tiletype = "IDR"
                    elif Left == checkc and Right != checkc and Up == checkc and Down != checkc:
                        tiletype = "TL"
                    elif Left != checkc and Right == checkc and Up == checkc and Down != checkc:
                        tiletype = "TR"
                    elif Left == checkc and Right != checkc and Up != checkc and Down == checkc:
                        tiletype = "DL"
                    elif Left != checkc and Right == checkc and Up != checkc and Down == checkc:
                        tiletype = "DR"
                    elif Left == checkc and Right != checkc and Up == checkc and Down == checkc:
                        tiletype = "DLT"
                    elif Left != checkc and Right == checkc and Up == checkc and Down == checkc:
                        tiletype = "TRD"
                    elif Left == checkc and Right == checkc and Up != checkc and Down == checkc:
                        tiletype = "LDR"
                    elif Left == checkc and Right == checkc and Up == checkc and Down != checkc:
                        tiletype = "RTL"
                    elif Left != checkc and Right != checkc and Up == checkc and Down != checkc:
                        tiletype = "T"
                    elif Left != checkc and Right != checkc and Up != checkc and Down == checkc:
                        tiletype = "D"
                    elif Left == checkc and Right != checkc and Up != checkc and Down != checkc:
                        tiletype = "L"
                    elif Left != checkc and Right == checkc and Up != checkc and Down != checkc:
                        tiletype = "R"
                    elif Left != checkc and Right == checkc and Up == checkc and Down == checkc:
                        tiletype = "TD"
                    elif Left == checkc and Right == checkc and Up != checkc and Down != checkc:
                        tiletype = "LR"
                    elif Left == checkc and Right == checkc and Up == checkc and Down == checkc:
                        tiletype = "F"
                    else:
                        tiletype = "E"

                    try:
                        image = tile["tiles"][tiletype][0]
                    except:
                        image = tile["image"]

                    hitbox = tile["tiles"][tiletype][1]

                    if tiletype == "E":
                        image = tile["image"]
                        
                    self.data[(x, y)] = {"pos": [x * self.size[0] + self.hitbox.x, y * self.size[1] + self.hitbox.y], "sprite": image}
                    self.hitboxs[(x, y)] = Hitbox(x * self.size[0] + self.hitbox.x + hitbox[0], y * self.size[1] + self.hitbox.y + hitbox[1], hitbox[2], hitbox[3])
                    
    def draw(self, screen, offset = [0, 0]):
        for dat in self.data.values():
            screen.blit(dat["sprite"], (dat["pos"][0] + offset[0], dat["pos"][1] + offset[1]))
            
    def setPos(self, x, y):
        for dat in self.data.values():
            dat["pos"][0] += x - self.pos.x
            dat["pos"][1] += y - self.pos.y

        for hb in self.hitboxs:
            hitboxs.x += x - self.pos.x
            hitboxs.y += y - self.pos.y
            
        self.pos.x = x
        self.pos.y = y
