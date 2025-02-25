import pygame
from config import *

class Snake:
    def __init__(self, velocity, start_x=600, start_y = 400, length=3):
        self.body = [pygame.Rect(start_x + i * BODY_SIZE, start_y, BODY_SIZE, BODY_SIZE)
                     for i in range(length)]
        self.colors = [HEAD_COLOR] + [BODY_COLOR] * (len(self.body) - 2) + [TAIL_COLOR]
        self.velocity = velocity
        self.grow = False

    def draw(self, screen):
        for rect, color in zip(self.body, self.colors):
            pygame.draw.rect(screen, color, rect)

    def move(self):
        head_x, head_y = self.body[0].topleft
        new_x = head_x + self.velocity[0]
        new_y = head_y + self.velocity[1]

        if new_y < LINE_START[1]:
            new_y = SCREEN_HEIGHT - BODY_SIZE
        elif new_y >= SCREEN_HEIGHT:
            new_y = LINE_START[1]

        if new_x < 0:
            new_x = SCREEN_WIDTH - BODY_SIZE
        elif new_x >= SCREEN_WIDTH:
            new_x = 0
        new_head = pygame.Rect(new_x, new_y, BODY_SIZE, BODY_SIZE)


        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            self.colors = [HEAD_COLOR] + [BODY_COLOR] * (len(self.body) - 2) + [TAIL_COLOR]
        # print(self.body)

    def grow_snake(self):
        self.grow = True

