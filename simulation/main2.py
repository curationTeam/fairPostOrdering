import random
from simulation import Simulation
import matplotlib.pyplot as plt

seed = random.randint(0, 1000)

sim = Simulation((1,1), 3, (2,0,0), 0.02, 0.1, 0.3, 2, [[0.4, 1], [0.5, 0.8]])
players, posts = sim.init_setup(seed)
gen = sim.execute(players, posts)

players, posts = next(gen)
print(posts)
players, posts = next(gen)
print(posts)
