import pygame as py
from constants import *
from character import Character
from items import Item

class World():
    def __init__(self, surface):
        self.surface = surface
        self.map_tiles = []
        self.on_init()
    
    def on_init(self):
        # characters should not be able to cross these tiles
        self.obstacle_tiles = []
        # allows character to move to next level
        self.exit_tile = None
        # create character and enemies
        self.player = None
        self.enemies = []
        # item list
        self.item_group = []
        
        # images
        self.tile_list = []
        for x in range(TILE_TYPES):
            tile_image = py.image.load(f'{FILEPATH}/assets/images/tiles/{x}.png').convert_alpha()
            tile_image = py.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
            self.tile_list.append(tile_image)
            
        
    def process_data(self, data):
        self.level_length = len(data)
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image =  self.tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * TILE_SIZE
                image_y = y * TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]
                
                # collision list
                if tile == 7:
                    self.obstacle_tiles.append(tile_data)
                elif tile == 8:
                    self.exit_tile = tile
                elif tile == 9:
                    coin = Item(self.surface, 'coin', image_x, image_y)
                    self.item_group.append(coin)
                    tile_data[0] = self.tile_list[0]
                elif tile == 10:
                    potion_red = Item(self.surface, 'potion_red', image_x, image_y)
                    self.item_group.append(potion_red)
                    tile_data[0] = self.tile_list[0]
                elif tile == 11:
                    player = Character(self.surface, 'elf', 100, image_x, image_y)
                    self.player = player
                    tile_data[0] = self.tile_list[0]
                elif tile == 12:
                    enemy = Character(self.surface, 'imp', 100, image_x, image_y)
                    self.enemies.append(enemy)
                    tile_data[0] = self.tile_list[0]
                elif tile == 13:
                    enemy = Character(self.surface, 'skeleton', 100, image_x, image_y)
                    self.enemies.append(enemy)
                    tile_data[0] = self.tile_list[0]
                elif tile == 14:
                    enemy = Character(self.surface, 'goblin', 100, image_x, image_y)
                    self.enemies.append(enemy)
                    tile_data[0] = self.tile_list[0]
                elif tile == 15:
                    enemy = Character(self.surface, 'muddy', 100, image_x, image_y)
                    self.enemies.append(enemy)
                    tile_data[0] = self.tile_list[0]
                elif tile == 16:
                    enemy = Character(self.surface, 'tiny_zombie', 100, image_x, image_y)
                    self.enemies.append(enemy)
                    tile_data[0] = self.tile_list[0]
                elif tile == 17:
                    enemy = Character(self.surface, 'big_demon', 100, image_x, image_y, 2)
                    self.enemies.append(enemy)
                    tile_data[0] = self.tile_list[0]
                # add image data to main tiles list
                if tile >= 0:
                    self.map_tiles.append(tile_data)
    
    
    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])
            
                    
    def draw(self):
        for tile in self.map_tiles:
           self.surface.blit(tile[0], tile[1])