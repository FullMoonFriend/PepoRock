import random
import pygame

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Player parameters
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = (0, 0, 255)
PLAYER_SPEED = 5

# Enemy parameters
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_COLOR = (255, 0, 0)
ENEMY_SPEED = 5
# Projectile parameters
PROJECTILE_COLOR = (255, 255, 255)
PROJECTILE_SPEED = 10
# Player images
PLAYER_IMAGES = ['peepoRainbow.png', 'peepoBlush.png', 'peepoMaga.png', 'peepoCozy.png', 'peepoFat.png', 'peepoRiot.png', 'peepoFancy.png', 'peepoToilet.png', 'peepoCheer.png', 'peepoFat.png', 'peepoHug.png', 'peepoClown.png', 'peepoPog.png', 'peepoGlad.png', 'peepoWTF.png']
# audio enabled global variable
audio_enabled = True


# Functions
def select_player_icon(screen):
    icons = [pygame.image.load(f'resources/images/{image}') for image in PLAYER_IMAGES]
    selected_icon = 0
    font = pygame.font.Font(None, 36)
    filename_font = pygame.font.Font(None, 24)  # Font for displaying filenames
    
    # Normalize icon sizes to a fixed width and height
    ICON_WIDTH, ICON_HEIGHT = 100, 100  # Adjust this to your preferred dimensions
    icons = [pygame.transform.scale(icon, (ICON_WIDTH, ICON_HEIGHT)) for icon in icons]
    
    # Calculate how many icons can fit in a row and the number of rows required
    icons_per_row = (SCREEN_WIDTH - 10) // (ICON_WIDTH + 10)
    num_rows = (len(icons) - 1) // icons_per_row + 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_icon = (selected_icon - 1) % len(icons)
                elif event.key == pygame.K_RIGHT:
                    selected_icon = (selected_icon + 1) % len(icons)
                elif event.key == pygame.K_RETURN:
                    return PLAYER_IMAGES[selected_icon]

        screen.fill((0, 0, 0))
        text = font.render("Choose your Peepo!", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))
        
        for i, icon in enumerate(icons):
            row = i // icons_per_row
            col = i % icons_per_row
            x = 10 + col * (ICON_WIDTH + 10)
            y = (SCREEN_HEIGHT - num_rows * ICON_HEIGHT) // 2 + row * ICON_HEIGHT + row * 10
            screen.blit(icon, (x, y))
            
            # Display the filename below the icon, stripping the '.png' extension and the 'peepo' from the front of the filename
            filename_text = filename_font.render(PLAYER_IMAGES[i][5:-4], True, (255, 255, 255))
            filename_x = x + (ICON_WIDTH - filename_text.get_width()) // 2
            filename_y = y + ICON_HEIGHT + 5  # 5 pixels below the icon
            screen.blit(filename_text, (filename_x, filename_y))
            
            # Adjusting the rectangle's position and size
            if i == selected_icon:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x-2, y-2, ICON_WIDTH+4, ICON_HEIGHT+4), 2)
        
        pygame.display.flip()




        pygame.time.wait(100)

# Function for muting / unmuting the sound
# def toggle_sound():
#     global audio_enabled # Use the global variable
#     audio_enabled = not audio_enabled
#     if audio_enabled:
#         pygame.mixer.unpause()
#         else:
#         pygame.mixer.pause()


# Classes
class PowerUp:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.x = x
        self.y = y
        self.speed = ENEMY_SPEED  # Use the same speed as enemies for simplicity
        self.duration = 5000  # Duration for which the power-up remains active (in milliseconds)

        # Load and scale the power-up image
        if self.kind == 'multi-shot':
            self.image = pygame.image.load('resources/images/multishot.png')
            self.image = pygame.transform.scale(self.image, (50, 50))  # Adjust size as needed
        # After loading and scaling the image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        if self.kind == 'multi-shot':
            screen.blit(self.image, (self.x, self.y))
    
    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)  # Update the rect position


class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = PROJECTILE_SPEED

    def draw(self, screen):
        pygame.draw.circle(screen, PROJECTILE_COLOR, (self.x, self.y), 5)

    def update(self):
        self.y -= self.speed

class Player:
    def __init__(self, image):
        self.image = pygame.image.load(f'resources/images/{image}')
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT)) 
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
        self.speed = PLAYER_SPEED
        self.is_jumping = False
        self.jump_height = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dx):
        self.rect.x += dx * self.speed
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_height = 10
    

    def update(self):
        if self.is_jumping:
            self.rect.y -= self.jump_height
            self.jump_height -= 1
            if self.jump_height < -10:
                self.is_jumping = False
                self.rect.y = SCREEN_HEIGHT - self.rect.height - 10


class Enemy:
    def __init__(self):
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT 
        self.color = ENEMY_COLOR
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = ENEMY_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        points = [
            (self.x, self.y), 
            (self.x + self.width // 2, self.y + self.height), 
            (self.x + self.width, self.y)
        ]
        pygame.draw.polygon(screen, self.color, points)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

        
def main():
    """
    The main function that runs the game loop for PepoRock.

    Initializes Pygame and loads the game resources, including sounds and music.
    Displays the game screen and handles user input.
    Updates the game state and score based on user input and enemy collisions.
    Displays the score and high score on the screen.
    Asks the player if they want to play again after the game is over.
    """
    pygame.init()
    try:
        pygame.mixer.init()  # Initialize the mixer
    except pygame.error:
        print("Could not initialize mixer, disabling sound")
    # ...

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    player_image = select_player_icon(screen)
    if player_image is None:
        return
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  # Use the default font and a size of 36
    
    #### 
    # Load the sounds and music
    music = pygame.mixer.music.load('resources/sound/music.wav')
    gun_sound = pygame.mixer.Sound('resources/sound/gun.wav')
    hit_sound = pygame.mixer.Sound('resources/sound/hit.wav')
    jump_sound = pygame.mixer.Sound('resources/sound/jump.wav')
    death_sound = pygame.mixer.Sound('resources/sound/death.wav')
    ###
    # initialize the power-ups
    power_ups = []
    active_power_up = None
    power_up_start_time = None
    high_score = 0
    multi_shot_count = 1

    
    
    running = True
    
    while running:
        pygame.mixer.music.play(-1)  # Play the music on loop
        player = Player(player_image)
        enemies = []
        projectiles = []
        score = 0

        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(jump_sound)
                        player.jump()
                    elif event.key == pygame.K_w:
                        pygame.mixer.Sound.play(gun_sound)
                        if active_power_up == 'multi-shot':
                            for i in range(multi_shot_count):
                                offset = (i - (multi_shot_count - 1) / 2) * PLAYER_WIDTH / (multi_shot_count + 1)
                                projectiles.append(Projectile(player.rect.x + PLAYER_WIDTH // 2 + offset, player.rect.y))
                        else:
                            projectiles.append(Projectile(player.rect.x + PLAYER_WIDTH // 2, player.rect.y))


            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move(-1)
            elif keys[pygame.K_RIGHT]:
                player.move(1)

            if random.random() < 0.005:  # Adjust this probability as needed
                power_ups.append(PowerUp('multi-shot', random.randint(0, SCREEN_WIDTH - 50), 0))

            for power_up in power_ups:
                power_up.update()
                if player.rect.colliderect(power_up.rect):
                    if active_power_up == 'multi-shot':
                        multi_shot_count += 1
                    else:
                        active_power_up = 'multi-shot'
                        multi_shot_count = 2
                    power_up_start_time = pygame.time.get_ticks()
                    power_ups.remove(power_up)



            if random.random() < 0.01:
                enemies.append(Enemy())

            for enemy in enemies:
                enemy.update()
                if enemy.rect.y > SCREEN_HEIGHT:
                    enemies.remove(enemy)
                    score += 1
                elif player.rect.colliderect(enemy.rect):
                    pygame.mixer.Sound.play(death_sound)
                    game_over = True
                for projectile in projectiles:
                    if projectile.y < 0:
                        projectiles.remove(projectile)
                    elif enemy.rect.collidepoint((projectile.x, projectile.y)):
                        pygame.mixer.Sound.play(hit_sound)
                        enemies.remove(enemy)
                        projectiles.remove(projectile)
                        score += 1
                        break

            player.update()


            for projectile in projectiles:
                projectile.update()

            screen.fill((0, 0, 0))
            player.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)
            for power_up in power_ups:
                power_up.draw(screen)
            for projectile in projectiles:
                projectile.draw(screen)

            # Check powerup timer
            if active_power_up and pygame.time.get_ticks() - power_up_start_time > power_up.duration:
                active_power_up = None


            # Draw the score and high score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (20, 20))
            high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
            screen.blit(high_score_text, (SCREEN_WIDTH - 200, 20))

            pygame.display.flip()

            clock.tick(60)

        # Update the high score
        if score > high_score:
            high_score = score
        # Reset the multi-shot power-up
        multi_shot_count = 1

        # Ask the player if they want to play again
        while True:
            pygame.event.pump()  # Update event queue
            keys = pygame.key.get_pressed()
            if keys[pygame.K_y]:
                break
            elif keys[pygame.K_n]:
                running = False
                break

            screen.fill((0, 0, 0))
            game_over_text = font.render("Game Over! Play again? (y/n)", True, (255, 255, 255))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()

            clock.tick(60)


if __name__ == "__main__":
    main()
