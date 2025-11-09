import pygame
import sys

# Initialize Pygame
pygame.init()

BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)   
BLUE=(0, 0, 255)

size=(700, 500)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("My First Pygame Program")

done=False
clock=pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True

    screen.fill(WHITE)

    pygame.draw.line(screen, BLACK, [0, 0], [100, 100], 5)
    pygame.draw.rect(screen, RED, [20, 20, 250, 100], 2)
    pygame.draw.ellipse(screen, GREEN, [300, 200, 200, 100], 0)
    pygame.draw.polygon(screen, BLUE, [[100, 100], [0, 200], [200, 200]], 5)
    pygame.draw.circle(screen, BLACK, [400, 400], 50, 0)

    pygame.display.flip()
    clock.tick(60)

