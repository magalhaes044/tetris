import pygame
import random

# Initialize the game
pygame.init()

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Set the width and height of the screen
screen_width = 800
screen_height = 600
block_size = 30

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Define the shapes of the Tetriminos
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# Define the colors of the Tetriminos
colors = [CYAN, YELLOW, MAGENTA, GREEN, BLUE, ORANGE, RED]

# Function to create a new Tetrimino
def create_tetrimino():
    shape = random.choice(shapes)
    color = random.choice(colors)
    x = screen_width // 2 - len(shape[0]) * block_size // 2
    y = -len(shape) * block_size
    return {
        'shape': shape,
        'color': color,
        'x': x,
        'y': y
    }

# Function to draw a Tetrimino on the screen
def draw_tetrimino(tetrimino):
    for i in range(len(tetrimino['shape'])):
        for j in range(len(tetrimino['shape'][0])):
            if tetrimino['shape'][i][j] == 1:
                pygame.draw.rect(screen, tetrimino['color'], (tetrimino['x'] + j * block_size, tetrimino['y'] + i * block_size, block_size, block_size))

# Function to check if a Tetrimino is colliding with the walls or other Tetriminos
def is_collision(tetrimino, tetriminos):
    for i in range(len(tetrimino['shape'])):
        for j in range(len(tetrimino['shape'][0])):
            if tetrimino['shape'][i][j] == 1:
                if tetrimino['x'] + j * block_size < 0 or tetrimino['x'] + j * block_size >= screen_width or tetrimino['y'] + i * block_size >= screen_height:
                    return True
                for other_tetrimino in tetriminos:
                    if tetrimino['y'] + i * block_size == other_tetrimino['y'] and tetrimino['x'] + j * block_size == other_tetrimino['x']:
                        return True
    return False

# Function to check if a row is full
def is_row_full(row, tetriminos):
    for tetrimino in tetriminos:
        for i in range(len(tetrimino['shape'])):
            if tetrimino['y'] + i * block_size == row:
                return True
    return False

# Function to remove a full row
def remove_full_rows(tetriminos):
    full_rows = []
    for i in range(screen_height // block_size):
        if is_row_full(i * block_size, tetriminos):
            full_rows.append(i * block_size)
    for row in full_rows:
        for tetrimino in tetriminos:
            if tetrimino['y'] < row:
                tetrimino['y'] += block_size
            elif tetrimino['y'] == row:
                tetriminos.remove(tetrimino)

# Initialize the game state
tetriminos = []
current_tetrimino = create_tetrimino()
score = 0

game_over = False

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetrimino['x'] -= block_size
                if is_collision(current_tetrimino, tetriminos):
                    current_tetrimino['x'] += block_size

            elif event.key == pygame.K_RIGHT:
                current_tetrimino['x'] += block_size
                if is_collision(current_tetrimino, tetriminos):
                    current_tetrimino['x'] -= block_size

            elif event.key == pygame.K_DOWN:
                current_tetrimino['y'] += block_size
                if is_collision(current_tetrimino, tetriminos):
                    current_tetrimino['y'] -= block_size

    # Move the current Tetrimino down
    current_tetrimino['y'] += block_size
    if is_collision(current_tetrimino, tetriminos):
        current_tetrimino['y'] -= block_size
        tetriminos.append(current_tetrimino)
        current_tetrimino = create_tetrimino()
        remove_full_rows(tetriminos)
        score += 1

    # Clear the screen
    screen.fill(BLACK)

    # Draw the Tetriminos
    for tetrimino in tetriminos:
        draw_tetrimino(tetrimino)

    draw_tetrimino(current_tetrimino)

    # Draw the score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

    # Update the screen
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(10)

# Quit the game
pygame.quit()