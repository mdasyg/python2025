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

def cast_rays():
    start_angle = player_angle - HALF_FOV
    for ray in range(CASTED_RAYS):
        current_angle = start_angle + ray * STEP_ANGLE
        for depth in range(MAX_DEPTH):
            target_x = player_x - math.sin(current_angle) * depth
            target_y = player_y + math.cos(current_angle) * depth

            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            if 0 <= col < MAP_SIZE and 0 <= row < MAP_SIZE:
                if MAP[row * MAP_SIZE + col] == '#':
                    pygame.draw.line(win, (255, 255, 0), (player_x, player_y), (target_x, target_y), 3)
                    #pygame.draw.rect(win, (255, 255, 0), (ray * SCALE + SCREEN_WIDTH/2, (SCREEN_HEIGHT/2) - (200 / (depth * math.cos(current_angle - player_angle))), SCALE, (400 / (depth * math.cos(current_angle - player_angle))))  )
                    pygame.draw.rect(win, (0,255,0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE-2, TILE_SIZE-2), 2)

                    depth *= math.cos(current_angle - player_angle)  # Fish-eye correction
                    wall_height = 21000 / (depth + 0.0001)  # Avoid division by zero
                    if wall_height > SCREEN_HEIGHT:   #to avoid drawing walls taller than the screen
                        wall_height = SCREEN_HEIGHT

                    pygame.draw.rect(win, (255, 255, 255), (SCREEN_HEIGHT + ray * SCALE, (SCREEN_HEIGHT/2) - wall_height / 2, SCALE, wall_height))

                    break

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= 0.1    
    if keys[pygame.K_RIGHT]:
        player_angle += 0.1
    if keys[pygame.K_UP]:
        forward=True
        player_x += -math.sin(player_angle) * speed
        player_y += math.cos(player_angle) * speed
    if keys[pygame.K_DOWN]:
        forward=False
        player_x += +math.sin(player_angle) * speed
        player_y += -math.cos(player_angle) * speed
    if keys[pygame.K_p]:
        speed +=1
    if keys[pygame.K_m]:
        speed -=1

    if speed < 0:
        speed = 1

    column = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)
    square = row * MAP_SIZE + column
    if MAP[square] == '#':
        if forward:
            player_x -= -math.sin(player_angle) * speed
            player_y -= math.cos(player_angle) * speed
        else:
            player_x -= +math.sin(player_angle) * speed
            player_y -= -math.cos(player_angle) * speed

    win.fill((0, 0, 0))

    # Draw the right half of the screen for the 3D view
    #floor
    pygame.draw.rect(win, (140,140,140), (SCREEN_WIDTH/2, SCREEN_HEIGHT, SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    #ceiling
    pygame.draw.rect(win,(200,200,200), (SCREEN_WIDTH/2, 0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)    )

    draw_map()
    # Raycasting logic goes here
    cast_rays()
    pygame.display.flip()
    clock.tick(30)

    