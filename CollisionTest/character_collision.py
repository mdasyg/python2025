import pygame
import random

#A rectangle moving in space and when collides with a random generated circle it reports a message

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collision Detection")

# Rectangle properties
rect_size = (50, 50)
rect_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
rect_speed = 5
player_rect = pygame.Rect(rect_pos[0], rect_pos[1], rect_size[0], rect_size[1])

# Obstacle properties
num_obstacles = 10
obstacles = []
obstacle_radius = 20
for i in range(num_obstacles):
    while True:
        pos = (random.randint(obstacle_radius, SCREEN_WIDTH-obstacle_radius),
               random.randint(obstacle_radius, SCREEN_HEIGHT-obstacle_radius))
        new_obstacle = pygame.Rect(pos[0]-obstacle_radius, pos[1]-obstacle_radius, obstacle_radius*2, obstacle_radius*2)
        if not player_rect.colliderect(new_obstacle):
            obstacles.append(new_obstacle)
            break

# Font for collision text
font = pygame.font.Font(None, 36)

# Main game loop
running = True
collision_text = ""
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= rect_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += rect_speed
    if keys[pygame.K_UP]:
        player_rect.y -= rect_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += rect_speed

    # Collision detection
    for index, obstacle in enumerate(obstacles):
        if player_rect.colliderect(obstacle):
            collision_text = f"Collided with obstacle number: {index+1}"
            break
    else:
        collision_text = ""

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player_rect)
    for obstacle in obstacles:
        pygame.draw.circle(screen, RED, obstacle.center, obstacle_radius)

    # Draw collision text if there's a collision
    if collision_text:
        text = font.render(collision_text, True, RED)
        screen.blit(text, (50, 50))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Clean up
pygame.quit()
