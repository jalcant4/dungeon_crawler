import pygame as py

# img scales
SCALE = 3
WEAPON_SCALE = 1.5
ENEMY_PROJ_SCALE = 1
ITEM_SCALE = 3
BUTTON_SCALE = 1

# game 
FILEPATH = '/home/jad/dungeon_crawler'
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG = (40, 25, 25)
TILE_SIZE = 16 * SCALE
TILE_TYPES = 18
WORLD_ROWS = 150
WORLD_COLS = 150
SCROLL_THRESHOLD = 200

# color
RED = 'Red'
WHITE = 'White'
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
PANEL = (50, 50, 50)
MENU_BG = (130, 0, 0)

# animations
MOB_TYPES = ['elf', 'big_demon', 'goblin', 'imp', 'muddy', 'skeleton', 'tiny_zombie']
ANIMATION_TYPES = ['idle', 'run']
ANIMATION_COUNT = 4

# character constants
PLAYER_SPEED = 5
HIT_COOLDOWN = 400
ENEMY_SPEED = 3
ENEMY_RANGE = 50
ATTACK_RANGE = 60
OFFSET = 12
MAX_HEALTH = 5
HEART_HEALTH = 20

# weapon constants
SHOT_COOLDOWN = 300
PROJECTILE_SPEED = 7.5
ENEMY_PROJ_SPEED = 4


# helper methods
def scale_img(image, scale):
    return py.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

def draw_text(surface, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))

def draw_grid(surface):
    for x in range(30):
        py.draw.line(surface, WHITE, (x * TILE_SIZE, 0), (x * TILE_SIZE, SCREEN_HEIGHT))
        py.draw.line(surface, WHITE, (0, x * TILE_SIZE), (SCREEN_WIDTH, x * TILE_SIZE))


# helper classes
class ScreenFade():
    def __init__(self, surface, direction, color, speed):
        self.surface = surface
        self.direction = direction
        self.color = color
        self.speed = speed
        self.on_init()
        
    def on_init(self):
        self.fade_counter = 0
        
    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        # whole screen fade
        if self.direction == 1:
            py.draw.rect(self.surface, self.color, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            py.draw.rect(self.surface, self.color, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            py.draw.rect(self.surface, self.color, (0, 0- self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            py.draw.rect(self.surface, self.color, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        # vertical screen fade down
        if self.direction == 2:
            py.draw.rect(self.surface, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
        return fade_complete

py.font.init()
font = py.font.Font(f'{FILEPATH}/assets/fonts/AtariClassic.ttf', 20)
class DamageText(py.sprite.Sprite):
    def __init__(self, x, y, damage, color, surface):
        py.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect() 
        self.rect.center = (x, y)
        self.surface = surface
        self.on_init()
     
    def on_init(self):
        self.counter = 0 
       
    def update(self, screen_scroll):
        # reposition the text based on scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        # move damage text up
        self.rect.y -= 1
        # delete the counter after a few ms
        self.counter += 1
        if self.counter > 45:
            self.kill()
        
    def draw(self):
        self.surface.blit(self.image, self.rect)
        