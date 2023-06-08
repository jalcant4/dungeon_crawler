import pygame as py
from constants import *

class Item(py.sprite.Sprite):
    def __init__(self, surface, name, x, y, dummy = False):
        py.sprite.Sprite.__init__(self)
        self.surface = surface
        self.name = name
        self.dummy = dummy
        self.on_init(x, y)
        
    def on_init(self, x, y):
        match self.name:
            case 'coin':
                self.item_type = 0
                self.animation_list = []
                for i in range(ANIMATION_COUNT):
                    img = scale_img(py.image.load(f'{FILEPATH}/assets/images/items/{self.name}_f{i}.png').convert_alpha(), ITEM_SCALE)
                    self.animation_list.append(img)
            case 'potion_red':
                self.item_type = 1
                self.animation_list = [scale_img(py.image.load(f'{FILEPATH}/assets/images/items/{self.name}.png').convert_alpha(), ITEM_SCALE)]
            
        self.frame_index = 0
        self.update_time = py.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
    def update(self, player, screen_scroll):
        # reposition with screen scroll
        if not self.dummy:
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]
        
        # check to see if player collides
        if self.rect.colliderect(player.rect):
            if self.item_type == 0:
                player.score += 1
            elif self.item_type == 1:
                player.health += 10
                if player.health > 100:
                    player.health = 100
            self.kill()
        # handle cooldown
        animation_cooldown = 150
        # update image
        self.image = self.animation_list[self.frame_index]
        # check if enough time has passed since the last update
        if py.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = py.time.get_ticks()
        # check if anamiation has finished
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            
    def draw(self):
        self.surface.blit(self.image, self.rect)