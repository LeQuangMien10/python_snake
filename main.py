import pygame
from config import *
import snake
import food

def snake_control():
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        if snake.velocity == RIGHT_VELOCITY or snake.velocity == LEFT_VELOCITY:
            snake.velocity = UP_VELOCITY
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        if snake.velocity == RIGHT_VELOCITY or snake.velocity == LEFT_VELOCITY:
            snake.velocity = DOWN_VELOCITY
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        if snake.velocity == UP_VELOCITY or snake.velocity == DOWN_VELOCITY:
            snake.velocity = LEFT_VELOCITY
    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        if snake.velocity == UP_VELOCITY or snake.velocity == DOWN_VELOCITY:
            snake.velocity = RIGHT_VELOCITY

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

snake = snake.Snake(velocity=LEFT_VELOCITY)
food = food.Food(snake.body)
clock = pygame.time.Clock()

paused = False

running = True


def display_pause_screen():
    snake.draw(screen)
    font = pygame.font.Font(None, 100)
    text = font.render("PAUSED", True, WHITE)
    text_rect = text.get_rect()
    screen.blit(text, ((SCREEN_WIDTH - text_rect.width) // 2, (SCREEN_HEIGHT - text_rect.height) // 2))


def handle_event():
    global running, paused
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            paused = not paused
        if not paused:
            snake_control()


while running:
    # Check for event
    for event in pygame.event.get():
        handle_event()

    # Draw screen
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.line(screen, WHITE, LINE_START, LINE_END, LINE_WIDTH)

    # Draw snake
    if not paused:
        if snake.body[0].topleft == food.rect.topleft:
            snake.grow_snake()
            food.position = food.reset_position(snake.body)
        snake.move()
        snake.draw(screen)
    else:
        display_pause_screen()

    food.draw(screen)
    #Update screen
    pygame.display.flip()

    clock.tick(10) # 10 FPS

pygame.quit()