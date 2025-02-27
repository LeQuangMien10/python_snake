import pygame
from config import *
import snake
import food

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

snake_instance = snake.Snake(velocity=LEFT_VELOCITY)
food_instance = food.Food(snake_instance.body)
clock = pygame.time.Clock()

score = 0
level = DEFAULT_LEVEL
paused = False
game_over = False
running = True


# Control snake with keyboard.
def snake_control():
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        if snake_instance.velocity == RIGHT_VELOCITY or snake_instance.velocity == LEFT_VELOCITY:
            snake_instance.velocity = UP_VELOCITY
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        if snake_instance.velocity == RIGHT_VELOCITY or snake_instance.velocity == LEFT_VELOCITY:
            snake_instance.velocity = DOWN_VELOCITY
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        if snake_instance.velocity == UP_VELOCITY or snake_instance.velocity == DOWN_VELOCITY:
            snake_instance.velocity = LEFT_VELOCITY
    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        if snake_instance.velocity == UP_VELOCITY or snake_instance.velocity == DOWN_VELOCITY:
            snake_instance.velocity = RIGHT_VELOCITY


# Reset game
def reset_game():
    global snake_instance, food_instance, game_over, score
    snake_instance = snake.Snake(velocity=LEFT_VELOCITY)
    food_instance = food.Food(snake_instance.body)
    game_over = False
    score = 0


# Draw dynamic components (snake, food, score)
def draw_dynamic_components():
    snake_instance.draw(screen)
    food_instance.draw(screen)
    draw_score()


# Display pause screen
def display_pause_screen():
    draw_dynamic_components()
    font = pygame.font.Font(None, 100)
    text = font.render("PAUSED", True, WHITE)
    text_rect = text.get_rect()
    screen.blit(text, ((SCREEN_WIDTH - text_rect.width) // 2,
                       (SCREEN_HEIGHT - text_rect.height) // 2))


# Display game over screen
def display_game_over_screen():
    draw_dynamic_components()
    game_over_font = pygame.font.Font(None, 100)
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    game_over_text_rect = game_over_text.get_rect()

    guide_font = pygame.font.Font(None, 50)
    guide_text = guide_font.render("Press R to restart!!", True, WHITE)
    guide_text_rect = guide_text.get_rect()

    screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text_rect.width) // 2,
                                 (SCREEN_HEIGHT - (game_over_text_rect.height + guide_text_rect.height)) // 2))
    screen.blit(guide_text, ((SCREEN_WIDTH - guide_text_rect.width) // 2,
                             (SCREEN_HEIGHT - (game_over_text_rect.height + guide_text_rect.height)) // 2 +
                             game_over_text_rect.height))


# Handle quit, pause, game over
def handle_event():
    global running, paused, game_over
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE and not game_over:
            paused = not paused
        elif event.key == pygame.K_r:
            reset_game()
        if not paused:
            snake_control()


# Draw static components
def draw_screen():
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.line(screen, WHITE, LINE_START, LINE_END, LINE_WIDTH)


# Game logic
def display_game():
    food_instance.update()
    if game_over:
        display_game_over_screen()
    elif paused:
        display_pause_screen()
    else:
        handle_snake_eats_food()
        snake_instance.move()
        draw_dynamic_components()


def draw_score():
    font = pygame.font.Font(None, 50)
    score_text = font.render("Score: " + str(score), True, WHITE)
    score_text_rect = score_text.get_rect()
    screen.blit(score_text, (10, 10))


# Handle snake eats food
def handle_snake_eats_food():
    global score
    if snake_instance.body[0].topleft == food_instance.rect.topleft:
        score += level
        snake_instance.grow_snake()
        food_instance.position = food_instance.reset_position(snake_instance.body)


# Check for game over
def check_for_game_over():
    global game_over
    if not game_over:
        if snake_instance.check_self_collision():
            game_over = True
            # print("Game Over")


# Main loop
while running:
    # Check for event
    for event in pygame.event.get():
        handle_event()

    # Draw screen
    draw_screen()

    display_game()

    check_for_game_over()

    # Update screen
    pygame.display.flip()
    clock.tick(DEFAULT_FPS)  # 10 FPS

pygame.quit()
