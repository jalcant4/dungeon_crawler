import pygame as py
from constants import *                     # get constants and definitions
from pygame import mixer
from character import *                     # character and info
from weapon import *
from items import Item
from world import World
from button import Button
import csv
import sys

mixer.init()
py.init()
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("Dungeon Crawler")
# clock defines frame rate
clock = py.time.Clock()

# define game variables
level = 1
start_game = False
pause_game = False
level_complete = False
start_intro = False
screen_scroll = [0, 0]

# load music
py.mixer.music.load(f'{FILEPATH}/assets/audio/music.wav')
py.mixer.music.set_volume(0.3)
py.mixer.music.play(-1, 0.0, 5000)
# fx
shot_fx = py.mixer.Sound(f'{FILEPATH}/assets/audio/arrow_shot.mp3')
hit_fx = py.mixer.Sound(f'{FILEPATH}/assets/audio/arrow_hit.wav')    
# create world
world_data = []
for row in range(WORLD_ROWS):
    r = [-1] * WORLD_COLS
    world_data.append(r)
with open(f'{FILEPATH}/levels/level{level}_data.csv', newline= '') as csvfile:
    reader= csv.reader(csvfile, delimiter = ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World(screen)
world.process_data(world_data)

# create player and info
player = world.player
info = Info(player, level)
# create weapons
bow = Weapon(screen, 'bow')

# create enemies
enemies = world.enemies

# create sprite groups
damage_text_group = py.sprite.Group()
arrow_group = py.sprite.Group()
enemy_proj_group = py.sprite.Group()
item_group = py.sprite.Group()

score_coin = Item(screen, 'coin', SCREEN_WIDTH - 115, 23, True)
item_group.add(score_coin)
for item in world.item_group:
    item_group.add(item)    
    
# create screen fade
intro_fade = ScreenFade(screen, 1, BLACK, 4)
death_fade = ScreenFade(screen, 2, PINK, 4)    

# create buttons
start_button = Button(screen, 'button_start', SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 2 - 150)
exit_button = Button(screen, 'button_exit', SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50)
restart_button = Button(screen, 'button_restart', SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 50)
resume_button = Button(screen, 'button_resume', SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 150)

def reset_level():
    # reset item groups
    damage_text_group.empty()
    arrow_group.empty()
    enemy_proj_group.empty()
    item_group.empty()
    # reset lists
    enemies.clear()
    # crete empty tile list
    world_data = []
    for row in range(WORLD_ROWS):
        r = [-1] * WORLD_COLS
        world_data.append(r)
    
    return world_data
    

# main game loop
run = True
while run:
    # control frame rate
    clock.tick(FPS)
     # event handler
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False 
            
        if event.type == py.KEYDOWN:
            if event.key == py.K_UP:
                player.movement['dy'] = -PLAYER_SPEED
            if event.key == py.K_DOWN:
                player.movement['dy'] = PLAYER_SPEED
            if event.key == py.K_LEFT:
                player.movement['dx'] = -PLAYER_SPEED
            if event.key == py.K_RIGHT:
                player.movement['dx'] = PLAYER_SPEED
                
        if event.type == py.KEYUP:
            if event.key == py.K_UP:
                player.movement['dy'] = 0
            if event.key == py.K_DOWN:
                player.movement['dy'] = 0
            if event.key == py.K_LEFT:
                player.movement['dx'] = 0
            if event.key == py.K_RIGHT:
                player.movement['dx'] = 0

    
    # if start game == false
    if start_game == False:
        screen.fill(MENU_BG)
        if start_button.draw():
            start_game = True
            start_intro = True
        if exit_button.draw():
            run = False
    else:
            # the screen
            screen.fill(BG)
            
            if player.alive:    
                # capture movement
                screen_scroll, level_complete = player.move(world.obstacle_tiles, world.exit_tile)
                
                # update
                world.update(screen_scroll)
                for enemy in enemies:
                    enemy_proj = enemy.ai(player, world.obstacle_tiles, screen_scroll)
                    if enemy_proj:
                        enemy_proj_group.add(enemy_proj)
                    if enemy.alive:
                        enemy.update()
                player.update()
                arrow = bow.update(player)
                if arrow:
                    arrow_group.add(arrow)
                    shot_fx.play()
                for arrow in arrow_group:
                    damage, damage_pos = arrow.update(enemies, world.obstacle_tiles, screen_scroll)
                    if damage:
                        damage_text = DamageText(damage_pos.centerx, damage_pos.y, f'{damage}', RED, screen)
                        damage_text_group.add(damage_text)
                        hit_fx.play()
                damage_text_group.update(screen_scroll)
                enemy_proj_group.update(player, world.obstacle_tiles, screen_scroll)
                item_group.update(player, screen_scroll)
                        
            # draw
            world.draw()
            for enemy in enemies:
                enemy.draw()
            for item in item_group:
                item.draw()
            player.draw()
            bow.draw()
            for arrow in arrow_group:
                arrow.draw()
            for enemy_proj in enemy_proj_group:
                enemy_proj.draw()
            for damage_text in damage_text_group:
                damage_text.draw()
            info.draw_info()
            score_coin.draw()
            
            # show intro
            if start_intro:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0
                    
            # check for new instance
            if level_complete:
                start_intro = True
                level += 1
                world_data = reset_level()
                
                with open(f'{FILEPATH}/levels/level{level}_data.csv', newline= '') as csvfile:
                    reader= csv.reader(csvfile, delimiter = ",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                # reset world            
                world = World(screen)
                world.process_data(world_data)
                # prev
                prev_health = player.health
                prev_score = player.score
                # char instances
                enemies = world.enemies
                player = world.player
                player.health = prev_health
                player.score = prev_score
                info = Info(player, level)
                score_coin = Item(screen, 'coin', SCREEN_WIDTH - 115, 23, True)
                item_group.add(score_coin)
                for item in world.item_group:
                    item_group.add(item)  
                level_complete = False
                    
            # death screen
            if not player.alive:
                if death_fade.fade()and restart_button.draw():
                    start_intro = True
                    world_data = reset_level()
                    with open(f'{FILEPATH}/levels/level{level}_data.csv', newline= '') as csvfile:
                        reader= csv.reader(csvfile, delimiter = ",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    # reset world            
                    world = World(screen)
                    world.process_data(world_data)
                    # prev
                    prev_health = player.health
                    prev_score = player.score
                    # char instances
                    enemies = world.enemies
                    player = world.player
                    player.alive = True
                    info = Info(player, level)
                    score_coin = Item(screen, 'coin', SCREEN_WIDTH - 115, 23, True)
                    item_group.add(score_coin)
                    for item in world.item_group:
                        item_group.add(item)  
                    level_complete = False
                    death_fade.fade_counter = 0
        
            py.display.update()
            
py.quit()
sys.exit()    