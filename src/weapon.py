import pygame as py
import math
import random
from constants import *

# helper to scale image
def scale_img(image, scale):
    return py.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

class Weapon:
    def __init__(self, surface, name):
        self.surface = surface
        self.name = name
        self.on_init()
        
    def on_init(self):
        self.original_image = scale_img(py.image.load(f'{FILEPATH}/assets/images/weapons/{self.name}.png').convert_alpha(), WEAPON_SCALE)
        self.angle = 0
        self.image = py.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = py.time.get_ticks()
        
    def update(self, player):
        arrow = None
        self.rect.center = player.rect.center                                   # this code attaches the weapon to the player
        
        # this section calculates the angle from center to cursor 
        pos = py.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)                                  # pygame y coordinates increase down the surface
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        
        # shoot a projectile on left mouseclick
        if py.mouse.get_pressed()[0] and self.fired == False and (py.time.get_ticks() - self.last_shot) >= SHOT_COOLDOWN:                                           
            arrow = Projectile(self.surface, 'arrow', self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = py.time.get_ticks()
            
        # reset mouse click
        if py.mouse.get_pressed()[0] == False:
            self.fired = False
            
        return arrow
        
    def draw(self):
        self.image = py.transform.rotate(self.original_image, self.angle)
        self.surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))
        
class Projectile(py.sprite.Sprite):
    def __init__(self, surface, name, x, y, angle):
        py.sprite.Sprite.__init__(self)
        self.surface = surface
        self.name = name
        self.angle = angle
        self.on_init(x, y)
        
    def on_init(self, x, y):
        self.original_image = py.image.load(f'{FILEPATH}/assets/images/weapons/{self.name}.png').convert_alpha()
        self.image = py.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # calculate horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * PROJECTILE_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * PROJECTILE_SPEED)
       
        
    def update(self, enemies):
        # calculate damage
        damage = 0
        damage_pos = None
        
        # reposition based on speed
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # check if arrow is out of bounds
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
            
        for enemy in enemies:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5, 5)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill()
                break
                
        return damage, damage_pos
    
    # sprites don't necessarily need a draw method, but
    #       we modify the projectile state    
    def draw(self):
        self.surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))