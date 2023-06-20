import pygame as py
import math
import random
from constants import *

class Weapon:
    def __init__(self, surface, name, scale= WEAPON_SCALE):
        self.surface = surface
        self.name = name
        self.scale = scale
        self.on_init()
        
    def on_init(self):
        self.original_image = scale_img(py.image.load(f'{FILEPATH}/assets/images/weapons/{self.name}.png').convert_alpha(), self.scale)
        self.angle = 0
        self.image = py.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = py.time.get_ticks()
        
    def update(self, player):
        # return an arrow on mouse click
        arrow = None
        # this code attaches the weapon to the player
        self.rect.center = player.rect.center
        
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
    def __init__(self, surface, name, x, y, angle, scale= 1):
        py.sprite.Sprite.__init__(self)
        self.surface = surface
        self.name = name
        self.angle = angle
        self.scale = scale
        self.on_init(x, y)
        
    def on_init(self, x, y):
        self.original_image = scale_img(py.image.load(f'{FILEPATH}/assets/images/weapons/{self.name}.png').convert_alpha(), self.scale)
        self.image = py.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # calculate horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * PROJECTILE_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * PROJECTILE_SPEED)
       
        
    def update(self, enemies, obstacle_tiles, screen_scroll):
        # calculate damage
        damage = 0
        damage_pos = None
        # reposition based on speed
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy
        # check if out of bounds
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
        # check for collision with obstacles
        for obstacle in obstacle_tiles:
             if obstacle[1].colliderect(self.rect):
                 self.kill()
        # check for collision between enemy
        for enemy in enemies:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5, 5)
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True
                self.kill()
                break
                
        return damage, damage_pos
    
    # sprites don't necessarily need a draw method, but
    #       we modify the projectile state    
    def draw(self):
        self.surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))
        
class Enemy_Projectile(py.sprite.Sprite):
    def __init__(self, surface, name, x, y, target_x, target_y, scale= ENEMY_PROJ_SCALE, projectile_speed= ENEMY_PROJ_SPEED):
        py.sprite.Sprite.__init__(self)
        self.surface = surface
        self.name = name
        x_dist = target_x - x
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.scale = scale
        self.projectile_speed = projectile_speed
        self.on_init(x, y)
        
    def on_init(self, x, y):
        self.original_image = scale_img(py.image.load(f'{FILEPATH}/assets/images/weapons/{self.name}.png').convert_alpha(), self.scale)
        self.image = py.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # calculate horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * self.projectile_speed
        self.dy = -(math.sin(math.radians(self.angle)) * self.projectile_speed)
       
        
    def update(self, player, obstacle_tiles, screen_scroll):
        # reposition based on speed
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy
        # check if out of bounds
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
        # check for collision with obstacles
        for obstacle in obstacle_tiles:
             if obstacle[1].colliderect(self.rect):
                 self.kill()
        # check for collision for player
        if player.rect.colliderect(self.rect) and not player.hit:
            player.hit = True
            player.last_hit = py.time.get_ticks()
            player.health -= 10
            self.kill() 
    # sprites don't necessarily need a draw method, but
    #       we modify the projectile state    
    def draw(self):
        self.surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))