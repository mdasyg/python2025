import pygame
import sys
import math

SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2

MAP_SIZE = 8
MAP = (
    '########'
    '#...#..#'
    '#......#'
    '#..#...#'
    '#..#...#'
    '#......#'
    '#...#..#'
    '########'
)

TILE_SIZE = int((SCREEN_WIDTH/2) / MAP_SIZE)
player_x = (SCREEN_WIDTH/4)           
player_y = (SCREEN_HEIGHT/2)
player_angle = 0

FOV = math.pi / 3
CASTED_RAYS = 120
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE) 
STEP_ANGLE = FOV / CASTED_RAYS
HALF_FOV = FOV / 2
speed = 1

SCALE = (SCREEN_WIDTH/2) / CASTED_RAYS

pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raycasting")
clock = pygame.time.Clock()

def draw_map():
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            square = row * MAP_SIZE + col
            therectang = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if MAP[square] == '#':
                pygame.draw.rect(win, (200, 200, 200), therectang)
            else:
                pygame.draw.rect(win, (100, 100, 100), therectang, 1)
    pygame.draw.circle(win, (255, 0, 0), (int(player_x), int(player_y)), 8)

    startXY=(player_x,player_y)
    #κεντρική ακτίνα
    stopXY=(player_x - math.sin(player_angle) * 40, player_y + math.cos(player_angle) * 40)
    pygame.draw.line(win, (255, 0, 0), startXY, stopXY, 3)

    #ακτίνα αριστερά
    stopXY=(player_x - math.sin(player_angle - HALF_FOV) * 40, player_y + math.cos(player_angle - HALF_FOV) * 40)
    pygame.draw.line(win, (255, 0, 0), startXY, stopXY, 3)

    #ακτίνα δεξιά
    stopXY=(player_x - math.sin(player_angle + HALF_FOV) * 40, player_y + math.cos(player_angle + HALF_FOV) * 40)
    pygame.draw.line(win, (255, 0, 0), startXY, stopXY, 3)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    win.fill((0, 0, 0))
    draw_map()
    # Raycasting logic goes here

    pygame.display.flip()
    clock.tick(30)

    