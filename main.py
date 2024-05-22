import pygame
import random

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("alien.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        # Remove the bullet if it flies off the screen
        if self.rect.bottom < 0:
            self.kill()

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Space Shooter")

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Loop until the user clicks the close button
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Main loop
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # --- Game logic
    all_sprites.update()

    # Check if the player's bullets hit an enemy
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check if the player collides with an enemy
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        done = True

    # --- Drawing code
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # --- Update the screen
    pygame.display.flip()

    # --- Limit frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
