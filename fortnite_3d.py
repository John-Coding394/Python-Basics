import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SPEED = 0.1  # Reduced speed for smoother movement
BULLET_SPEED = 0.5  # Reduced bullet speed
GRAVITY = -0.05    # Reduced gravity
JUMP_STRENGTH = 0.2  # Reduced jump strength
SKY_SIZE = 200
MAX_HEALTH = 100
MAX_MATERIALS = 100
MAX_AMMO = 30
RELOAD_TIME = 60
MOUSE_SENSITIVITY = 0.2  # Added mouse sensitivity control

class Bullet:
    def __init__(self, pos, direction):
        self.pos = list(pos)
        self.direction = direction
        self.lifetime = 100
        self.damage = 25

    def update(self):
        # Smooth bullet movement
        self.pos[0] += self.direction[0] * BULLET_SPEED
        self.pos[1] += self.direction[1] * BULLET_SPEED
        self.pos[2] += self.direction[2] * BULLET_SPEED
        self.lifetime -= 1

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        
        # Optimized bullet rendering
        glBegin(GL_QUADS)
        glColor3f(1, 1, 0)  # Yellow color
        # Front face
        glVertex3f(-0.1, -0.1, 0.1)
        glVertex3f(0.1, -0.1, 0.1)
        glVertex3f(0.1, 0.1, 0.1)
        glVertex3f(-0.1, 0.1, 0.1)
        # Back face
        glVertex3f(-0.1, -0.1, -0.1)
        glVertex3f(-0.1, 0.1, -0.1)
        glVertex3f(0.1, 0.1, -0.1)
        glVertex3f(0.1, -0.1, -0.1)
        glEnd()
        
        glPopMatrix()

class Structure:
    def __init__(self, pos):
        self.pos = list(pos)
        self.size = 1.0
        self.health = 100

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        
        # Optimized structure rendering
        glBegin(GL_QUADS)
        glColor3f(0.5, 0.5, 0.5)  # Gray color
        # Front face
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        # Back face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        # Top face
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)
        # Bottom face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glEnd()
        
        glPopMatrix()

class Player:
    def __init__(self):
        self.pos = [0, 0, -5]
        self.rot = [0, 0]
        self.velocity = [0, 0, 0]
        self.health = MAX_HEALTH
        self.bullets = []
        self.structures = []
        self.materials = MAX_MATERIALS
        self.ammo = MAX_AMMO
        self.max_ammo = MAX_AMMO
        self.reloading = False
        self.reload_time = 0
        self.score = 0
        self.is_jumping = False
        self.last_shoot_time = 0
        self.shoot_cooldown = 0.1  # 100ms cooldown between shots

    def move(self, dx, dy, dz):
        # Smooth movement with proper rotation
        angle = math.radians(self.rot[0])
        self.pos[0] += dx * math.cos(angle) - dz * math.sin(angle)
        self.pos[2] += dx * math.sin(angle) + dz * math.cos(angle)
        self.pos[1] += dy

    def update(self, current_time):
        # Smooth physics update
        self.velocity[1] += GRAVITY
        self.pos[1] += self.velocity[1]
        
        # Ground collision with proper bounce damping
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.velocity[1] = 0
            self.is_jumping = False

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.lifetime <= 0:
                self.bullets.remove(bullet)

        # Handle reloading
        if self.reloading:
            self.reload_time -= 1
            if self.reload_time <= 0:
                self.ammo = self.max_ammo
                self.reloading = False

    def shoot(self, current_time):
        if (self.ammo > 0 and not self.reloading and 
            current_time - self.last_shoot_time >= self.shoot_cooldown):
            angle_h = math.radians(self.rot[0])
            angle_v = math.radians(self.rot[1])
            
            direction = [
                math.cos(angle_v) * math.sin(angle_h),
                -math.sin(angle_v),
                math.cos(angle_v) * math.cos(angle_h)
            ]
            
            self.bullets.append(Bullet(self.pos, direction))
            self.ammo -= 1
            self.last_shoot_time = current_time

    def reload(self):
        if not self.reloading and self.ammo < self.max_ammo:
            self.reloading = True
            self.reload_time = RELOAD_TIME

    def build(self):
        if self.materials >= 10:
            angle = math.radians(self.rot[0])
            build_pos = [
                self.pos[0] + 2 * math.sin(angle),
                self.pos[1],
                self.pos[2] + 2 * math.cos(angle)
            ]
            self.structures.append(Structure(build_pos))
            self.materials -= 10

def draw_sky():
    glPushMatrix()
    glColor3f(0.4, 0.6, 1.0)  # Light blue color
    
    # Optimized sky rendering
    glBegin(GL_QUADS)
    # Front face
    glVertex3f(-SKY_SIZE, -SKY_SIZE, SKY_SIZE)
    glVertex3f(SKY_SIZE, -SKY_SIZE, SKY_SIZE)
    glVertex3f(SKY_SIZE, SKY_SIZE, SKY_SIZE)
    glVertex3f(-SKY_SIZE, SKY_SIZE, SKY_SIZE)
    
    # Back face
    glVertex3f(-SKY_SIZE, -SKY_SIZE, -SKY_SIZE)
    glVertex3f(-SKY_SIZE, SKY_SIZE, -SKY_SIZE)
    glVertex3f(SKY_SIZE, SKY_SIZE, -SKY_SIZE)
    glVertex3f(SKY_SIZE, -SKY_SIZE, -SKY_SIZE)
    
    # Top face
    glVertex3f(-SKY_SIZE, SKY_SIZE, -SKY_SIZE)
    glVertex3f(-SKY_SIZE, SKY_SIZE, SKY_SIZE)
    glVertex3f(SKY_SIZE, SKY_SIZE, SKY_SIZE)
    glVertex3f(SKY_SIZE, SKY_SIZE, -SKY_SIZE)
    
    # Left face
    glVertex3f(-SKY_SIZE, -SKY_SIZE, -SKY_SIZE)
    glVertex3f(-SKY_SIZE, -SKY_SIZE, SKY_SIZE)
    glVertex3f(-SKY_SIZE, SKY_SIZE, SKY_SIZE)
    glVertex3f(-SKY_SIZE, SKY_SIZE, -SKY_SIZE)
    
    # Right face
    glVertex3f(SKY_SIZE, -SKY_SIZE, -SKY_SIZE)
    glVertex3f(SKY_SIZE, SKY_SIZE, -SKY_SIZE)
    glVertex3f(SKY_SIZE, SKY_SIZE, SKY_SIZE)
    glVertex3f(SKY_SIZE, -SKY_SIZE, SKY_SIZE)
    glEnd()
    
    glPopMatrix()

def draw_hud(screen, player):
    # Create a font object
    font = pygame.font.Font(None, 36)
    
    # Health bar
    health_text = font.render(f"Health: {player.health}/{MAX_HEALTH}", True, (255, 255, 255))
    screen.blit(health_text, (10, 10))
    
    # Ammo counter
    ammo_text = font.render(f"Ammo: {player.ammo}/{MAX_AMMO}", True, (255, 255, 255))
    screen.blit(ammo_text, (10, 50))
    
    # Materials counter
    materials_text = font.render(f"Materials: {player.materials}/{MAX_MATERIALS}", True, (255, 255, 255))
    screen.blit(materials_text, (10, 90))
    
    # Score
    score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 130))
    
    # Reloading indicator
    if player.reloading:
        reload_text = font.render("RELOADING...", True, (255, 0, 0))
        screen.blit(reload_text, (WINDOW_WIDTH//2 - 100, 10))
    
    # Crosshair
    pygame.draw.circle(screen, (255, 255, 255), (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), 5, 1)
    pygame.draw.line(screen, (255, 255, 255), (WINDOW_WIDTH//2 - 10, WINDOW_HEIGHT//2), 
                    (WINDOW_WIDTH//2 + 10, WINDOW_HEIGHT//2), 1)
    pygame.draw.line(screen, (255, 255, 255), (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 10), 
                    (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 10), 1)

def main():
    pygame.init()
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Fortnite Clone")
    
    # Hide mouse cursor and grab input
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    # Set up the 3D view
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)

    player = Player()
    clock = pygame.time.Clock()
    last_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds

    while True:
        current_time = pygame.time.get_ticks() / 1000.0
        delta_time = current_time - last_time
        last_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_jumping:
                    player.velocity[1] = JUMP_STRENGTH
                    player.is_jumping = True
                elif event.key == pygame.K_r:
                    player.reload()
                elif event.key == pygame.K_b:
                    player.build()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        # Handle mouse movement for looking around
        if pygame.mouse.get_focused():
            mouse_movement = pygame.mouse.get_rel()
            player.rot[0] += mouse_movement[0] * MOUSE_SENSITIVITY
            player.rot[1] = max(-90, min(90, player.rot[1] - mouse_movement[1] * MOUSE_SENSITIVITY))

        # Handle keyboard input for movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, 0, PLAYER_SPEED * delta_time * 60)
        if keys[pygame.K_s]:
            player.move(0, 0, -PLAYER_SPEED * delta_time * 60)
        if keys[pygame.K_a]:
            player.move(-PLAYER_SPEED * delta_time * 60, 0, 0)
        if keys[pygame.K_d]:
            player.move(PLAYER_SPEED * delta_time * 60, 0, 0)

        # Handle mouse buttons
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left click
            player.shoot(current_time)

        player.update(current_time)

        # Clear the screen and reset the view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply player rotation and position
        glRotatef(player.rot[1], 1, 0, 0)
        glRotatef(player.rot[0], 0, 1, 0)
        glTranslatef(-player.pos[0], -player.pos[1], -player.pos[2])

        # Draw sky
        draw_sky()

        # Draw the ground
        glBegin(GL_QUADS)
        glColor3f(0.2, 0.8, 0.2)
        glVertex3f(-100, 0, -100)
        glVertex3f(-100, 0, 100)
        glVertex3f(100, 0, 100)
        glVertex3f(100, 0, -100)
        glEnd()

        # Draw bullets
        for bullet in player.bullets:
            bullet.draw()

        # Draw structures
        for structure in player.structures:
            structure.draw()

        # Draw HUD
        pygame.display.flip()
        screen = pygame.display.get_surface()
        draw_hud(screen, player)
        pygame.display.flip()
        
        clock.tick(60)

if __name__ == "__main__":
    main()