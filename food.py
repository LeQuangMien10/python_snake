import pygame
import random
from config import *

class Food:
    def __init__(self, width=FOOD_SIZE, height=FOOD_SIZE, color=FOOD_COLOR):
        self.color = color
        self.position = self.random_position()
        self.rect = pygame.Rect(self.position[0], self.position[1], width, height)

    def random_position(self):
        x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(LINE_START[1] // GRID_SIZE, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        print(x, y)
        return x, y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def reset_position(self):
        self.position = self.random_position()
        self.rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)

