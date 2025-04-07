# ... existing code ...

# Maze layout (1 = wall, 0 = path)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Update window dimensions to match new maze size
WINDOW_WIDTH = len(maze[0]) * GRID_SIZE
WINDOW_HEIGHT = len(maze) * GRID_SIZE

# Update screen size
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Update power-up positions for new maze
powerups = []
for y in range(len(maze)):
    for x in range(len(maze[0])):
        if maze[y][x] == 0:
            screen_x, screen_y = maze_to_screen(x, y)
            dots.append((screen_x, screen_y))
            # Add power-ups at corners
            if (x, y) in [(1, 1), (18, 1), (1, 18), (18, 18)]:
                powerups.append((screen_x, screen_y))

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

def draw_maze():
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLUE, 
                               (x * GRID_SIZE, y * GRID_SIZE, 
                                GRID_SIZE, GRID_SIZE))

def draw_pacman(x, y, direction, mouth_open):
    if mouth_open:
        pygame.draw.arc(screen, YELLOW, 
                       (x - GRID_SIZE//2, y - GRID_SIZE//2, 
                        GRID_SIZE, GRID_SIZE),
                       direction * 3.14/2, (direction + 1) * 3.14/2, 
                       GRID_SIZE//2)
    else:
        pygame.draw.circle(screen, YELLOW, (x, y), GRID_SIZE//2)

def move_ghost(ghost):
    if random.random() < 0.02:  # 2% chance to change direction
        ghost["direction"] = random.randint(0, 3)
    
    new_x, new_y = ghost["x"], ghost["y"]
    if ghost["direction"] == 0:  # Right
        new_x = min(new_x + GHOST_SPEED, WINDOW_WIDTH - GRID_SIZE)
    elif ghost["direction"] == 1:  # Down
        new_y = min(new_y + GHOST_SPEED, WINDOW_HEIGHT - GRID_SIZE)
    elif ghost["direction"] == 2:  # Left
        new_x = max(new_x - GHOST_SPEED, GRID_SIZE)
    elif ghost["direction"] == 3:  # Up
        new_y = max(new_y - GHOST_SPEED, GRID_SIZE)
    
    if is_valid_position(new_x, new_y):
        ghost["x"], ghost["y"] = new_x, new_y

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pacman_direction = 0
            elif event.key == pygame.K_DOWN:
                pacman_direction = 1
            elif event.key == pygame.K_LEFT:
                pacman_direction = 2
            elif event.key == pygame.K_UP:
                pacman_direction = 3
            elif event.key == pygame.K_ESCAPE:
                running = False

    # Move Pacman
    new_x, new_y = pacman_x, pacman_y
    if pacman_direction == 0:  # Right
        new_x = min(pacman_x + PACMAN_SPEED, WINDOW_WIDTH - GRID_SIZE)
    elif pacman_direction == 1:  # Down
        new_y = min(pacman_y + PACMAN_SPEED, WINDOW_HEIGHT - GRID_SIZE)
    elif pacman_direction == 2:  # Left
        new_x = max(pacman_x - PACMAN_SPEED, GRID_SIZE)
    elif pacman_direction == 3:  # Up
        new_y = max(pacman_y - PACMAN_SPEED, GRID_SIZE)
    
    if is_valid_position(new_x, new_y):
        pacman_x, pacman_y = new_x, new_y

    # Move ghosts
    for ghost in ghosts:
        move_ghost(ghost)

    # Check for dot collection
    for dot in dots[:]:
        if abs(pacman_x - dot[0]) < GRID_SIZE and abs(pacman_y - dot[1]) < GRID_SIZE:
            dots.remove(dot)
            score += 10

    # Check for power-up collection
    for powerup in powerups[:]:
        if abs(pacman_x - powerup[0]) < GRID_SIZE and abs(pacman_y - powerup[1]) < GRID_SIZE:
            powerups.remove(powerup)
            powered_up = True
            power_up_timer = pygame.time.get_ticks()

    # Check power-up duration
    if powered_up and pygame.time.get_ticks() - power_up_timer > POWERUP_DURATION:
        powered_up = False

    # Check for collision with ghosts
    for ghost in ghosts:
        if abs(pacman_x - ghost["x"]) < GRID_SIZE and abs(pacman_y - ghost["y"]) < GRID_SIZE:
            if powered_up:
                # Reset ghost position
                ghost["x"], ghost["y"] = find_valid_position()
                score += 50
            else:
                print(f"Game Over! Final Score: {score}")
                running = False

    # Animate Pacman's mouth
    pacman_mouth_timer += 1
    if pacman_mouth_timer > 10:
        pacman_mouth_open = not pacman_mouth_open
        pacman_mouth_timer = 0

    # Draw everything
    screen.fill(BLACK)
    draw_maze()
    
    # Draw dots
    for dot in dots:
        pygame.draw.circle(screen, WHITE, dot, 3)
    
    # Draw power-ups
    for powerup in powerups:
        pygame.draw.circle(screen, ORANGE, powerup, 5)
    
    # Draw Pacman
    draw_pacman(pacman_x, pacman_y, pacman_direction, pacman_mouth_open)
    
    # Draw ghosts
    for ghost in ghosts:
        ghost_color = CYAN if powered_up else ghost["color"]
        pygame.draw.rect(screen, ghost_color, 
                        (ghost["x"] - GRID_SIZE//2, ghost["y"] - GRID_SIZE//2, 
                         GRID_SIZE, GRID_SIZE))
    
    # Draw score and power-up status
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    if powered_up:
        power_text = font.render("POWERED UP!", True, ORANGE)
        screen.blit(power_text, (WINDOW_WIDTH - 150, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()