import pygame
from config import *
import snake
import food


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


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

snake_instance = snake.Snake(velocity=LEFT_VELOCITY)
food_instance = food.Food(snake_instance.body)
clock = pygame.time.Clock()

paused = False
game_over = False
running = True


def reset_game():
    global snake_instance, food_instance, game_over
    snake_instance = snake.Snake(velocity=LEFT_VELOCITY)
    food_instance = food.Food(snake_instance.body)
    game_over = False


def display_pause_screen():
    snake_instance.draw(screen)
    food_instance.draw(screen)
    font = pygame.font.Font(None, 100)
    text = font.render("PAUSED", True, WHITE)
    text_rect = text.get_rect()
    screen.blit(text, ((SCREEN_WIDTH - text_rect.width) // 2,
                       (SCREEN_HEIGHT - text_rect.height) // 2))


def display_game_over_screen():
    snake_instance.draw(screen)
    food_instance.draw(screen)
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


def draw_screen():
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.line(screen, WHITE, LINE_START, LINE_END, LINE_WIDTH)


def display_game():
    food_instance.update()
    if game_over:
        display_game_over_screen()
    elif paused:
        display_pause_screen()
    else:
        if snake_instance.body[0].topleft == food_instance.rect.topleft:
            snake_instance.grow_snake()
            food_instance.position = food_instance.reset_position(snake_instance.body)
        snake_instance.move()
        snake_instance.draw(screen)
        food_instance.draw(screen)


def check_for_game_over():
    global game_over
    if not game_over:
        if snake_instance.check_self_collision():
            game_over = True
            print("Game Over")


while running:
    # Check for event
    for event in pygame.event.get():
        handle_event()

    # Draw screen
    draw_screen()

    # Draw snake
    display_game()

    check_for_game_over()

    # Update screen
    pygame.display.flip()
    clock.tick(10)  # 10 FPS

pygame.quit()
