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
        self.speed = 100

class Player(Character):
    def __init__(self, filename, scale, initial_center):
        super().__init__(filename, scale, initial_center)

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

    ## --- EVENT LOOP --- ##
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # Quit the game
            Running = False
        elif event.type == pygame.KEYDOWN:  # Keypresses
            if event.key == pygame.K_ESCAPE: Running = False

    ## --- KEYSTATES --- ##
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:  # Activate on hold
        pass

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