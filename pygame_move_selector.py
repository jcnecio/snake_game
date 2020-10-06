import pygame as pg

PG_MAPPING = {
    pg.K_DOWN: 0,
    pg.K_UP: 1,
    pg.K_RIGHT: 2,
    pg.K_LEFT: 3
}

NOT_ALLOWED_MOVES = {
    0: pg.K_UP,
    1: pg.K_DOWN,
    2: pg.K_LEFT,
    3: pg.K_RIGHT
}

class PygameMoveSelector:    
    def get_move(self, last_move, sight):
        current_move = last_move
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key in PG_MAPPING:
                if last_move in NOT_ALLOWED_MOVES:
                    if event.key != NOT_ALLOWED_MOVES[last_move]:
                        current_move = PG_MAPPING[event.key]
                else:
                    current_move = PG_MAPPING[event.key]
                break
        return current_move