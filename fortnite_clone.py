import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
PLAYER_SPEED = 5
BULLET_SPEED = 10
GRAVITY = 0.5
JUMP_STRENGTH = -12
BUILDING_MATERIALS = 100
MAX_HEALTH = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Fortnite Clone")

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.velocity_x = 0
        self.velocity_y = 0
        self.health = MAX_HEALTH
        self.materials = BUILDING_MATERIALS
        self.is_jumping = False
        self.direction = 1  # 1 for right, -1 for left
        self.weapons = ["AR", "Shotgun"]
        self.current_weapon = 0
        self.ammo = {"AR": 30, "Shotgun": 8}
        self.reload_timer = 0
        self.is_reloading = False

    def move(self, keys):
        # Horizontal movement
        if keys[pygame.K_a]:
            self.velocity_x = -PLAYER_SPEED
            self.direction = -1
        elif keys[pygame.K_d]:
            self.velocity_x = PLAYER_SPEED
            self.direction = 1
        else:
            self.velocity_x = 0

        # Jump
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True

        # Apply gravity
        self.velocity_y += GRAVITY

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Keep player in bounds
        self.x = max(0, min(WINDOW_WIDTH - self.width, self.x))
        self.y = max(0, min(WINDOW_HEIGHT - self.height, self.y))

        # Ground collision
        if self.y >= WINDOW_HEIGHT - self.height:
            self.y = WINDOW_HEIGHT - self.height
            self.velocity_y = 0
            self.is_jumping = False

    def shoot(self):
        if not self.is_reloading and self.ammo[self.weapons[self.current_weapon]] > 0:
            self.ammo[self.weapons[self.current_weapon]] -= 1
            return Bullet(self.x + self.width//2, self.y + self.height//2, 
                         self.direction, self.weapons[self.current_weapon])
        return None

    def reload(self):
        if not self.is_reloading:
            self.is_reloading = True
            self.reload_timer = 60  # 1 second at 60 FPS

    def build(self, structures):
        if self.materials >= 10:
            structure = Structure(self.x + self.width//2, 
                                self.y + self.height//2)
            structures.append(structure)
            self.materials -= 10

    def draw(self, screen):
        # Draw player
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        
        # Draw health bar
        health_width = (self.health / MAX_HEALTH) * 50
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, 50, 5))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, health_width, 5))

# Bullet class
class Bullet:
    def __init__(self, x, y, direction, weapon_type):
        self.x = x
        self.y = y
        self.direction = direction
        self.weapon_type = weapon_type
        self.speed = BULLET_SPEED
        self.damage = 25 if weapon_type == "AR" else 50
        self.radius = 5 if weapon_type == "AR" else 8

    def move(self):
        self.x += self.speed * self.direction

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

# Structure class
class Structure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.health = 100

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))

# Game objects
player = Player(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
bullets = []
structures = []
enemies = []

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player.reload()
            elif event.key == pygame.K_q:
                player.current_weapon = (player.current_weapon + 1) % len(player.weapons)
            elif event.key == pygame.K_b:
                player.build(structures)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                bullet = player.shoot()
                if bullet:
                    bullets.append(bullet)

    # Get keyboard input
    keys = pygame.key.get_pressed()
    player.move(keys)

    # Update bullets
    for bullet in bullets[:]:
        bullet.move()
        if bullet.x < 0 or bullet.x > WINDOW_WIDTH:
            bullets.remove(bullet)

    # Update reload timer
    if player.is_reloading:
        player.reload_timer -= 1
        if player.reload_timer <= 0:
            player.is_reloading = False
            player.ammo[player.weapons[player.current_weapon]] = 30 if player.weapons[player.current_weapon] == "AR" else 8

    # Draw everything
    screen.fill(BLACK)
    
    # Draw structures
    for structure in structures:
        structure.draw(screen)
    
    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)
    
    # Draw player
    player.draw(screen)
    
    # Draw UI
    font = pygame.font.Font(None, 36)
    ammo_text = font.render(f"Ammo: {player.ammo[player.weapons[player.current_weapon]]}", True, WHITE)
    materials_text = font.render(f"Materials: {player.materials}", True, WHITE)
    weapon_text = font.render(f"Weapon: {player.weapons[player.current_weapon]}", True, WHITE)
    
    screen.blit(ammo_text, (10, 10))
    screen.blit(materials_text, (10, 50))
    screen.blit(weapon_text, (10, 90))
    
    if player.is_reloading:
        reload_text = font.render("RELOADING...", True, RED)
        screen.blit(reload_text, (WINDOW_WIDTH//2 - 100, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit() 