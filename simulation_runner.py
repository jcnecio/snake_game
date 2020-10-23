import os
import random
import time
import numpy as np

from snake import *

from null_drawer import NullDrawer
from parameter_move_selector import ParameterMoveSelector
from pygame_drawer import PygameSnakeDrawer
from pygame_move_selector import PygameMoveSelector

from multiprocessing import Pool

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

class HookedGame(Game):
    def __init__(self, move_selector, graphics):
        super().__init__(move_selector, graphics)
        self.last_eaten = 100
        self.fitness = 0

    def loop(self, last_move):
        initial_size = self.snek.body.size
        new_move = super().loop(last_move)
        new_size = self.snek.body.size

        if new_size > initial_size:
            self.last_eaten = 500
            self.fitness += 1
        else:
            self.last_eaten -= 1
        
        if self.last_eaten == 0:
            self.is_over = True

        return new_move

class Simulator:
    def __init__(self, graphics):
        self.mutation_rate = 0.05
        self.mutation_value = 1
        self.graphics = graphics

    def try_random_mutation(self, chromosome):
        for i,v in enumerate(chromosome):
            chance = random.random()
            if chance < self.mutation_rate:
                value = (random.random() * self.mutation_value) - self.mutation_value
                chromosome[i] += value
        return chromosome

    def cross_breed(self, parent_a, parent_b):
        child_a = ParameterMoveSelector()
        child_b = ParameterMoveSelector()

        chrom_a = parent_a.hidden_layer.flatten()
        chrom_b = parent_b.hidden_layer.flatten()
        full = chrom_a.shape[0]
        half = int(full/2)
        child_a_h = self.try_random_mutation(np.append(chrom_a[0:half], chrom_b[half:full]))
        child_b_h = self.try_random_mutation(np.append(chrom_b[0:half], chrom_a[half:full]))

        child_a.hidden_layer = np.reshape(child_a_h, child_a.hidden_layer.shape)
        child_b.hidden_layer = np.reshape(child_b_h, child_b.hidden_layer.shape)

        chrom_a = parent_a.output_layer.flatten()
        chrom_b = parent_b.output_layer.flatten()
        full = chrom_a.shape[0]
        half = int(full/2)
        child_a_o = self.try_random_mutation(np.append(chrom_a[0:half], chrom_b[half:full]))
        child_b_o = self.try_random_mutation(np.append(chrom_b[0:half], chrom_a[half:full]))
        
        child_a.output_layer = np.reshape(child_a_o, child_a.output_layer.shape)
        child_b.output_layer = np.reshape(child_b_o, child_b.output_layer.shape)

        return child_a, child_b

    def generate_offsprings(self, num_candidates, generation_count):
        parent_generation = generation_count - 1
        candidates = []
        pick_rate = []
        new_generation = []
        for i in range(num_candidates):
            path = 'models/gen{}/{}.npz'.format(parent_generation, i)
            prev_gen = ParameterMoveSelector(file_path=path)
            candidates.append(prev_gen)
            pick_rate.append(prev_gen.last_fitness)
        
        pick_rate = softmax(np.array(pick_rate))

        half_count = int(num_candidates/2)
        parents = random.choices(candidates, weights=pick_rate, k=half_count)
        for i in range(half_count):
            child_a, child_b = self.cross_breed(parents[i], parents[(i+1)%half_count])
            new_generation.append(child_a)
            new_generation.append(child_b)
        
        if len(new_generation) < num_candidates: # if candidate count is odd
            prodigy, ignored = self.cross_breed(parents[0], parents[1]) # first and second place child
            new_generation.append(prodigy)

        return new_generation

    def run_agent(self, args):
        index, agent = args
        game = HookedGame(agent, self.graphics)
        game.start()
        agent.last_fitness = game.fitness
        game.quit()
        return index, game.fitness

    def simulate(self, num_candidates=100, generation_count=0):
        start = time.time()
        if generation_count != 0:
            agents = self.generate_offsprings(num_candidates, generation_count)
        else:
            agents = [ParameterMoveSelector() for i in range(num_candidates)]

        with Pool() as pool:
            results = pool.map_async(self.run_agent, enumerate(agents)).get()
        for result in results:
            i, fitness = result 
            agents[i].last_fitness = fitness

        agents.sort(key=lambda agent: agent.last_fitness, reverse=True)
        if not os.path.exists('models/gen{}'.format(generation_count)):
            os.makedirs('models/gen{}'.format(generation_count))
        for i, agent in enumerate(agents):
            agent.save('models/gen{}/{}'.format(generation_count, i))
        print('Average fitness: {}, Top Agent: {}'.format(np.mean([int(i.last_fitness) for i in agents[:int(num_candidates*0.1)]]), agents[0].last_fitness))
        return (time.time() - start)*1000
        

# graphics = PygameSnakeDrawer(WIDTH, HEIGHT, BLOCK_SIZE)
# move_selector = ParameterMoveSelector(file_path='models/gen99/0.npz')
# print(move_selector.hidden_layer)
# game = HookedGame(move_selector, graphics)
# game.start()
# game.quit()

random.seed(1337)
num_generations = 100
player_size = 500
graphics = NullDrawer()
simulator = Simulator(graphics)

for i in range(num_generations):
    time_taken = simulator.simulate(num_candidates=player_size, generation_count=i)
    print('Done with generation {}: took {}ms'.format(i, time_taken))