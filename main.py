import heapq

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
options = ["CONTINUE", "NEW GAME", "SELECT LEVEL", "HIGH SCORES", "QUIT"]
selected = 0

# Game variables
game_loop = False
snake_instance = snake.Snake(velocity=LEFT_VELOCITY)
food_instance = food.Food(snake_instance.body)
clock = pygame.time.Clock()
score = 0
paused = False
game_over = False
main_loop = True

# High score variables
high_score_loop = False

# Level variables
level_loop = False
current_level = DEFAULT_LEVEL
fps = LEVEL_SPEEDS[current_level]
str_fps = str(fps)

#AI Game Loop Variables
ai_game_loop = False


# Initialize menu screen
def initialize_menu_screen():
    screen.fill(BACKGROUND_COLOR)
    title = title_font.render("SNAKE GAME", True, WHITE)
    screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 50))
    for i, option in enumerate(options):
        color = WHITE if i != selected else YELLOW
        menu_text = menu_font.render(
            option, True, color) if i != selected else menu_selected_font.render(option, True, color)
        screen.blit(menu_text, (MENU_OPTION_X, (250 + 50 * i - menu_text.get_height() // 2)))
    pygame.display.flip()


# Handle Menu Event
def handle_menu_event():
    global event, main_loop, selected, paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_settings()
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
                elif selected == LEVEL_SELECT:
                    do_level_menu_loop()
                elif selected == QUIT:
                    save_settings()
                    main_loop = False
            elif event.key == pygame.K_a:
                do_ai_game_loop()


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
    fps = LEVEL_SPEEDS[current_level]
    if paused:
        paused = False
    clear_game_state()


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
    screen.blit(score_text, (10, 10))


# Handle snake eats food
def handle_snake_eats_food():
    global score, fps
    if snake_instance.body[0].topleft == food_instance.rect.topleft:
        score += current_level
        fps = float(fps + 25 / 10000 * fps)
        snake_instance.grow_snake()
        food_instance.position = food_instance.reset_position(snake_instance.body)
        return True
    return False


# Check for game over
def check_for_game_over():
    global game_over
    if not game_over:
        if snake_instance.check_self_collision():
            game_over = True
            update_high_scores()
            # print("Game Over")


# Save game when exit
def save_game_state():
    game_data = {
        "snake_body": [(rect.x, rect.y) for rect in snake_instance.body],
        "snake_length": len(snake_instance.body),
        "snake_velocity": snake_instance.velocity,
        "food_position": food_instance.position,
        "score": score,
        "paused": True
    }

    with open(SAVE_FILE, "w") as file:
        json.dump(game_data, file, indent=4)


# Load game to continue
def load_game_state():
    try:
        with open(SAVE_FILE, "r") as file:
            game_data = json.load(file)
            return game_data
    except (FileNotFoundError, json.JSONDecodeError):
        return None


# Check if there is a saved game
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
        paused = game_data["paused"]


# Clear game_state file
def clear_game_state():
    with open(SAVE_FILE, "w") as file:
        file.write("")


def reset_fps():
    global str_fps
    str_fps = str(LEVEL_SPEEDS[current_level])
    save_settings()


# Game loop
def do_game_loop():
    if selected == NEW_GAME:
        reset_game()
    else:
        check_for_saved_game()
    global event, game_loop, fps, str_fps
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
        str_fps = str(fps)
        # print(current_level, fps, LEVEL_SPEEDS[current_level], str_fps)
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


# Level menu loop
def do_level_menu_loop():
    global current_level, level_loop, main_loop

    title_text = title_font.render("CHOOSE LEVEL", True, WHITE)
    subtitle_text = menu_font.render("Press ESC to go back to main menu", True, WHITE)

    selected_level = current_level
    level_loop = True
    while level_loop:
        selected_level = handle_level_menu_event(selected_level)
        draw_level_menu(selected_level, subtitle_text, title_text)


# Draw level menu
def draw_level_menu(selected_level, subtitle_text, title_text):
    screen.fill(BACKGROUND_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 125))
    for i in range(1, 9):
        color = WHITE if i != selected_level else YELLOW
        level_text = menu_font.render(
            f"Level {i}", True,
            color) if i != selected_level else menu_selected_font.render(
            f"Level {i}", True, color)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2,
                                 150 + i * 40 - level_text.get_height() // 2))
    pygame.display.flip()


# Handle level menu event
def handle_level_menu_event(selected_level):
    global level_loop, main_loop, current_level
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            level_loop = False
            main_loop = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                level_loop = False
            elif e.key == pygame.K_RETURN:
                if current_level != selected_level:
                    current_level = selected_level
                    reset_game()
                    clear_game_state()
                save_settings()
                level_loop = False
            elif e.key == pygame.K_UP or e.key == pygame.K_w:
                selected_level = selected_level - 1 if selected_level > 1 else 8
            elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
                selected_level = selected_level + 1 if selected_level < 8 else 1
    return selected_level


# Save settings
def save_settings():
    print(fps, str_fps)
    settings = {
        "level": current_level,
        "fps": str_fps
    }
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


# Load settings
def load_settings():
    global current_level, fps, str_fps
    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
            current_level = settings.get("level")
            fps = float(settings.get("fps"))
            str_fps = str(fps)
    except (FileNotFoundError, json.JSONDecodeError):
        current_level = DEFAULT_LEVEL
        fps = LEVEL_SPEEDS[current_level]

def astar(start, goal, obstacles):
    def heuristic(s, g):
        return abs(s[0] - g[0]) + abs(s[1] - g[1])
    open_set = [] # Priority queue for f(n)
    heapq.heappush(open_set, (0, start))

    came_from = {} # Dict for saving the path
    g_score = {start: 0} # Cost
    f_score = {start: heuristic(start, goal)} # Manhattan distance

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [UP_VELOCITY, DOWN_VELOCITY, LEFT_VELOCITY, RIGHT_VELOCITY]:
            neighbor = (current[0] + dx, current[1] + dy)

            if neighbor[0] < 0:
                neighbor = (SCREEN_WIDTH - GRID_SIZE, neighbor[1])
            elif neighbor[0] >= SCREEN_WIDTH:
                neighbor = (0, neighbor[1])
            if neighbor[1] < LINE_START[1]:
                neighbor = (neighbor[0], SCREEN_HEIGHT - GRID_SIZE)
            elif neighbor[1] >= SCREEN_HEIGHT:
                neighbor = (neighbor[0], LINE_START[1])

            if neighbor in obstacles:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []

def move_snake_ai(snake, food):
    global score, fps
    head = snake.body[0].topleft
    food_pos = food.rect.topleft

    if head == food_pos:
        score += current_level
        fps = float(fps + 25 / 10000 * fps)
        snake.grow_snake()
        food.position = food.reset_position(snake.body)
        head = snake.body[0].topleft
        food_pos = food.reset_position(snake_instance.body)
    
    obstacles = set(segment.topleft for segment in snake.body[1:])
    
    path = astar(head, food_pos, obstacles)
    
    if path:
        next_pos = path[0]
        dx, dy = next_pos[0] - head[0], next_pos[1] - head[1]
        snake.velocity = (dx, dy)
    else:
        for dx, dy in [UP_VELOCITY, RIGHT_VELOCITY, DOWN_VELOCITY, LEFT_VELOCITY]:
            next_pos = (head[0] + dx, head[1] + dy)
            if next_pos not in obstacles:
                snake.velocity = (dx, dy)
                break

def do_ai_game_loop():
    global event, fps, str_fps, ai_game_loop, main_loop, paused
    ai_game_loop = True
    while ai_game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ai_game_loop = False
                main_loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ai_game_loop = False
                elif event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_p:
                    paused = not paused
        move_snake_ai(snake_instance, food_instance)
        # Draw screen
        draw_game_screen()
        display_game()
        check_for_game_over()
        # Update screen
        pygame.display.flip()
        clock.tick(fps)
        str_fps = str(fps)

load_settings()
# Main loop
while main_loop:
    initialize_menu_screen()
    handle_menu_event()

if game_over:
    reset_fps()
    reset_game()
    clear_game_state()
else:
    save_game_state()

pygame.quit()
exit()
