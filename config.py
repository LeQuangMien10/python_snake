# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
BACKGROUND_COLOR = BLACK
LINE_START = (0, 100)
LINE_END = (SCREEN_WIDTH, 100)
LINE_WIDTH = 1

# Snake
BODY_SIZE = GRID_SIZE
HEAD_COLOR = RED
BODY_COLOR = WHITE
TAIL_COLOR = WHITE

START_X = SCREEN_WIDTH / 2
START_Y = SCREEN_HEIGHT / 2
SNAKE_DEFAULT_LENGTH = 3

UP_VELOCITY = (0, -20)
DOWN_VELOCITY = (0, 20)
LEFT_VELOCITY = (-20, 0)
RIGHT_VELOCITY = (20, 0)

# Food
FOOD_SIZE = GRID_SIZE
FOOD_COLOR = [GREEN, YELLOW]
BLINK_TIME = 500

# Game
DEFAULT_LEVEL = 5

LEVEL_SPEEDS = {
    1: 5.0,
    2: 8.0,
    3: 12.0,
    4: 16.0,
    5: 20.0,
    6: 25.0,
    7: 30.0,
    8: 40.0
}

# Menu
CONTINUE = 0
NEW_GAME = 1
LEVEL_SELECT = 2
HIGH_SCORE = 3
QUIT = 4
HIGH_SCORE_FILE = "highscores.json"
SAVE_FILE = "game_state.json"
SETTINGS_FILE = "settings.json"

MENU_OPTION_X = 10
