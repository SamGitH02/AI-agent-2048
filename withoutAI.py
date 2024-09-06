import pygame
import random

# Game constants
GRID_SIZE = 4
TILE_SIZE = 100
WIDTH = GRID_SIZE * TILE_SIZE
HEIGHT = GRID_SIZE * TILE_SIZE
FPS = 30

# Colors (you can customize these)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()

# Game variables
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]  # Initialize empty grid
score = 0

# Function to add a new tile
def add_new_tile():
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = 2 if random.random() < 0.9 else 4

# Function to draw the game board
def draw_board():
    screen.fill(BLACK)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_value = grid[i][j]
            tile_color = WHITE if tile_value == 0 else GRAY  # Example colors, adjust as needed
            pygame.draw.rect(screen, tile_color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile_value != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(tile_value), True, BLACK)
                text_rect = text.get_rect(center=((j + 0.5) * TILE_SIZE, (i + 0.5) * TILE_SIZE))
                screen.blit(text, text_rect)

# Function to compress the grid in a given direction
def compress(grid, direction):
    changed = False
    new_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

    if direction == "left":
        for i in range(GRID_SIZE):
            pos = 0
            for j in range(GRID_SIZE):
                if grid[i][j] != 0:
                    new_grid[i][pos] = grid[i][j]
                    if j != pos:
                        changed = True
                    pos += 1
    elif direction == "right":
        for i in range(GRID_SIZE):
            pos = GRID_SIZE - 1
            for j in range(GRID_SIZE - 1, -1, -1):
                if grid[i][j] != 0:
                    new_grid[i][pos] = grid[i][j]
                    if j != pos:
                        changed = True
                    pos -= 1
    elif direction == "up":
        for j in range(GRID_SIZE):
            pos = 0
            for i in range(GRID_SIZE):
                if grid[i][j] != 0:
                    new_grid[pos][j] = grid[i][j]
                    if i != pos:
                        changed = True
                    pos += 1
    elif direction == "down":
        for j in range(GRID_SIZE):
            pos = GRID_SIZE - 1
            for i in range(GRID_SIZE - 1, -1, -1):
                if grid[i][j] != 0:
                    new_grid[pos][j] = grid[i][j]
                    if i != pos:
                        changed = True
                    pos -= 1

    return new_grid, changed

# Function to merge tiles in a given direction
def merge(grid, direction):
    global score
    changed = False

    if direction == "left":
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                if grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                    grid[i][j] *= 2
                    grid[i][j + 1] = 0
                    score += grid[i][j]
                    changed = True
    elif direction == "right":
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1, 0, -1):
                if grid[i][j] == grid[i][j - 1] and grid[i][j] != 0:
                    grid[i][j] *= 2
                    grid[i][j - 1] = 0
                    score += grid[i][j]
                    changed = True
    elif direction == "up":
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE - 1):
                if grid[i][j] == grid[i + 1][j] and grid[i][j] != 0:
                    grid[i][j] *= 2
                    grid[i + 1][j] = 0
                    score += grid[i][j]
                    changed = True
    elif direction == "down":
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE - 1, 0, -1):
                if grid[i][j] == grid[i - 1][j] and grid[i][j] != 0:
                    grid[i][j] *= 2
                    grid[i - 1][j] = 0
                    score += grid[i][j]
                    changed = True

    return grid, changed

# Function to handle a move in a given direction
def move(direction):
    global grid
    grid, changed1 = compress(grid, direction)
    grid, changed2 = merge(grid, direction)
    grid, _ = compress(grid, direction)  # Compress again after merging
    if changed1 or changed2:
        add_new_tile()

# Function to check if the game is over
def game_over():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return False
            if j < GRID_SIZE - 1 and grid[i][j] == grid[i][j + 1]:
                return False
            if i < GRID_SIZE - 1 and grid[i][j] == grid[i + 1][j]:
                return False
    return True

# Game loop
running = True
add_new_tile()
add_new_tile()  # Start with two tiles

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move("left")
            elif event.key == pygame.K_RIGHT:
                move("right")
            elif event.key == pygame.K_UP:
                move("up")
            elif event.key == pygame.K_DOWN:
                move("down")

    # Check for game over after each move
    if game_over():
        print("Game Over!")
        running = False

    draw_board()
    pygame.display.flip()

pygame.quit()