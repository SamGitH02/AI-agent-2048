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
best_score=0

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
        # Display current score and best score
        font = pygame.font.Font(None, 30)
        score_text = font.render(f"Score: {score}", True, WHITE)
        best_score_text = font.render(f"Best: {best_score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 40))
        screen.blit(best_score_text, (WIDTH - 10 - best_score_text.get_width(), HEIGHT - 40))


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
    global score, best_score
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
    #update best score
    best_score=max(score,best_score)
    return grid, changed

# Function to handle a move in a given direction
def move(grid,direction):

    grid, changed1 = compress(grid, direction)
    grid, changed2 = merge(grid, direction)
    grid, _ = compress(grid, direction)  # Compress again after merging
    if changed1 or changed2:
        return grid, True  # Return the updated grid
    else:
        return grid, False
        

# Function to check if the game is over
def game_over(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return False
            if j < GRID_SIZE - 1 and grid[i][j] == grid[i][j + 1]:
                return False
            if i < GRID_SIZE - 1 and grid[i][j] == grid[i + 1][j]:
                return False
    return True
# Heuristic functions
def monotonicity(grid):
    score = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - 1):
            if grid[i][j] >= grid[i][j + 1]:
                score += 1
            if grid[j][i] >= grid[j + 1][i]:
                score += 1
    return score

def smoothness(grid):
    score = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - 1):
            if grid[i][j] != 0 and grid[i][j + 1] != 0:
                score -= abs(grid[i][j] - grid[i][j + 1])
            if grid[j][i] != 0 and grid[j + 1][i] != 0:
                score -= abs(grid[j][i] - grid[j + 1][i])
    return score

def free_tiles(grid):
    count = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                count += 1
    return count
# Expectimax algorithm
def expectimax(grid, depth, maximizing_player):
    if depth == 0 or game_over(grid):
        return None, monotonicity(grid) + smoothness(grid) + free_tiles(grid)

    if maximizing_player:
        best_score = -float('inf')
        best_move = None

        for direction in ["left", "right", "up", "down"]:
            new_grid, changed = move([row[:] for row in grid], direction) 

            if changed:
                _, new_score = expectimax(new_grid, depth - 1, False)
                if new_score > best_score:
                    best_score = new_score
                    best_move = direction

        return best_move, best_score

    else:  # Environment's turn (chance node)
        total_score = 0
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]

        for row, col in empty_cells:
            for value in [2, 4]:
                new_grid = [row[:] for row in grid]
                new_grid[row][col] = value
                _, new_score = expectimax(new_grid, depth - 1, True)
                total_score += new_score * (0.9 if value == 2 else 0.1) 

        average_score = total_score / len(empty_cells) if empty_cells else 0 
        return None, average_score

# Function to display the game over pop-up
def show_game_over_popup():
    popup_width = 300
    popup_height = 200
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    popup_surface = pygame.Surface((popup_width, popup_height))
    popup_surface.fill(GRAY)
    popup_rect = popup_surface.get_rect(topleft=(popup_x, popup_y))

    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over!", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=(popup_width // 2, popup_height // 2 - 30))

    final_score_text = font.render(f"Score: {score}", True, BLACK)
    final_score_rect = final_score_text.get_rect(center=(popup_width // 2, popup_height // 2 + 30))

    popup_surface.blit(game_over_text, game_over_rect)
    popup_surface.blit(final_score_text, final_score_rect)
    screen.blit(popup_surface, popup_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting= False

# Game loop
running = True

add_new_tile() 

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # AI's turn
    best_move, _ = expectimax(grid, 3, True)  # Adjust depth as needed
    if best_move:
        grid, _ = move(grid, best_move)
        add_new_tile() 

    if game_over(grid):
        show_game_over_popup()
        running = False

    draw_board()
    pygame.display.flip()

pygame.quit()


