"""
Program Name:
Programmer/s: Caylie del Rosario, Soph Kawada, Abri Wisco, Sam Zantua

Description:
"""

import sys
import pygame
from pathlib import Path

# =========================================================================
# CONSTANTS
# =========================================================================
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

MAX_FPS = 60

## --- FILE DIRECTORIES --- ##
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
IMAGES_DIR = BASE_DIR / 'assets' / 'images'

# =========================================================================
# CLASSES
# =========================================================================
# players and zombies use the same animation + health + other stuff
class Character(pygame.sprite.Sprite):
    def __init__(self, filename, scale, initial_center : tuple):
        super().__init__()
        # Create and scale image
        # TODO: allow for animation
        self.img = pygame.image.load(IMAGES_DIR / filename).convert_alpha()
        self.img = pygame.transform.scale(self.img,
            (self.img.width * scale, self.img.height * scale)
        )

        # Position rectangle at initial center location
        self.rect = self.img.get_frect(center=initial_center)

        # Default movement speed of the character
        self.speed = 100 #pixels per second

class Player(Character):
    def __init__(self, filename, scale, initial_center):
        super().__init__(filename, scale, initial_center)
        self.speed = 50
        self.dash_ready = True
        self.facing_up = False
        self.facing_down = False
        self.facing_right = True
        self.facing_left = False

    def update(self):
        window.blit(self.img, self.rect)

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
    # PLAYER MOVEMENT
    if keys[pygame.K_w]:  # Move up
        Player.rect.top -= Player.speed * dt
        Player.facing_up = True
        Player.facing_down = False
    if keys[pygame.K_s]:  # Move down
        Player.rect.bottom += Player.speed * dt
        Player.facing_up = False
        Player.facing_down = True
    if keys[pygame.K_a]:  # Move left
        Player.rect.left -= Player.speed * dt
        Player.facing_right = False
        Player.facing_left = True
    if keys[pygame.K_d]:  # Move right
        Player.rect.right += Player.speed * dt
        Player.facing_right = True
        Player.facing_left = False

    ## --- EVENT LOOP --- ##
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # Quit the game
            Running = False
        elif event.type == pygame.KEYDOWN:  # Keypresses
            if event.key == pygame.K_1:
                if Player.dash_ready:
                    if Player.facing_up:
                        Player.rect.top -= Player.speed * dt * 100
                    if Player.facing_down:
                        Player.rect.bottom += Player.speed * dt * 100
                    if Player.facing_left:
                        Player.rect.left -= Player.speed * dt * 100
                    if Player.facing_right:
                        Player.rect.right += Player.speed * dt * 100


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