import pygame
from config import *
import snake
import food
import json
import datetime

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Menu Variables
title_font = pygame.font.SysFont("comicsans", 80)
menu_font = pygame.font.SysFont("comicsans", 20)
menu_selected_font = pygame.font.SysFont("comicsans", 40)
options = ["CONTINUE", "NEW GAME", "HIGH SCORES", "QUIT"]
selected = 0

# Game variables
game_loop = False
snake_instance = snake.Snake(velocity=LEFT_VELOCITY)
food_instance = food.Food(snake_instance.body)
clock = pygame.time.Clock()
score = 0
level = DEFAULT_LEVEL
fps = float(2.5 * level + 2.5)
paused = False
game_over = False
main_loop = True

# High score variables
high_score_loop = False


# Initialize menu screen
def initialize_menu_screen():
    screen.fill(BACKGROUND_COLOR)
    title = title_font.render("SNAKE GAME", True, WHITE)
    screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 50))
    for i, option in enumerate(options):
        color = WHITE if i != selected else YELLOW
        menu_text = menu_font.render(
            option, True, color) if i != selected else menu_selected_font.render(option, True, color)
        screen.blit(menu_text, (10, 250 + 50 * i))
    pygame.display.flip()


# Handle Menu Event
def handle_menu_event():
    global event, main_loop, selected, paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_loop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected = (selected + 1) % len(options)
            elif event.key == pygame.K_UP:
                selected = (selected - 1) % len(options)
            elif event.key == pygame.K_RETURN:
                if selected == CONTINUE:
                    do_game_loop()
                elif selected == NEW_GAME:
                    do_game_loop()
                elif selected == HIGH_SCORE:
                    do_high_score_loop()
                elif selected == QUIT:
                    main_loop = False


# Control snake with keyboard.
def snake_control():
    global snake_instance
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
    global snake_instance, food_instance, game_over, score, fps, paused
    snake_instance = snake.Snake(velocity=LEFT_VELOCITY)
    food_instance = food.Food(snake_instance.body)
    game_over = False
    score = 0
    fps = float(2.5 * level + 2.5)
    if paused:
        paused = False


# Draw dynamic components (snake, food, score)
def draw_dynamic_components():
    snake_instance.draw(screen)
    food_instance.draw(screen)
    draw_game_score()


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
def handle_game_event():
    global main_loop, paused, game_over, game_loop
    if event.type == pygame.QUIT:
        game_loop = False
        main_loop = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game_loop = False
        elif event.key == pygame.K_p and not game_over:
            paused = not paused
        elif event.key == pygame.K_r:
            reset_game()
        if not paused:
            snake_control()


# Draw static components in game
def draw_game_screen():
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


# Display score
def draw_game_score():
    font = pygame.font.Font(None, 50)
    score_text = font.render("Score: " + str(score), True, WHITE)
    score_text_rect = score_text.get_rect()
    screen.blit(score_text, (10, 10))


# Handle snake eats food
def handle_snake_eats_food():
    global score, fps
    if snake_instance.body[0].topleft == food_instance.rect.topleft:
        score += level
        fps = float(fps + 25 / 10000 * fps)
        snake_instance.grow_snake()
        food_instance.position = food_instance.reset_position(snake_instance.body)


# Check for game over
def check_for_game_over():
    global game_over
    if not game_over:
        if snake_instance.check_self_collision():
            game_over = True
            update_high_scores()
            # print("Game Over")

def save_game_state():
    game_data = {
        "snake_body": [(rect.x, rect.y) for rect in snake_instance.body],
        "snake_length": len(snake_instance.body),
        "snake_velocity": snake_instance.velocity,
        "food_position": food_instance.position,
        "score": score,
    }

    with open(SAVE_FILE, "w") as file:
        json.dump(game_data, file, indent=4)


def load_game_state():
    try:
        with open(SAVE_FILE, "r") as file:
            game_data = json.load(file)
            return game_data
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def check_for_saved_game():
    global score, paused, snake_instance, food_instance
    game_data = load_game_state()
    if game_data:
        snake_instance.body = [pygame.Rect(x, y, BODY_SIZE, BODY_SIZE) for x, y in game_data["snake_body"]]
        snake_instance.colors = [HEAD_COLOR] + [BODY_COLOR] * (len(snake_instance.body) - 2) + [TAIL_COLOR]
        snake_instance.length = game_data["snake_length"]
        snake_instance.velocity = tuple(game_data["snake_velocity"])
        food_instance.position = tuple(game_data["food_position"])
        food_instance.rect = pygame.Rect(food_instance.position[0], food_instance.position[1], FOOD_SIZE, FOOD_SIZE)
        score = game_data["score"]
        paused = True

# Game loop
def do_game_loop():
    if selected == NEW_GAME:
        reset_game()
    else:
        check_for_saved_game()
    global event, game_loop
    game_loop = True
    while game_loop:
        for event in pygame.event.get():
            handle_game_event()
        # Draw screen
        draw_game_screen()
        display_game()
        check_for_game_over()
        # Update screen
        pygame.display.flip()
        clock.tick(fps)
    save_game_state()


# Load data from json file to an array
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Save new high scores into high_scores.json
def save_high_scores(scores):
    with open(HIGH_SCORE_FILE, "w") as file:
        json.dump(scores, file, indent=4)


# Update high scores
def update_high_scores():
    scores = load_high_score()
    today = datetime.date.today().strftime("%d-%m-%Y")
    scores.append({"score": score, "date": today})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]

    save_high_scores(scores)


# High score menu loop
def do_high_score_loop():
    global event, main_loop, high_score_loop
    high_score_loop = True
    while high_score_loop:
        for event in pygame.event.get():
            handle_high_score_event()

        draw_high_scores()


# Display high scores
def draw_high_scores():
    screen.fill(BACKGROUND_COLOR)
    scores = load_high_score()
    y_offset = 50
    for i, entry in enumerate(scores):
        score_text = menu_font.render(f"{i + 1}. {entry['score']} - {entry['date']}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 40
    pygame.display.flip()


# Handle high score menu event
def handle_high_score_event():
    global high_score_loop, main_loop
    if event.type == pygame.QUIT:
        high_score_loop = False
        main_loop = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            high_score_loop = False


# Main loop
while main_loop:
    initialize_menu_screen()
    handle_menu_event()

if game_over:
    reset_game()
save_game_state()
pygame.quit()
exit()
