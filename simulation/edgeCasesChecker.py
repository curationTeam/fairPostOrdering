import random
from simulation import Simulation
import matplotlib.pyplot as plt

seed = random.randint(0, 1000)

sim = Simulation((1,1,0), 4, (3,0,0), 0.5, 0.5, 0.5, 3, [[1, 0.8, 0], [1, 0.8, 0], [0.9, 1, 0]])
players, posts = sim.init_setup(seed)
gen = sim.execute(players, posts)

for _i in range(0, 4):
    players, posts = next(gen)
    print(posts)
