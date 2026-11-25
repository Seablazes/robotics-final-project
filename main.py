"""
Program Name:
Programmer/s: Caylie del Rosario, Soph Kawada, Abri Wisco, Sam Zantua

Description:
"""

import sys
import pygame
from pathlib import Path
from pynnacle_nexus import *

# =========================================================================
# CONSTANTS
# =========================================================================
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

MAX_FPS = 60

# Directions for ease of use
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

## --- FILE DIRECTORIES --- ##
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
IMAGES_DIR = BASE_DIR / 'assets' / 'images'

# =========================================================================
# CLASSES
# =========================================================================
class Character(pygame.sprite.Sprite):
    def __init__(self, filename, scale, initial_center : tuple):
        super().__init__()
        # Create and scale image
        # TODO: allow for animation
        self.img = pygame.image.load(IMAGES_DIR / filename).convert_alpha()
        self.img = pygame.transform.scale(self.img,
            (self.img.width * scale, self.img.height * scale)
        )

        # Game stats
        self.max_hp = 5        # maximum health stat
        self.hp = self.max_hp  # health remaining
        self.atk = 1           # damage dealt per attack

        # Position rectangle at initial center location
        self.rect = self.img.get_frect(center=initial_center)

        # Default movement speed of the character
        self.speed = 100 #pixels per second

class Player(Character):
    def __init__(self, filename, img_scale, initial_center):
        super().__init__(filename, img_scale, initial_center)
        # Game stats
        self.speed = 200

        # Dash
        self.dash_ready = True
        self.facing_up_down = 0     #1 is down, -1 is up
        self.facing_left_right = 0  #1 is right, -1 is left

        # Block
        self.block_ready = False

    def move(self):


    def update(self):
        window.blit(self.img, self.rect)

# =========================================================================
# INITIALIZATION
# =========================================================================
## --- PINNACLE NEXUS --- ##
joystick_x = AnalogInput(A4)
joystick_y = AnalogInput(A5)

B_SHIELD = Button(2) # upper left
LED_SHIELD = DigitalOutput(3)
B_MELEE = Button(4) # lower left
LED_MELEE = DigitalOutput(5)
RANGE_BUTTON = Button(7) # upper right
LED_RANGE = DigitalOutput(6)
DASH_BUTTON = Button(8) # lower right
LED_DASH = DigitalOutput(9)

pygame.init()

## --- DISPLAY SURFACE --- ##
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Untitled Game")

clock = pygame.Clock()

Characters = pygame.sprite.Group()

## --- PLAYER CHARACTER --- ##
Player = Player(
    IMAGES_DIR / 'stick figure.png',
    1,
    (640, 360)
)
Characters.add(Player)

Running = True

# =========================================================================
# GAME LOOP
# =========================================================================
while Running:
    dt = clock.tick(MAX_FPS) / 1000 # Get time between frames in ms

    ## --- KEYSTATES --- ##
    keys = pygame.key.get_pressed()
    """"# PLAYER MOVEMENT
    if keys[pygame.K_w]:  # Move up
        Player.rect.top -= Player.speed * dt
    if keys[pygame.K_s]:  # Move down
        Player.rect.bottom += Player.speed * dt
    if keys[pygame.K_a]:  # Move left
        Player.rect.left -= Player.speed * dt
    if keys[pygame.K_d]:  # Move right
        Player.rect.right += Player.speed * dt"""
    # forgot we were using joystick lol

    ## --- EVENT LOOP --- ##
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # Quit the game
            Running = False
        elif event.type == pygame.KEYDOWN:  # Keypresses
            if event.key == pygame.K_1:
                if Player.dash_ready:
                    pass

    ## --- CONSOLE INPUT --- ##

    ## --- UPDATING --- ##


    ## --- DRAWING --- ##
    window.fill((255, 255, 255))

    Characters.update()
    pygame.display.update()

# =========================================================================
# CLEANUP
# =========================================================================
pygame.quit() # closes the window
sys.exit()