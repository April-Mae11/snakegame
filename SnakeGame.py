import pygame
import random
import sys

# ---------------------------
# CONFIG
# ---------------------------
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FONT_NAME = "freesansbold.ttf"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
YELLOW = (255, 215, 0)
PURPLE = (180, 0, 255)
GRAY_OVERLAY = (0, 0, 0, 160)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# ---------------------------
# HELPERS
# ---------------------------
def draw_cell(surface, pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)

def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))

def random_food_position(snake):
    positions = {(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}
    positions -= set(snake)
    return random.choice(list(positions))

# ---------------------------
# MAIN GAME FUNCTION
# ---------------------------
def game(level_speed):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Twist")
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_NAME, 20)
    big_font = pygame.font.Font(FONT_NAME, 48)

    # Initialize snake
    init_x = GRID_WIDTH // 2
    init_y = GRID_HEIGHT // 2
    snake = [(init_x, init_y), (init_x - 1, init_y), (init_x - 2, init_y)]
    direction = RIGHT
    next_direction = direction

    food = random_food_position(snake)
    bad_food = None
    score = 0
    fps = level_speed
    paused = False
    game_over = False
    twist_timer = 0
    twist_interval = random.randint(10, 20)  # random delay for bad food

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    next_direction = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    next_direction = DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    next_direction = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    next_direction = RIGHT
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r and game_over:
                    return True  # restart
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not paused and not game_over:
            # Prevent instant reverse
            if (next_direction[0] * -1, next_direction[1] * -1) != direction:
                direction = next_direction

            # Move head
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)  # wrap-around

            # Collision with self
            if new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)

                # Check if eaten normal food
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                    fps += 0.5
                    twist_timer += 1

                    # Maybe spawn bad food
                    if twist_timer >= twist_interval:
                        bad_food = random_food_position(snake)
                        twist_timer = 0
                        twist_interval = random.randint(10, 20)

                # Check if eaten bad food
                elif bad_food and new_head == bad_food:
                    score = max(0, score - 1)
                    bad_food = None
                    if len(snake) > 3:
                        snake.pop()
                        snake.pop()
                    else:
                        game_over = True
                else:
                    snake.pop()

        # DRAW
        screen.fill(BLACK)
        draw_grid(screen)

        # Draw food
        draw_cell(screen, food, RED)
        if bad_food:
            draw_cell(screen, bad_food, PURPLE)

        # Draw snake
        for i, segment in enumerate(snake):
            color = GREEN if i == 0 else YELLOW
            draw_cell(screen, segment, color)

        # HUD
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (8, 8))
        fps_text = font.render(f"Speed: {int(fps)}", True, WHITE)
        screen.blit(fps_text, (WINDOW_WIDTH - 120, 8))

        # Pause overlay
        if paused:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill(GRAY_OVERLAY)
            screen.blit(overlay, (0, 0))
            pause_text = big_font.render("PAUSED", True, WHITE)
            rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(pause_text, rect)

        # Game Over overlay
        if game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill(GRAY_OVERLAY)
            screen.blit(overlay, (0, 0))
            go_text = big_font.render("GAME OVER", True, RED)
            go_rect = go_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            screen.blit(go_text, go_rect)
            info = font.render("Press R to Restart or ESC to Quit", True, WHITE)
            info_rect = info.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            screen.blit(info, info_rect)

        pygame.display.flip()
        clock.tick(int(fps))


# ---------------------------
# MENU FUNCTION
# ---------------------------
def show_menu():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Twist - Menu")
    font = pygame.font.Font(FONT_NAME, 28)
    big_font = pygame.font.Font(FONT_NAME, 50)

    while True:
        screen.fill(BLACK)
        title = big_font.render("SNAKE TWIST", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        screen.blit(title, title_rect)

        easy = font.render("1. Easy", True, WHITE)
        medium = font.render("2. Medium", True, WHITE)
        hard = font.render("3. Hard", True, WHITE)
        screen.blit(easy, (WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 - 20))
        screen.blit(medium, (WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 + 20))
        screen.blit(hard, (WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 + 60))

        info = font.render("Press ESC to Exit", True, DARK_GRAY)
        info_rect = info.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        screen.blit(info, info_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 6
                elif event.key == pygame.K_2:
                    return 10
                elif event.key == pygame.K_3:
                    return 14
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# ---------------------------
# MAIN LOOP
# ---------------------------
if __name__ == "__main__":
    while True:
        level_speed = show_menu()
        restart = game(level_speed)
        if not restart:
            break
