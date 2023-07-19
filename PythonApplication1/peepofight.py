import pygame
import sys

# Initialize Pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant screen size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Fighter:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 1  # Velocity for movement
        self.punch_width = 20  # Width of the punch
        self.health = 1000  # Health of the fighter
        self.punching = False  # Whether the fighter is punching
        self.hit = False  # Whether the fighter is hit

    def draw(self, win):
        # Draw the fighter
        pygame.draw.rect(win, (255, 0, 0) if self.hit else self.color, (self.x, self.y, self.width, self.height))

        # Draw the punch if the fighter is punching
        if self.punching:
            pygame.draw.rect(win, self.color, (self.x + self.width, self.y, self.punch_width, self.height))

    def move_left(self):
        self.x -= self.vel

    def move_right(self):
        self.x += self.vel

    def punch(self, other):
        # The fighter is punching
        self.punching = True

        # Create a rectangle representing the punch
        punch = pygame.Rect(self.x + self.width, self.y, self.punch_width, self.height)
        # If the punch collides with the other fighter, decrease the other fighter's health
        if punch.colliderect(pygame.Rect(other.x, other.y, other.width, other.height)):
            other.health -= 10
            other.hit = True  # The other fighter is hit


# In the end of the game loop:



def draw_health_bar(win, fighter, x, y):
    if fighter.health < 0:
        fighter.health = 0
    pygame.draw.rect(win, (255,0,0), (x, y, 100, 10))
    pygame.draw.rect(win, (0,255,0), (x, y, fighter.health/10, 10))  # Scale health down for drawing

# Create fighters
fighter1 = Fighter(100, 500, 50, 100, (0, 0, 255))  # Blue fighter
fighter2 = Fighter(650, 500, 50, 100, (255, 0, 0))  # Red fighter

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # Fighter1 punch
                fighter1.punch(fighter2)
            if event.key == pygame.K_UP:  # Fighter2 punch
                fighter2.punch(fighter1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:  # Fighter1 stop punching
                fighter1.punching = False
            if event.key == pygame.K_UP:  # Fighter2 stop punching
                fighter2.punching = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Move fighter1 left
        fighter1.move_left()
    if keys[pygame.K_d]:  # Move fighter1 right
        fighter1.move_right()
    if keys[pygame.K_LEFT]:  # Move fighter2 left
        fighter2.move_left()
    if keys[pygame.K_RIGHT]:  # Move fighter2 right
        fighter2.move_right()

    # Check for game over
    if fighter1.health <= 0 or fighter2.health <= 0:
        print("Game Over")
        pygame.quit()
        sys.exit()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the fighters
    fighter1.draw(screen)
    fighter2.draw(screen)

    # Draw the health bars
    draw_health_bar(screen, fighter1, 50, 50)
    draw_health_bar(screen, fighter2, 650, 50)

    # Reset the hit status of the fighters
    fighter1.hit = False
    fighter2.hit = False

    pygame.display.update()