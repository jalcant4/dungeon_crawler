import math
import pygame as py
from constants import *
from weapon import *

class Character:
    def __init__(self, surface, name, health, x, y, size= 1, boss= False):
        self.surface = surface
        self.name = name
        # game mechanics
        self.alive = True
        self.health = health
        # rect
        self.rect = py.Rect(0, 0, TILE_SIZE * size, TILE_SIZE * size)                       # x, y, width, length
        self.rect.center = (x, y)
        # is boss?
        self.boss= boss
        self.on_init()
    
    def on_init(self):
        # score
        self.score = 0
        # set up timer
        self.update_time = py.time.get_ticks()
        self.hit = False
        self.last_hit_time= py.time.get_ticks()
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
        # set up game mechanics
        self.stunned = False
        self.last_attack = py.time.get_ticks()

            
    def move(self, obstacle_tiles, exit_tile= None):
        # game mechanics
        screen_scroll = [0, 0]
        level_complete = False
        
        # change in movement
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
        
        # check if collision with map in x direction
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect) and dx > 0:
                self.rect.right = obstacle[1].left
            elif obstacle[1].colliderect(self.rect) and dx < 0:
                self.rect.left = obstacle[1].right
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect) and dy > 0:
                self.rect.bottom = obstacle[1].top
            elif obstacle[1].colliderect(self.rect) and dy < 0:
                self.rect.top = obstacle[1].bottom

        # logic only apllies to player
        if self.name == 'elf':
            # ensure player is close to the center of exit
            if exit_tile[1].colliderect(self.rect):
                exit_dist= math.sqrt(((self.rect.centerx - exit_tile[1].centerx) ** 2) + ((self.rect.centery - exit_tile[1].centery) ** 2))
                if exit_dist < 20:
                    level_complete = True
            # update scroll based on player position
            # move camera left and right
            if self.rect.right > (SCREEN_WIDTH - SCROLL_THRESHOLD):
                screen_scroll[0] = (SCREEN_WIDTH - SCROLL_THRESHOLD) - self.rect.right
                self.rect.right = SCREEN_WIDTH - SCROLL_THRESHOLD
            if self.rect.left < SCROLL_THRESHOLD:
                screen_scroll[0] = SCROLL_THRESHOLD - self.rect.left
                self.rect.left = SCROLL_THRESHOLD
            # move camera up and down
            if self.rect.bottom > (SCREEN_HEIGHT - SCROLL_THRESHOLD):
                screen_scroll[1] = (SCREEN_HEIGHT - SCROLL_THRESHOLD) - self.rect.bottom
                self.rect.bottom = SCREEN_HEIGHT - SCROLL_THRESHOLD
            if self.rect.top < SCROLL_THRESHOLD:
                screen_scroll[1] = SCROLL_THRESHOLD - self.rect.top
                self.rect.top = SCROLL_THRESHOLD
                
        return screen_scroll, level_complete
    
    def ai(self, player, obstacle_tiles, screen_scroll):
        enemy_proj = None
        stun_cooldown = 150
        clipped_line= ()
        # reset movement
        self.movement['dx'] = 0
        self.movement['dy'] = 0
        # reposition the enemy based on scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        # line of sight from enemy to player
        line_of_sight= ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))
        # check if line of sight passes through an obstacle
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line= obstacle[1].clipline(line_of_sight)
        # check distance to player
        dist = math.sqrt(((self.rect.centerx - player.rect.centerx) ** 2) + ((self.rect.centery - player.rect.centery) ** 2))
        if not clipped_line and dist > ENEMY_RANGE:
        # homing type ai
            if self.rect.centerx > player.rect.centerx:
                self.movement['dx'] -= ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx:
                self.movement['dx'] = ENEMY_SPEED
            if self.rect.centery > player.rect.centery:
                self.movement['dy'] -= ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                self.movement['dy'] = ENEMY_SPEED
        # enemy is stunned
        if self.alive and not self.stunned:
            # move     
            self.move(obstacle_tiles)
            # attack player
            if dist < ATTACK_RANGE and not player.hit:
                player.hit = True
                player.last_hit_time = py.time.get_ticks()
                player.health -= 10
            # boss shoot fierballes
            enemy_proj_cooldown = 650
            if self.boss and dist < 500:
                if py.time.get_ticks() - self.last_attack >= enemy_proj_cooldown:
                    enemy_proj = Enemy_Projectile(self.surface, 'fireball', self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                    self.last_attack = py.time.get_ticks()
        # check if hit
        if self.alive and self.hit:
            self.hit = False
            self.last_hit_time = py.time.get_ticks()
            self.stunned = True
            self.movement['dx'] = 0
            self.movement['dy'] = 0
        # reset cooldown
        if self.alive and (py.time.get_ticks() - self.last_hit_time) > stun_cooldown:
            self.stunned = False
        
        return enemy_proj    
                    
    # Must be called after move    
    def update(self):
        animation_cooldown = 70
        # check health
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.animation_type = ANIMATION_TYPES[0]
        # check last hit time
        if (py.time.get_ticks()- self.last_hit_time) >= HIT_COOLDOWN:
            self.hit = False
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
    def __init__(self, character, level):
        self.character = character
        self.level = level
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
        # draw level
        draw_text(self.surface, f"LEVEL: {self.level}", font, WHITE, SCREEN_WIDTH / 2, 15)                
        # draw score
        draw_text(self.surface, f"X:{self.character.score}", font, WHITE, SCREEN_WIDTH - 100, 15)