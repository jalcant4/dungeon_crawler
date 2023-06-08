import pygame as py
from constants import *                     # get constants and definitions
from character import *                     # character and info
from weapon import Weapon
from items import Item
from world import World
import csv
import sys

py.init()
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("Dungeon Crawler")
# clock defines frame rate
clock = py.time.Clock()

# define game variables
level = 1
screen_scroll = [0, 0]
    
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
item_group = py.sprite.Group()

score_coin = Item(screen, 'coin', SCREEN_WIDTH - 115, 23, True)
item_group.add(score_coin)
for item in world.item_group:
    item_group.add(item)

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
    
    # the screen
    screen.fill(BG)
        
    # capture movement
    screen_scroll = player.move(world.obstacle_tiles)
    
    # update
    world.update(screen_scroll)
    for enemy in enemies:
        enemy.ai(screen_scroll)
        enemy.update()
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemies, screen_scroll)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, f'{damage}', RED, screen)
            damage_text_group.add(damage_text)
    for damage_text in damage_text_group:
        damage_text.update(screen_scroll)
    for item in item_group:
        item.update(player, screen_scroll)
            
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
    for damage_text in damage_text_group:
        damage_text.draw()
    info.draw_info()
    score_coin.draw()
    
    py.display.update()
            
py.quit()
sys.exit()    