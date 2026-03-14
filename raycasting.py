import pygame
import sys
import math

SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2

pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raycasting")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    win.fill((0, 0, 0))

    # Raycasting logic goes here

    pygame.display.flip()
    clock.tick(30)

    