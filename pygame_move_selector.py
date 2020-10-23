import pygame as pg

PG_MAPPING = {
    pg.K_DOWN: 0,
    pg.K_UP: 1,
    pg.K_RIGHT: 2,
    pg.K_LEFT: 3
}

class PygameMoveSelector:    
    def get_move(self, last_move, sight):
        current_move = last_move
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key in PG_MAPPING:
                return PG_MAPPING[event.key]
        return current_move