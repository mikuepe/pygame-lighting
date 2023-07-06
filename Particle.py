import pygame
import random

class Particle:
    def __init__(self, pos, lightmap, maxPos):
        self.x = pos[0]
        self.y = pos[1]
        self.xMax = maxPos[0]
        self.yMax = maxPos[1]

        self.vx = random.randrange(-15,  15) * 4
        self.vy = random.randrange(-17, -12) * 6
        
        self.lightmap = lightmap

    def update(self, delta_time):
        self.vy += 30 * delta_time
        
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

    def draw(self, surface, lightsurface):
        pos = (round(self.x), round(self.y))
        pygame.draw.circle(surface, (255, 255, 255), pos, 1)
        lightsurface.blit(self.lightmap, (pos[0] - 8, pos[1] - 8), special_flags=pygame.BLEND_ADD)
