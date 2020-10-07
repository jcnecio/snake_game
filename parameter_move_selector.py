import numpy as np
import random

class ParameterMoveSelector:
    def __init__(self, file_path=None):
        if file_path == None:
            self.hidden_layer = np.random.uniform(size=(10,8))
            self.output_layer = np.random.uniform(size=(8,4))
            self.last_fitness = -1
        else:
            loaded = np.load(file_path)
            self.hidden_layer = loaded['hidden']
            self.output_layer = loaded['output']
            self.last_fitness = loaded['fitness']

    def get_move(self, last_move, sight):
        direction = np.zeros(4)
        if last_move != -1:
            direction[last_move] = 1
        sight.extend(direction)
        new_sight = np.array(sight)
        new_sight = np.expand_dims(new_sight, axis=0)
        hidden_out = np.dot(new_sight, self.hidden_layer)
        move_probability = np.dot(hidden_out, self.output_layer)
        return np.argmax(move_probability)
    
    def save(self, file_path):
        np.savez(file_path, hidden=self.hidden_layer, output=self.output_layer, fitness=self.last_fitness)