import pygame as py
from constants import *                     # get constants and definitions
from character import *                     # character and info
from weapon import Weapon
from items import Item
import sys

py.init()
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("Dungeon Crawler")
# clock defines frame rate
clock = py.time.Clock()

    
# create player and info
player = Character(screen, 'elf', 59, 100, 100)
info = Info(player)

# create weapons
bow = Weapon(screen, 'bow')

# create sprite groups
damage_text_group = py.sprite.Group()
arrow_group = py.sprite.Group()
item_group = py.sprite.Group()

potion = Item(screen, 'potion_red', 200, 200)
item_group.add(potion)
coin = Item(screen, 'coin', 400, 400)
item_group.add(coin)

enemies = []
enemy = Character(screen, 'skeleton', 100, 400, 200)
enemies.append(enemy)

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
    player.move()
    
    # update player
    for enemy in enemies:
        enemy.update()
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemies)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, f'{damage}', RED, screen)
            damage_text_group.add(damage_text)
    for damage_text in damage_text_group:
        damage_text.update()
    for item in item_group:
        item.update(player)
            
    # draw
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
    
    
    py.display.update()
            
py.quit()
sys.exit()    