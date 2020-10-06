import pygame as pg

BG_WHITE = (200, 200, 200)
BORDER_BLACK = (0, 0, 0)
FOOD = (10, 255, 10)
SNAKE_HEAD = (255, 10, 10)
SNAKE_BODY = (150, 10, 150)
TARGET_FPS = 5

class PygameSnakeDrawer:
    def __init__(self, width, height, block_size):
        self.pg = pg
        self.pg.init()
        self.width = width
        self.height = height
        self.block_size = block_size
        self.inner_width = width - 2*block_size
        self.inner_height = height - 2*block_size
        self.display = self.pg.display.set_mode((width, height))
        self.clock = self.pg.time.Clock()

        self.pg.display.set_caption("SNEK!")
        self.pg.draw.rect(self.display, BORDER_BLACK, [0, 0, self.width, self.height])
        self.pg.draw.rect(self.display, BG_WHITE, [self.block_size, self.block_size, self.inner_width, self.inner_height])

    def draw_block(self, color, x, y):
        half_block = int(self.block_size / 2)
        self.pg.draw.rect(self.display, color, [x, y, self.block_size, self.block_size])

    def draw_snake(self, snek):
        current = snek.body.head
        self.draw_block(SNAKE_HEAD, current.x * self.block_size, current.y * self.block_size)

        while current.next != None:
            current = current.next
            self.draw_block(SNAKE_BODY, current.x * self.block_size, current.y * self.block_size)

    def erase_snake(self, snek):
        self.draw_block(BG_WHITE, snek.body.last.x * self.block_size, snek.body.last.y * self.block_size)

    def draw_food(self, food):
        self.draw_block(FOOD, food.x * self.block_size, food.y * self.block_size)

    def update_screen(self):
        self.pg.display.update()

    def frame_loop(self, snake, food):
        self.draw_snake(snake)
        self.draw_food(food)
        self.update_screen()
        self.clock.tick(TARGET_FPS)

    def clean(self):
        self.pg.quit()