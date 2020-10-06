import random

class RandomMoveSelector:    
    def get_move(self, last_move, sight):
        return random.sample([0,1,2,3], 1)[0]