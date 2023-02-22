import math
"""
class Goal():
    def __init__(self, entity):
        self.entity = entity
        self.resolved = False

class Move(Goal):
    def __init__(self, entity, pos, speed = 1):
        super(Hunt, self).__init__(entity)
        self.target_pos = pos
        self.speed = speed
    def update(self):
        direction = [self.target_pos.x - self.entity.hitbox.x, \
                     self.target_pos.y - self.entity.hitbox.y]
        self.entity.vel[0] += (self.speed if direction >= 0 else -self.speed)
        self.entity.vel[1] += (self.speed if direction >= 0 else -self.speed)
"""
i = 0.1
maxval = 0
while i < 12:
    k = math.sqrt(math.pow(3, 2) + math.pow(i, 2)) + math.sqrt(math.pow(6, 2) + math.pow((12 - i), 2))
    if k > maxval:
        maxval = k
    i += 0.1

print(maxval)
