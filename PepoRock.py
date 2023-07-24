import random, pygame, sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


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

# Database connection
engine = create_engine('sqlite:///peporock.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Database classes (For highscores score and player name on the end screen)
class PlayerScore(Base):
    __tablename__ = 'PlayerScores'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    score = sqlalchemy.Column(sqlalchemy.Integer)

    def __repr__(self):
        return f'PlayerScore(name={self.name}, score={self.score})'

class HighScore(Base):
    __tablename__ = 'highscores'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    score = sqlalchemy.Column(sqlalchemy.Integer)

    def __repr__(self):
        return f'Highscore(score={self.score})'



# Functions

# returns the highest value score from the database (score is an integer)
def get_high_score():
    high_score = session.query(PlayerScore).order_by(PlayerScore.score.desc()).first()
    if high_score is None:
        return PlayerScore(score=0, name='None')
    else:
        return high_score

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
    jump_sound = pygame.mixer.Sound('resources/sound/jump.wav')
    death_sound = pygame.mixer.Sound('resources/sound/death.wav')
    ###
    
    
    
    # set the high score to the highest score in the peporock.db database
    high_score = get_high_score()
    
    running = True
    while running:
        player = Player(player_image)
        enemies = []
        projectiles = []
        score = 0
                # If the current score is higher than the high score, update the high score
        if score > high_score.score:
            high_score.score = score
            session.add(HighScore(score=high_score.score))
            session.commit()
        
        screen.fill((0, 0, 0))

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
            high_score_text = font.render(f"High Score: {high_score.name} {high_score.score}", True, (255, 255, 255))
            screen.blit(high_score_text, (SCREEN_WIDTH - 250, 20))

            pygame.display.flip()

            clock.tick(60)

        # Save the high score to the database file defined above engine = create_engine('sqlite:///peporock.db', echo=True)
        engine = create_engine('sqlite:///peporock.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        # create the table if it doesn't exist, first
        if not engine.dialect.has_table(engine.connect(), 'high_scores'):
            Base.metadata.create_all(bind=engine)
        # Add the high score to the database
        session.add(HighScore(score=high_score.score))
        session.commit()
        screen.fill((0, 0, 0))
        # Before showing the game over screen, let the user enter their initials (to be saved with in the Player table of the database)
        # Display the input in pygame, not the console

        enter_initials_text = font.render("Enter your initials:", True, (255, 255, 255))
        initials_prompt_x = SCREEN_WIDTH // 2 - enter_initials_text.get_width() // 2  # Save the x-coordinate for later
        initials_prompt_y = SCREEN_HEIGHT // 2 - enter_initials_text.get_height() // 2
        screen.blit(enter_initials_text, (initials_prompt_x, initials_prompt_y))
        pygame.display.flip()

        # Capture the user's initials as keyboard input
        initials = ""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():  # We only want to capture up to 3 alphabetic characters
                        if len(initials) < 3:
                            initials += event.unicode
                            # Redraw the text including the new character
                            screen.fill((0, 0, 0))
                            screen.blit(enter_initials_text, (initials_prompt_x, initials_prompt_y))
                            initials_text = font.render(initials, True, (255, 255, 255))
                            screen.blit(initials_text, (initials_prompt_x, initials_prompt_y + enter_initials_text.get_height()))  # Display the initials just below the prompt
                            pygame.display.flip()
                        elif event.key == pygame.K_BACKSPACE:
                            initials = initials[:-1]
                            # Redraw the text without the last character
                            screen.fill((0, 0, 0))
                            screen.blit(enter_initials_text, (initials_prompt_x, initials_prompt_y))
                            initials_text = font.render(initials, True, (255, 255, 255))
                            screen.blit(initials_text, (initials_prompt_x, initials_prompt_y + enter_initials_text.get_height()))  # Display the initials just below the prompt
                            pygame.display.flip()
                    elif event.key == pygame.K_RETURN:  # The user has finished entering their initials
                        running = False

        # if the user entered initials, add them to the database
        if initials:
            session.add(PlayerScore(name=initials, score=score))
            session.commit()

        # Load the high score(s) from the database) with the existing session 
        high_scores = session.query(HighScore).all()
        # Ask the player if they want to play again
        # Ask the player if they want to play again, while displaying the high score
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            pygame.event.pump()  # Update event queue
            keys = pygame.key.get_pressed()
            if keys[pygame.K_y]:

                break
            elif keys[pygame.K_n]:
                running = False
                break


            # Clear the screen and display the game over text, player score, and high score and ask the player if they want to play again
            screen.fill((0, 0, 0))
            # Draw the score and high score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (20, 20))
            high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
            screen.blit(high_score_text, (SCREEN_WIDTH - 200, 20))
            # Draw the game over text
            game_over_text = font.render("Game Over", True, (255, 255, 255))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            # Ask the player if they want to play again
            play_again_text = font.render("Play Again? (y/n)", True, (255, 255, 255))
            screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 - play_again_text.get_height() // 2 + 50))
            pygame.display.flip()
            
            clock.tick(60)


if __name__ == "__main__":
    main()
