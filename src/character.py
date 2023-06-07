import math
import pygame as py
from constants import *

class Character:
    def __init__(self, surface, name, health, x, y):
        self.surface = surface
        self.name = name
        # game mechanics
        self.alive = True
        self.health = health
        
        # rect
        self.rect = py.Rect(0, 0, 40, 40)                       # x, y, width, length
        self.rect.center = (x, y)
        self.on_init()
    
    def on_init(self):
        # score
        self.score = 0
        # set up timer
        self.update_time = py.time.get_ticks()
        # set up the animation dictionary
        self.animation_dict = {}
        for type in ANIMATION_TYPES:
            temp_list = []
            for i in range(ANIMATION_COUNT):
                img= py.image.load(f'/home/jad/dungeon_crawler/assets/images/characters/{self.name}/{type}/{i}.png').convert_alpha()
                img= scale_img(img, SCALE)
                temp_list.append(img)
            self.animation_dict[type] = temp_list   
        # set the first image
        self.flip = False
        self.frame_index = 0
        self.animation_type = ANIMATION_TYPES[0]
        self.image = self.animation_dict.get(self.animation_type)[self.frame_index]
        # set up the movement
        self.movement = {'dx': 0, 'dy': 0}

            
    def move(self):
        dx = self.movement.get('dx')
        dy = self.movement.get('dy')
        
        if dx == 0 and dy == 0:
            self.animation_type = ANIMATION_TYPES[0]
        else:
            self.animation_type = ANIMATION_TYPES[1]
        if dx < 0:
            self.flip = True
        elif dx > 0: 
            self.flip = False
            
        # control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)
        
        self.rect.x += dx
        self.rect.y += dy

    # Must be called after move    
    def update(self):
        animation_cooldown = 70
        # check health
        if self.health <= 0:
            self.health = 0
            self.alive = False
        
        # update image
        self.image = self.animation_dict.get(self.animation_type)[self.frame_index]
        # check if enough time has passed since the last update
        if py.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = py.time.get_ticks()
        
        if self.frame_index >= len(self.animation_dict.get(self.animation_type)):
            self.frame_index = 0

        
    def draw(self):
        flipped_image = py.transform.flip(self.image, self.flip, False)
        if self.name == 'elf':                                                          # adjusts the y coord based on scale and offset
            self.surface.blit(flipped_image, (self.rect.x, self.rect.y - SCALE * OFFSET))
        else: self.surface.blit(flipped_image, self.rect)
        py.draw.rect(self.surface, RED, self.rect, 1)                                   # surface, color, coordinates
        

# Info class prints information on the character        
class Info:
    def __init__(self, character):
        self.character = character
        self.on_init()
        
    def on_init(self):
        self.surface = self.character.surface
        # hearts
        self.heart_empty = scale_img(py.image.load(f'{FILEPATH}/assets/images/items/heart_empty.png').convert_alpha(), ITEM_SCALE)
        self.heart_half = scale_img(py.image.load(f'{FILEPATH}/assets/images/items/heart_half.png').convert_alpha(), ITEM_SCALE)
        self.heart_full = scale_img(py.image.load(f'{FILEPATH}/assets/images/items/heart_full.png').convert_alpha(), ITEM_SCALE)
        
    def draw_info(self):
        py.draw.rect(self.surface, PANEL, (0, 0, SCREEN_WIDTH, 50))
        py.draw.line(self.surface, WHITE, (0, 50), (SCREEN_WIDTH, 50))     # (start_x, start_y), (end_x, end_y)
        # draw lives
        half_heart_drawn = False
        for i in range(MAX_HEALTH):
            if self.character.health >= ((i + 1) * 20):
                self.surface.blit(self.heart_full, (10 + i * 50, 0))
            elif (self.character.health % HEART_HEALTH > 0) and not half_heart_drawn:
                self.surface.blit(self.heart_half, (10 + i * 50, 0))
                half_heart_drawn = True
            else:
                self.surface.blit(self.heart_empty, (10 + i * 50, 0))
        # draw score
        draw_text(self.surface, f"X:{self.character.score}", font, WHITE,SCREEN_WIDTH - 100, 15)