import pygame, sys

# Initialize Pygame
pygame.init()

# Determine max screen size and set up display
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

peepo_left = pygame.image.load('resources/images/peeporight.png').convert_alpha()
peepo_right = pygame.image.load('resources/images/transleftpeepo.png').convert_alpha()
stage = pygame.image.load('resources/images/fightstage.png').convert_alpha()


class Hadooken:
        def __init__(self, x, y, width, height, color):
            self.x = x
            self.y = y 
            self.width = width
            self.height = height
            self.color = color
            self.vel = 1
            # evaluatte correct direction to travel, based on the direction of the opponent
            if self.x > fighter2.x:
                self.direction = "left"
            else:
                self.direction = "right"
            self.is_hit = False
            self.has_hit = False  # Track if the Hadooken has already dealt damage
        
        def hit(self, other):
            hadooken = pygame.Rect(self.x, self.y, self.width, self.height)
            if not self.has_hit and hadooken.colliderect(pygame.Rect(other.x, other.y, other.width, other.height)):
                other.health -= 10
                other.hit = True  # The other fighter is hit
                self.has_hit = True  # Mark the Hadooken as having dealt damage


        def draw(self, win):
            pygame.draw.rect(win, (255, 0, 0) if self.is_hit else self.color, (self.x, self.y, self.width, self.height))

        def move(self):
            if self.direction == "right":
                self.x += self.vel
            else:
                self.x -= self.vel
class Tatsumaki:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.color = color
        self.vel = 1
        self.direction = "right"
        self.is_hit = False

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0) if self.is_hit else self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        if self.direction == "right":
            self.x += self.vel
        else:
            self.x -= self.vel

    def hit(self, other):
        tatsumaki = pygame.Rect(self.x, self.y, self.width, self.height)
        if tatsumaki.colliderect(pygame.Rect(other.x, other.y, other.width, other.height)):
            other.health -= 10
            other.hit = True

class Shoryuken:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.color = color
        self.vel = 1
        self.direction = "right"
        self.is_hit = False

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0) if self.is_hit else self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        if self.direction == "right":
            self.x += self.vel
        else:
            self.x -= self.vel

    def hit(self, other):
        shoryuken = pygame.Rect(self.x, self.y, self.width, self.height)
        if shoryuken.colliderect(pygame.Rect(other.x, other.y, other.width, other.height)):
            other.health -= 10
            other.hit = True
            


class Fighter:
    def __init__(self, x, y, width, height, color, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hit = False # Whether the fighter is hit
        self.original_height = height  # Store the original height
        self.original_y = y  # Store the original y position
        self.color = color
        self.image = image  # Store the image
        self.vel = 1  # Velocity for movement
        self.punch_width = 20  # Width of the punch/kick
        self.health = 1000  # Health of the fighter
        self.punching = False  # Whether the fighter is punching
        self.kicking = False  # Whether the fighter is kicking
        self.hit = False  # Whether the fighter is hit
        self.jump = False  # Whether the fighter is jumping
        self.gravity = 0  # The speed of falling
    
    def draw(self, win):
        # Draw the fighter using the image
        screen.blit(self.image, (self.x, self.y))

        # Punching and kicking can be indicated with additional rectangles or images
        if self.punching:
            pygame.draw.rect(screen, self.color, (self.x + self.width, self.y, self.punch_width, self.height // 2))
        if self.kicking:
            pygame.draw.rect(screen, self.color, (self.x + self.width, self.y + self.height // 2, self.punch_width, self.height // 2))

    def move_left(self):
        self.x -= self.vel

    def move_right(self):
        self.x += self.vel
    def create_hadooken(self, other, active_hadookens):

        # Create a rectangle representing the punch
        hadooken = Hadooken(self.x + self.width, self.y, self.punch_width, self.height // 2, (255, 0, 0))
        # If the punch collides with the other fighter, decrease the other fighter's health
        if hadooken.x > other.x:
            hadooken.direction = "left"
        else:
            hadooken.direction = "right"
        active_hadookens.append(hadooken)
        # turn off punching
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
    bar_width = SCREEN_WIDTH * 0.1  # 10% of screen width
    bar_height = SCREEN_HEIGHT * 0.02  # 2% of screen height
    pygame.draw.rect(win, (255,0,0), (x, y, bar_width, bar_height))
    pygame.draw.rect(win, (0,255,0), (x, y, fighter.health/1000 * bar_width, bar_height))


# Create fighters
# fighter4 = Fighter(100, 500, 50, 100, (0, 0, 255))  # Blue fighter
# fighter3 = Fighter(400, 500, 50, 100, (0, 255, 0))  # Green fighter
# yellow fighter
fighter1 = Fighter(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.83, 50, 100, (0, 0, 255), peepo_left)
fighter2 = Fighter(SCREEN_WIDTH * 0.81, SCREEN_HEIGHT * 0.83, 50, 100, (255, 0, 0), peepo_right)

active_hadookens_player1 = []
active_hadookens_player2 = []
active_tatsumakis = []
active_shoryukens = []


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
            if event.key == pygame.K_e: # fighter 1 hadooken
                fighter1.create_hadooken(fighter2, active_hadookens_player1)
            if event.key == pygame.K_SLASH: # fighter 2 hadooken
                fighter2.create_hadooken(fighter1, active_hadookens_player2) 
            if event.key == pygame.K_UP:  # Fighter2 punch
                fighter2.punch(fighter1)
            if event.key == pygame.K_DOWN:  # Fighter2 kick
                fighter2.kick(fighter1)
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
    screen.blit(stage, (0, 0))
        # Update and draw Hadooken projectiles
    # Update and draw Hadooken projectiles
    updated_hadookens_player1 = []
    for hadooken1 in active_hadookens_player1:
        hadooken1.move()
        hadooken1.draw(screen)
        if not (hadooken1.x > SCREEN_WIDTH or hadooken1.x < 0 or hadooken1.has_hit):
            updated_hadookens_player1.append(hadooken1)
            hadooken1.hit(fighter2)
    active_hadookens_player1 = updated_hadookens_player1

    updated_hadookens_player2 = []
    for hadooken in active_hadookens_player2:
        hadooken.move()
        hadooken.draw(screen)
        if not (hadooken.x > SCREEN_WIDTH or hadooken.x < 0 or hadooken.has_hit):
            updated_hadookens_player2.append(hadooken)
            hadooken.hit(fighter1)
    active_hadookens_player2 = updated_hadookens_player2
    # Draw the fighters
    fighter1.draw(screen)
    fighter2.draw(screen)

    # Draw the health bars
    draw_health_bar(screen, fighter1, SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.05)
    draw_health_bar(screen, fighter2, SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.05)

    fighter1.hit = False
    fighter2.hit = False


    pygame.display.update()
