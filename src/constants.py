import pygame as py

# game
FILEPATH = '/home/jad/dungeon_crawler'
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG = (40, 25, 25)

# game mechanics
RED = 'Red'
WHITE = 'White'
PANEL = (50, 50, 50)

# img scales
SCALE = 3
WEAPON_SCALE = 1.5
ITEM_SCALE = 3

# animations
MOB_TYPES = ['elf', 'big_demon', 'goblin', 'imp', 'muddy', 'skeleton', 'tiny_zombie']
ANIMATION_TYPES = ['idle', 'run']
ANIMATION_COUNT = 4

# character constants
PLAYER_SPEED = 5
OFFSET = 12
MAX_HEALTH = 5
HEART_HEALTH = 20

# weapon constants
SHOT_COOLDOWN = 300
PROJECTILE_SPEED = 7.5


# helper methods
def scale_img(image, scale):
    return py.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

def draw_text(surface, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))

# helper classes
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
       
    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete the counter after a few ms
        self.counter += 1
        if self.counter > 45:
            self.kill()
        
    def draw(self):
        self.surface.blit(self.image, self.rect)
        