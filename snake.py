import pygame as pg
import math
import numpy as np
import random

from null_drawer import NullDrawer
from random_move_selector import RandomMoveSelector
from pygame_drawer import PygameSnakeDrawer
from pygame_move_selector import PygameMoveSelector

MOVEMENTS = {
    0: np.array((0, 1)),
    1: np.array((0, -1)),
    2: np.array((1, 0)),
    3: np.array((-1, 0))
}

SCORE_MULTIPLIER = 1
BLOCK_SIZE = 10
HEIGHT = 300
WIDTH = 400
DIMS = (WIDTH, HEIGHT)
IN_WIDTH = WIDTH - 2*BLOCK_SIZE
IN_HEIGHT = HEIGHT - 2*BLOCK_SIZE

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
    def __init__(self, snake, food, move_selector, graphics):
        self.is_over = False
        self.score = 0
        self.snek = snake
        self.food = food
        self.move_selector = move_selector
        self.graphics = graphics
    
    def colision_check(self):
        if self.snek.x < 1 or self.snek.y < 1 or \
            self.snek.x > IN_WIDTH/BLOCK_SIZE or self.snek.y > IN_HEIGHT/BLOCK_SIZE:
            self.is_over = True
            return

        head = self.snek.body.head
        current = head.next
        while current != None:
            if head.x == current.x and head.y == current.y:
                self.is_over = True
                return
            current = current.next

        if self.snek.x == self.food.x and self.snek.y == self.food.y:
            self.snek.body.append(self.snek.x, self.snek.y)
            self.score += SCORE_MULTIPLIER
            self.food.next_food_location()

    def update_snake_position(self, move):
        current = self.snek.body.head
        current_x = current.x
        current_y = current.y
        (current.x, current.y) = (current.x, current.y) + MOVEMENTS[move]
        (self.snek.x, self.snek.y) = (current.x, current.y)
        while current.next != None:
            tmp_x = current.next.x
            tmp_y = current.next.y
            current.next.x = current_x
            current.next.y = current_y
            current_x = tmp_x
            current_y = tmp_y
            current = current.next
    
    def get_snake_vision(self):
        sight = [0, 0, 0, 0, 0, 0]
        if self.snek.y - 1 < 1:
            sight[0] = 1
        if self.snek.y + 1 > IN_HEIGHT/BLOCK_SIZE:
            sight[1] = 1
        if self.snek.x - 1 < 1:
            sight[2] = 1
        if self.snek.x + 1 > IN_WIDTH/BLOCK_SIZE:
            sight[3] = 1
        
        head = self.snek.body.head
        current = head.next
        while current != None:
            if head.x == current.x and head.y-1 == current.y:
                sight[0] = 1
            if head.x == current.x and head.y+1 == current.y:
                sight[1] = 1
            if head.x-1 == current.x and head.y == current.y:
                sight[2] = 1
            if head.x+1 == current.x and head.y == current.y:
                sight[3] = 1
            if sight[:4] == [1,1,1,1]:
                break
            current = current.next

        x = self.snek.x - self.food.x
        y = self.snek.y - self.food.y
        sight[4] = math.sin(math.atan2(y, x))
        if abs(sight[4]) < 1e-10:
            sight[4] = 0.0
        sight[5] = math.sin(math.atan2(x, y))
        if (sight[5]) < 1e-10:
            sight[5] = 0.0
    
        return sight

    def start(self):
        current_move = -1
        while not self.is_over:
            current_move = self.move_selector.get_move(current_move, self.get_snake_vision())

            if current_move in MOVEMENTS:
                self.graphics.erase_snake(self.snek)
                self.update_snake_position(current_move)
                self.colision_check()

            self.graphics.frame_loop(self.snek, self.food)

    def quit(self):
        self.graphics.clean()

class Snake:
    def __init__(self):
        self.x = (WIDTH/BLOCK_SIZE)/2
        self.y = (HEIGHT/BLOCK_SIZE)/2
        self.body = LinkedList(self.x, self.y)

class Food:
    def __init__(self):
        self.next_food_location()

    def next_food_location(self):
        self.x = int((1 + random.random() * IN_WIDTH)/BLOCK_SIZE)
        self.y = int((1 + random.random() * IN_HEIGHT)/BLOCK_SIZE)

        if self.x < BLOCK_SIZE or self.y < BLOCK_SIZE or \
            self.x > IN_WIDTH or self.y > IN_HEIGHT:
            self.next_food_location()

# graphics = NullDrawer()
# move_selector = RandomMoveSelector()
graphics = PygameSnakeDrawer(WIDTH, HEIGHT, BLOCK_SIZE)
move_selector = PygameMoveSelector()

game = Game(Snake(), Food(), move_selector, graphics)
game.start()
print("Game Over! Final Score: {}".format(game.score))
game.quit()