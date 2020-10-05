import pygame as pg
import numpy as np
import random

BG_WHITE = (200, 200, 200)
BORDER_BLACK = (0, 0, 0)
FOOD = (10, 255, 10)
SNAKE_HEAD = (255, 10, 10)
SNAKE_BODY = (150, 10, 150)
SCORE_MULTIPLIER = 1
BLOCK_SIZE = 10
HEIGHT = 300
WIDTH = 400
TARGET_FPS = 10
DIMS = (WIDTH, HEIGHT)
IN_WIDTH = WIDTH - 2*BLOCK_SIZE
IN_HEIGHT = HEIGHT - 2*BLOCK_SIZE

NOT_ALLOWED_MOVES = {
    pg.K_DOWN: pg.K_UP,
    pg.K_UP: pg.K_DOWN,
    pg.K_RIGHT: pg.K_LEFT,
    pg.K_LEFT: pg.K_RIGHT
}

MOVEMENTS = {
    pg.K_DOWN: np.array((0, 1)),
    pg.K_UP: np.array((0, -1)),
    pg.K_RIGHT: np.array((1, 0)),
    pg.K_LEFT: np.array((-1, 0))
}

pg.init()
display = pg.display.set_mode(DIMS)
clock = pg.time.Clock()

pg.display.set_caption("SNEK!")
pg.draw.rect(display, BORDER_BLACK, [0,0,WIDTH,HEIGHT])
pg.draw.rect(display, BG_WHITE, [BLOCK_SIZE,BLOCK_SIZE,IN_WIDTH,IN_HEIGHT])

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None

class LinkedList:
    def __init__(self, start_x, start_y):
        self.head = Node(start_x, start_y)
        self.last = self.head

    def append(self, x, y):
        self.last.next = Node(x, y)
        self.last = self.last.next

class Game:
    def __init__(self):
        self.is_over = False
        self.score = 0

class Snake:
    def __init__(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.body = LinkedList(self.x, self.y)

class Food:
    def __init__(self):
        self.next_food_location()

    def next_food_location(self):
        self.x = int((BLOCK_SIZE + random.random() * IN_WIDTH)/BLOCK_SIZE) * BLOCK_SIZE
        self.y = int((BLOCK_SIZE + random.random() * IN_HEIGHT)/BLOCK_SIZE) * BLOCK_SIZE

        if self.x < BLOCK_SIZE or self.y < BLOCK_SIZE or \
            self.x > IN_WIDTH or self.y > IN_HEIGHT:
            self.next_food_location()

snek = Snake()
food = Food()
game = Game()

def draw_block(color, x, y):
    half_block = int(BLOCK_SIZE / 2)
    pg.draw.rect(display, color, [x, y, BLOCK_SIZE, BLOCK_SIZE])

def draw_snake():
    current = snek.body.head
    draw_block(SNAKE_HEAD, current.x, current.y)

    while current.next != None:
        current = current.next
        draw_block(SNAKE_BODY, current.x, current.y)

def erase_snake():
    draw_block(BG_WHITE, snek.body.last.x, snek.body.last.y)

def draw_food():
    draw_block(FOOD, food.x, food.y)

def game_loop():
    draw_snake()
    draw_food()
    pg.display.update()
    clock.tick(TARGET_FPS)

def colision_check():
    if snek.x < BLOCK_SIZE or snek.y < BLOCK_SIZE or \
        snek.x > IN_WIDTH or snek.y > IN_HEIGHT:
        game.is_over = True
        return

    head = snek.body.head
    current = head.next
    while current != None:
        if head.x == current.x and head.y == current.y:
            game.is_over = True
            return
        current = current.next

    if snek.x == food.x and snek.y == food.y:
        snek.body.append(snek.x, snek.y)
        game.score += SCORE_MULTIPLIER
        food.next_food_location()

current_move = 0

def update_snake_position():
    current = snek.body.head
    current_x = current.x
    current_y = current.y
    (current.x, current.y) = (current.x, current.y) + MOVEMENTS[current_move] * BLOCK_SIZE
    (snek.x, snek.y) = (current.x, current.y)
    while current.next != None:
        tmp_x = current.next.x
        tmp_y = current.next.y
        current.next.x = current_x
        current.next.y = current_y
        current_x = tmp_x
        current_y = tmp_y
        current = current.next

while not game.is_over:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key in MOVEMENTS:
            if current_move in NOT_ALLOWED_MOVES:
                if event.key != NOT_ALLOWED_MOVES[current_move]:
                    current_move = event.key
            else:
                current_move = event.key
            break

    if current_move in MOVEMENTS:
        erase_snake()
        update_snake_position()
        colision_check()

    game_loop()

print("Game Over! Final Score: {}".format(game.score))
pg.quit()