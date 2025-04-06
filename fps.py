import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SPEED = 0.5
BULLET_SPEED = 1.0
GRAVITY = -0.1
JUMP_STRENGTH = 1.0

class Bullet:
    def __init__(self, pos, direction):
        self.pos = list(pos)
        self.direction = direction
        self.lifetime = 100

    def update(self):
        self.pos[0] += self.direction[0] * BULLET_SPEED
        self.pos[1] += self.direction[1] * BULLET_SPEED
        self.pos[2] += self.direction[2] * BULLET_SPEED
        self.lifetime -= 1

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        
        # Draw a simple cube instead of a sphere
        glBegin(GL_QUADS)
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

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        
        glBegin(GL_QUADS)
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
        self.health = 100
        self.bullets = []
        self.structures = []
        self.materials = 100
        self.ammo = 30
        self.max_ammo = 30
        self.reloading = False
        self.reload_time = 0

    def move(self, dx, dy, dz):
        # Apply rotation to movement
        angle = math.radians(self.rot[0])
        self.pos[0] += dx * math.cos(angle) - dz * math.sin(angle)
        self.pos[2] += dx * math.sin(angle) + dz * math.cos(angle)
        self.pos[1] += dy

    def update(self):
        # Apply gravity
        self.velocity[1] += GRAVITY
        self.pos[1] += self.velocity[1]
        
        # Ground collision
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.velocity[1] = 0

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

    def shoot(self):
        if self.ammo > 0 and not self.reloading:
            angle_h = math.radians(self.rot[0])
            angle_v = math.radians(self.rot[1])
            
            direction = [
                math.cos(angle_v) * math.sin(angle_h),
                -math.sin(angle_v),
                math.cos(angle_v) * math.cos(angle_h)
            ]
            
            self.bullets.append(Bullet(self.pos, direction))
            self.ammo -= 1

    def reload(self):
        if not self.reloading and self.ammo < self.max_ammo:
            self.reloading = True
            self.reload_time = 60  # 1 second at 60 FPS

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

def main():
    pygame.init()
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Fortnite Clone")

    # Set up the 3D view
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    player = Player()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.pos[1] == 0:
                    player.velocity[1] = JUMP_STRENGTH
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
            player.rot[0] += mouse_movement[0] * 0.1
            player.rot[1] = max(-90, min(90, player.rot[1] - mouse_movement[1] * 0.1))

        # Handle keyboard input for movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, 0, PLAYER_SPEED)
        if keys[pygame.K_s]:
            player.move(0, 0, -PLAYER_SPEED)
        if keys[pygame.K_a]:
            player.move(-PLAYER_SPEED, 0, 0)
        if keys[pygame.K_d]:
            player.move(PLAYER_SPEED, 0, 0)

        # Handle mouse buttons
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left click
            player.shoot()

        player.update()

        # Clear the screen and reset the view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply player rotation and position
        glRotatef(player.rot[1], 1, 0, 0)
        glRotatef(player.rot[0], 0, 1, 0)
        glTranslatef(-player.pos[0], -player.pos[1], -player.pos[2])

        # Draw the ground
        glBegin(GL_QUADS)
        glColor3f(0.2, 0.8, 0.2)
        glVertex3f(-100, 0, -100)
        glVertex3f(-100, 0, 100)
        glVertex3f(100, 0, 100)
        glVertex3f(100, 0, -100)
        glEnd()

        # Draw bullets
        glColor3f(1, 1, 0)
        for bullet in player.bullets:
            bullet.draw()

        # Draw structures
        glColor3f(0.5, 0.5, 0.5)
        for structure in player.structures:
            structure.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()