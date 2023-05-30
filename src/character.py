import math
import pygame as pg
from constants import *

class Character:
    def __init__(self, x, y):
        self.rect = pg.Rect(0, 0, 40, 40)                       # x, y, width, length
        self.rect.center = (x, y)
        
    def move(self, dx, dy):
        # control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)
        
        self.rect.x += dx
        self.rect.y += dy
        
    def draw(self, surface):
        pg.draw.rect(surface, RED, self.rect)                  # screen, color, coordinates