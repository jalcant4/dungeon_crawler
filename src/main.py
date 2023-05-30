import pygame as pg
from constants import *                     # get constants and definitions
from character import Character
import sys

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Dungeon Crawler")

# clock defines frame rate
clock = pg.time.Clock()

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# create player
player = Character(100, 100)

# main game loop
run = True
while run:
    # control frame rate
    clock.tick(FPS)
    
    # event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                moving_up = True
            if event.key == pg.K_DOWN:
                moving_down = True
            if event.key == pg.K_LEFT:
                moving_left = True
            if event.key == pg.K_RIGHT:
                moving_right = True
                
        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                moving_up = False
            if event.key == pg.K_DOWN:
                moving_down = False
            if event.key == pg.K_LEFT:
                moving_left = False
            if event.key == pg.K_RIGHT:
                moving_right = False
    
    
    screen.fill(BG)
            
    # calculate player movement
    dx = 0
    dy = 0
    if moving_right == True:
        dx = PLAYER_SPEED
    if moving_left == True:
        dx = -PLAYER_SPEED
    if moving_up == True:
        dy = -PLAYER_SPEED
    if moving_down == True:
        dy = PLAYER_SPEED
        
    # move
    player.move(dx, dy)
            
    # draw
    player.draw(screen)
    
    pg.display.update()
            
pg.quit()
sys.exit()
    