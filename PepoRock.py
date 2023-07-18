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
PLAYER_IMAGES = ['player.png', 'rainbow_peepo.png', 'player.png']

def select_player_icon(screen):
    icons = [pygame.image.load(f'resources/images/{image}') for image in PLAYER_IMAGES]
    selected_icon = 0
    font = pygame.font.Font(None, 36)

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
        text = font.render("Choose your champion!", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))
        for i, icon in enumerate(icons):
            x = SCREEN_WIDTH // 2 - len(icons) * icon.get_width() // 2 + i * icon.get_width() + i * 10
            y = SCREEN_HEIGHT // 2 - icon.get_height() // 2
            screen.blit(icon, (x, y))
            if i == selected_icon:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, icon.get_width(), icon.get_height()), 2)
        pygame.display.flip()

        pygame.time.wait(100)

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
        points = [(self.x, self.y), 
                  (self.x + self.width // 2, self.y + self.height), 
                  (self.x + self.width, self.y)]
        pygame.draw.polygon(screen, self.color, points)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

        
def main():
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
    gun_sound = pygame.mixer.Sound('resources/sound/gun.wav')
    hit_sound = pygame.mixer.Sound('resources/sound/hit.wav')
    death_sound = pygame.mixer.Sound('resources/sound/death.wav')
    ###
    
    
    
    high_score = 0
    running = True
    while running:
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
                        player.jump()
                    elif event.key == pygame.K_w:
                        pygame.mixer.Sound.play(gun_sound)
                        projectiles.append(Projectile(player.rect.x + PLAYER_WIDTH // 2, player.rect.y))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move(-1)
            elif keys[pygame.K_RIGHT]:
                player.move(1)

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
            for projectile in projectiles:
                projectile.draw(screen)

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

        # Ask the player if they want to play again
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
