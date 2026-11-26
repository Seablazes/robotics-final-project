"""
Program Name:
Programmer/s: Caylie del Rosario, Soph Kawada, Abri Wisco, Sam Zantua

Description: TODO: fix
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
UP = -1
DOWN = 1
LEFT = -1
RIGHT = 1

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
while DEFAULT_X == 0 or DEFAULT_Y == 0 or DEFAULT_X >= 600 or DEFAULT_Y >= 600:
    DEFAULT_X, DEFAULT_Y = JOYSTICK_X.read(), JOYSTICK_Y.read()
print(DEFAULT_X, DEFAULT_Y)

OFFSET = 10 # so it works with joysticks that have diff default x/y values

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
        self.is_dashing = False
        self.dash_speed = 600
        self.facing_up_down = 0     #1 is down, -1 is up
        self.facing_left_right = 0  #1 is right, -1 is left
        self.dash_frame_counter = 0
        self.dash_max_frames = 60

        # Block
        self.block_ready = False

    def dash(self):
        if self.dash_ready: # Only dash when cooldown is done
            print(self.facing_left_right, self.facing_up_down)

            self.dash_ready = False # Start dash cooldown
            self.is_dashing = True  # For update function

    def update(self):
        # Dash
        if self.is_dashing:
            # Move in the correct direction
            self.rect.x += self.dash_speed * self.facing_left_right * dt
            self.rect.y += self.dash_speed * self.facing_up_down * dt
            # Update frame count
            self.dash_frame_counter += 1
            # If dashing for a whole lotta frames, stop
            if self.dash_frame_counter >= 60:
                self.is_dashing = False

        # Edge detection
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= WINDOW_HEIGHT: self.rect.bottom = WINDOW_HEIGHT
        if self.rect.left <= 0: self.rect.left = 0
        if self.rect.right >= WINDOW_WIDTH: self.rect.right = WINDOW_WIDTH


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
            if event.key == "":
                    pass

    ## --- CONSOLE INPUT --- ##
    x_move, y_move = JOYSTICK_X.read(), JOYSTICK_Y.read()

    ## --- UPDATING --- ##
    # Player
    if not Player.is_dashing: # dash temporarily disables regular movement
        if x_move < DEFAULT_X + OFFSET: # move right
            Player.rect.x += Player.speed * dt
            Player.facing_left_right = RIGHT
        else: Player.facing_left_right = 0
        if x_move > DEFAULT_X - OFFSET: # move left
            Player.rect.x -= Player.speed * dt
            Player.facing_left_right = LEFT
        else: Player.facing_left_right = 0
        if y_move < DEFAULT_Y + OFFSET: # move up
            Player.rect.y += Player.speed * dt
            Player.facing_up_down = UP
        else: Player.facing_up_down = 0
        if y_move > DEFAULT_Y - OFFSET: # move down
            Player.rect.y -= Player.speed * dt
            Player.facing_up_down = DOWN
        else: Player.facing_left_right = 0

    if B_DASH.is_toggled():
        Player.dash()
    if B_MELEE.is_toggled():
        Player.dash_ready = True

    ## --- DRAWING --- ##
    window.fill((255, 255, 255))

    Characters.update()
    Characters.draw(window)
    pygame.display.update()
    print("Happy birthday Miss Delgado!")

# =========================================================================
# CLEANUP
# =========================================================================
pygame.quit() # closes the window
sys.exit()