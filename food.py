import pygame
import random
from config import *


class Food:
    def __init__(self, snake_body, width=FOOD_SIZE, height=FOOD_SIZE, color=FOOD_COLOR[0]):
        self.current_color = color
        self.width = width
        self.height = height
        self.position = self.random_position(snake_body)
        self.rect = pygame.Rect(self.position[0], self.position[1], width, height)
        self.last_blink_time = pygame.time.get_ticks()

    def random_position(self, snake_body):
        all_positions = {
            (x, y)
            for x in range(0, SCREEN_WIDTH, GRID_SIZE)
            for y in range(LINE_START[1], SCREEN_HEIGHT, GRID_SIZE)
        }

        available_positions = list(all_positions - {(rect.x, rect.y) for rect in snake_body})

        if available_positions:
            return random.choice(available_positions)
        return 0, LINE_START[1]

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)

    def reset_position(self, snake_body):
        new_position = self.random_position(snake_body)
        self.position = new_position
        self.rect = pygame.Rect(new_position[0], new_position[1], self.width, self.height)
        return new_position

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_blink_time > BLINK_TIME:
            self.current_color = FOOD_COLOR[1] if self.current_color == FOOD_COLOR[0] else FOOD_COLOR[0]
            self.last_blink_time = current_time
