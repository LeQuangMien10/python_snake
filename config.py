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
DEFAULT_LENGTH = 3

UP_VELOCITY = (0, -20)
DOWN_VELOCITY = (0, 20)
LEFT_VELOCITY = (-20, 0)
RIGHT_VELOCITY = (20, 0)

# Food
FOOD_SIZE =  GRID_SIZE
FOOD_COLOR = [GREEN, YELLOW]
BLINK_TIME = 500