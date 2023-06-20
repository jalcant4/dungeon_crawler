import pygame as py
from constants import *

class Button():
    def __init__(self, surface, name, x, y):
        self.surface = surface
        self.name = name
        self.on_init(x, y)
        
    def on_init(self, x, y):
        self.image = scale_img(py.image.load(f'{FILEPATH}/assets/images/buttons/{self.name}.png').convert_alpha(), BUTTON_SCALE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self):
        action = False
        # get mouse pos
        pos = py.mouse.get_pos()
        # check mouseover and left clicked
        if self.rect.collidepoint(pos) and py.mouse.get_pressed()[0]:
            action = True
        self.surface.blit(self.image, self.rect)
        return action