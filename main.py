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

## --- PINNACLE NEXUS --- ##
JOYSTICK_X = AnalogInput(A4)
JOYSTICK_Y = AnalogInput(A5)

B_SHIELD = Button(2) # upper left
LED_SHIELD = DigitalOutput(3)

B_MELEE = Button(4) # lower left
LED_MELEE = DigitalOutput(5)

B_RANGE = Button(7) # upper right
LED_RANGE = DigitalOutput(6)

B_DASH = Button(8) # lower right
LED_DASH = DigitalOutput(9)

# for calibration purposes
DEFAULT_X, DEFAULT_Y = JOYSTICK_X.read(), JOYSTICK_Y.read()
# shouldn't get messed up by hardware failure/people moving it
while DEFAULT_X == 0 or DEFAULT_Y == 0 or DEFAULT_X > 900 or DEFAULT_Y > 900:
    DEFAULT_X, DEFAULT_Y = JOYSTICK_X.read(), JOYSTICK_Y.read()

OFFSET = 5 # so it works with joysticks that have diff default x/y values

# =========================================================================
# CLASSES
# =========================================================================
class Character(pygame.sprite.Sprite):
    def __init__(self, filename, scale, initial_center : tuple):
        super().__init__()
        # Create and scale image
        # TODO: allow for animation
        self.image = pygame.image.load(IMAGES_DIR / filename).convert_alpha()
        self.image = pygame.transform.scale(self.image,
            (self.image.width * scale, self.image.height * scale)
        )

        # Game stats
        self.max_hp = 5        # maximum health stat
        self.hp = self.max_hp  # health remaining
        self.atk = 1           # damage dealt per attack

        # Position rectangle at initial center location
        self.rect = self.image.get_frect(center=initial_center)

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

    def update(self):
        # Referring to jump code for how this works bear with me

# =========================================================================
# INITIALIZATION
# =========================================================================

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
    x_move, y_move = JOYSTICK_X.read(), JOYSTICK_Y.read()

    ## --- UPDATING --- ##
    # Player
    if x_move < DEFAULT_X + OFFSET: # move right
        Player.rect.x += Player.speed * dt
    if x_move > DEFAULT_X - OFFSET: # move left
        Player.rect.x -= Player.speed * dt
    if y_move < DEFAULT_Y + OFFSET: # move up
        Player.rect.y += Player.speed * dt
    if y_move > DEFAULT_Y - OFFSET: # move down
        Player.rect.y -= Player.speed * dt

    if B_DASH.read() == 0:
        Player.rect.x += 100

    ## --- DRAWING --- ##
    window.fill((255, 255, 255))

    Characters.draw(window)
    pygame.display.update()

# =========================================================================
# CLEANUP
# =========================================================================
pygame.quit() # closes the window
sys.exit()