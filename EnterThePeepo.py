import pygame
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Rogue-like Prototype')

# Player properties
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 0.1
# Room properties
room_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
current_color = 0

def generate_obstacles():
    obstacles = []
    num_obstacles = random.randint(2, 5)

    for _ in range(num_obstacles):
        width = random.randint(50, 150)
        height = random.randint(50, 150)
        
        x = random.randint(0, SCREEN_WIDTH - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        
        # Simple check to make sure obstacle doesn't overlap with player's initial position
        while abs(x - SCREEN_WIDTH // 2) < 100 and abs(y - SCREEN_HEIGHT // 2) < 100:
            x = random.randint(0, SCREEN_WIDTH - width)
            y = random.randint(0, SCREEN_HEIGHT - height)

        obstacles.append(pygame.Rect(x, y, width, height))

    return obstacles

obstacles = generate_obstacles()


running = True
while running:
    screen.fill(room_colors[current_color])
    for obstacle in obstacles:
        pygame.draw.rect(screen, (50, 50, 50), obstacle)
    if player_pos[0] <= 0 or player_pos[0] >= SCREEN_WIDTH - 50 or player_pos[1] <= 0 or player_pos[1] >= SCREEN_HEIGHT - 50:
        current_color = (current_color + 1) % len(room_colors)
        player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        obstacles = generate_obstacles()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed
    
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], 50, 50))
    pygame.display.flip()

pygame.quit()
