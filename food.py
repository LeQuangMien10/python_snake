import pygame
import random
from config import *

class Food:
    def __init__(self, snake_body, width=FOOD_SIZE, height=FOOD_SIZE, color=FOOD_COLOR):
        self.color = color
        self.position = self.random_position(snake_body)
        self.rect = pygame.Rect(self.position[0], self.position[1], width, height)

    def random_position(self, snake_body):
        all_positions = {
            (x, y)
            for x in range(0, SCREEN_WIDTH, GRID_SIZE)
            for y in range(LINE_START[1], SCREEN_HEIGHT, GRID_SIZE)
        }

        available_positions = list(all_positions - {(rect.x, rect.y) for rect in snake_body})

        if available_positions:
            self.position = random.choice(available_positions)

        # print(self.position)
        return self.position[0], self.position[1]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def reset_position(self, snake_body):
        self.position = self.random_position(snake_body)
        self.rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)

