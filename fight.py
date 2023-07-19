import pygame, sys

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
        self.original_height = height  # Store the original height
        self.original_y = y  # Store the original y position
        self.color = color
        self.vel = 1  # Velocity for movement
        self.punch_width = 20  # Width of the punch/kick
        self.health = 1000  # Health of the fighter
        self.punching = False  # Whether the fighter is punching
        self.kicking = False  # Whether the fighter is kicking
        self.hit = False  # Whether the fighter is hit
        self.jump = False  # Whether the fighter is jumping
        self.gravity = 0  # The speed of falling

    def draw(self, win):
        # Draw the fighter
        pygame.draw.rect(win, (255, 0, 0) if self.hit else self.color, (self.x, self.y, self.width, self.height))

        # Draw the punch if the fighter is punching
        if self.punching:
            pygame.draw.rect(win, self.color, (self.x + self.width, self.y, self.punch_width, self.height // 2))

        # Draw the kick if the fighter is kicking
        if self.kicking:
            pygame.draw.rect(win, self.color, (self.x + self.width, self.y + self.height // 2, self.punch_width, self.height // 2))

    def move_left(self):
        self.x -= self.vel

    def move_right(self):
        self.x += self.vel

    def crouchToggle(self):
        if self.height == self.original_height:
            self.height = self.height // 2 
            self.y = self.original_y + self.height  # Adjust y position when crouching
        else:
            self.y = self.original_y  # Reset y position when standing up
            self.height = self.original_height
    # Jumping method
    def jump_up(self):
        if not self.jump:  # If the fighter is not already jumping
            self.jump = True
            self.gravity = -10

    def move(self, direction):
        if direction == "left":
            self.x -= self.vel
        elif direction == "right":
            self.x += self.vel
        if self.jump:  # If the fighter is jumping
            self.y += self.gravity  # Move up or down
            self.gravity += 0.5  # Increase gravity (less negative or more positive)
            if self.gravity > 10:  # Maximum falling speed
                self.gravity = 10
            if self.y > 500:  # If the fighter is on the ground
                self.y = 500
                self.jump = False  # Stop jumping
                self.gravity = 0  # Reset gravity
    def jump_gravity(self):
        if self.jump:  # If the fighter is jumping
            self.y += self.gravity  # Move up or down
            self.gravity += 0.5  # Increase gravity (less negative or more positive)
            if self.gravity > 10:  # Maximum falling speed
                self.gravity = 10
            if self.y > 500:  # If the fighter is on the ground
                self.y = 500
                self.jump = False  # Stop jumping
                self.gravity = 0  # Reset gravity
    def punch(self, other):
        # The fighter is punching
        self.punching = True

        # Create a rectangle representing the punch
        punch = pygame.Rect(self.x + self.width, self.y, self.punch_width, self.height // 2)
        # If the punch collides with the other fighter, decrease the other fighter's health
        if punch.colliderect(pygame.Rect(other.x, other.y, other.width, other.height)):
            other.health -= 10
            other.hit = True  # The other fighter is hit

    def kick(self, other):
        # The fighter is kicking
        self.kicking = True

        # Create a rectangle representing the kick
        kick = pygame.Rect(self.x + self.width, self.y + self.height // 2, self.punch_width, self.height // 2)
        # If the kick collides with the other fighter, decrease the other fighter's health
        if kick.colliderect(pygame.Rect(other.x, other.y, other.width, other.height)):
            other.health -= 10
            other.hit = True  # The other fighter is hit

def draw_health_bar(win, fighter, x, y):
    if fighter.health < 0:
        fighter.health = 0
    pygame.draw.rect(win, (255,0,0), (x, y, 100, 10))
    pygame.draw.rect(win, (0,255,0), (x, y, fighter.health/10, 10))  # Scale health down for drawing

# Create fighters
fighter1 = Fighter(100, 500, 50, 100, (0, 0, 255))  # Blue fighter
fighter2 = Fighter(650, 500, 50, 100, (255, 0, 0))  # Red fighter

while True:
    fighter1.jump_gravity()
    fighter2.jump_gravity()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # Fighter1 punch
                fighter1.punch(fighter2)
            if event.key == pygame.K_s:  # Fighter1 kick
                fighter1.kick(fighter2)
            if event.key == pygame.K_UP:  # Fighter2 punch
                fighter2.punch(fighter1)
            if event.key == pygame.K_DOWN:  # Fighter2 kick
                fighter2.kick(fighter1)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:  # Fighter1 stop punching
                fighter1.punching = False
            if event.key == pygame.K_s:  # Fighter1 stop kicking
                fighter1.kicking = False
            if event.key == pygame.K_UP:  # Fighter2 stop punching
                fighter2.punching = False
            if event.key == pygame.K_DOWN:  # Fighter2 stop kicking
                fighter2.kicking = False

    keys = pygame.key.get_pressed()
    # Move fighters
    if keys[pygame.K_a]:  # Move fighter1 left
        fighter1.move("left")
    if keys[pygame.K_d]:  # Move fighter1 right
        fighter1.move("right")
    if keys[pygame.K_LEFT]:  # Move fighter2 left
        fighter2.move("left")
    if keys[pygame.K_RIGHT]:  # Move fighter2 right
        fighter2.move("right")
    # Crouch fighters
    if keys[pygame.K_LCTRL]:  # Crouch fighter1
        fighter1.crouchToggle()
    if keys[pygame.K_RSHIFT]:  # Crouch fighter2
        fighter2.crouchToggle()

    # Jump fighters
    if keys[pygame.K_SPACE]:  # Jump fighter1
        fighter1.jump_up()
    if keys[pygame.K_RCTRL]:  # Jump fighter2
        fighter2.jump_up()

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

    fighter1.hit = False
    fighter2.hit = False


    pygame.display.update()
