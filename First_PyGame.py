# import the pygame module
import pygame as py
import random

# Import pygame constants for keystrokes
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# Setup mixer in pygame
py.mixer.init()

# Initialize the pygame module
py.init()

# Game global variables
game_points = 0
coins_list = []

# Player object class by extending the sprite class
class Player(py.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = py.image.load(
            'assets/img/spaceShips_001.png').convert()
        self.surf = py.transform.scale(self.surf, (50, 50))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.speed = 10

    # movement of the player
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # check window screen collition
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# class object for enemy
class Enemy(py.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = py.image.load(
            'assets/img/spaceMeteors_001.png').convert()
        self.surf = py.transform.scale(
            self.surf, (random.randint(20, 50), random.randint(20, 50)))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite base on it's speed.
    # remove when passes the left edge of main screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Create object class for space building for background
class Station(py.sprite.Sprite):
    def __init__(self):
        super(Station, self).__init__()
        self.surf = py.image.load(
            'assets/img/spaceStation_022.png').convert()
        self.surf = py.transform.scale(self.surf, (20, 60))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Class for text object
class Text:
    def __init__(self, text, pos, size):
        self.text = text
        self.pos = pos
        self.fontsize = size

        self.fontname = None
        self.fontcolor = WHITE
        self.set_font()
        self.render()

    def set_font(self):
        # Add font to the text
        self.font = py.font.Font(self.fontname, self.fontsize)

    def render(self):
        # Convert text as an image in order to blit into the screen
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        # Draw the text to the screen
        screen.blit(self.img, self.rect)


class Coins(py.sprite.Sprite):
    def __init__(self):
        super(Coins, self).__init__()
        self.surf = py.image.load(
            'assets/img/spaceBuilding_008.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = 2

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def draw(self):
        screen.blit(self.surf, self.rect)

# Game functions
def game_over():
    screen.fill((0, 0, 0))
    txt_title = Text('Game Over', pos=(SCREEN_HEIGHT / 2,SCREEN_WIDTH / 3),size=(50))
    txt_score = Text('Score: ' + str(game_points), pos=(SCREEN_HEIGHT / 2,(SCREEN_WIDTH / 3) + 70),size=(50))
    txt_quit = Text('Press ESC to quit', pos=(SCREEN_HEIGHT / 2,(SCREEN_WIDTH / 3) + 140),size=(22))
    txt_title.draw()
    txt_score.draw()
    txt_quit.draw()
    py.display.flip()

    running = True
    while running:
        for event in py.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

    clock.tick(30)
    

# Constants for the screen size
# and create a screen object
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = py.Color(255, 255, 255)

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a new objects
ADDENEMY = py.USEREVENT + 1
py.time.set_timer(ADDENEMY, 500)
ADDSTATION = py.USEREVENT + 2
py.time.set_timer(ADDSTATION, 5000)
ADDCOINS = py.USEREVENT + 3
py.time.set_timer(ADDCOINS, random.randint(5000, 8000))

# Instantiate player
player = Player()
clock = py.time.Clock()  # Clock for framerate

# Create Sprite groups of sprites and enemy
# enemies - collision detection and position
# all_sprites - rendering
enemies = py.sprite.Group()
station = py.sprite.Group()
all_sprites = py.sprite.Group()
all_sprites.add(player)

# Load and play background music
py.mixer.music.load('assets/Apoxode_-_Electric_1.wav')
py.mixer.music.play(loops=-1)  # loop over and over

# Sound effects
move = py.mixer.Sound('assets/sound/Jump43.wav')
explode = py.mixer.Sound('assets/sound/Explosion06.wav')
points = py.mixer.Sound('assets/sound/Powerup11.wav')

# GAME LOOP
running = True
while running:
    # look at every previous frame event
    for event in py.event.get():
        # what key did the player used?
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False  # exit the game
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            # create a new enemy and add in sprite group
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDSTATION:
            # Create a new station
            new_station = Station()
            station.add(new_station)
            all_sprites.add(new_station)
        elif event.type == ADDCOINS:
            new_coins = Coins()
            coins_list.append(new_coins)

    screen.fill((0, 0, 0))
    # Get all the keyboard keys -> dictionary
    pressed_keys = py.key.get_pressed()
    # Update the position of player
    player.update(pressed_keys)
    enemies.update()
    station.update()
    # if new coins exist call the update method, if not don't
    try:
        for coins in coins_list:
            coins.update()
            coins.draw()
    except:
        print('No coins')
    text = Text(str(game_points), pos=(20, 20), size=(50))  # text object
    text.draw()

    # Draw all sprite in a sprite group
    for entity in all_sprites:
        screen.blit(py.transform.rotate(entity.surf, 90), entity.rect)

    # check if coins and player sprite collided
    if len(coins_list) != 0:
        for curr_coin in coins_list:
            if py.sprite.collide_rect(player, curr_coin):
                coins_list.remove(curr_coin)
                points.play()
                game_points += 1
                
    # Check if enemy collided to the player
    if py.sprite.spritecollideany(player, enemies):
        # if true, remove the player and game over
        player.kill()
        # Stop other sound and play collision sound
        explode.play()
        py.time.delay(500)
        print('Score: ', str(game_points))
        running = False
        
        # Game is done
        # Stop all music
        py.mixer.music.stop()
        py.mixer.quit()

        game_over()

    py.display.flip()  # Update the screen
    # Ensure the game runs 30 frame per seconds
    clock.tick(30)
