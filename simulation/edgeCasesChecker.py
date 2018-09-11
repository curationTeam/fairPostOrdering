import random
from simulation import Simulation
import matplotlib.pyplot as plt

seed = random.randint(0, 1000)

noPlayer = 341
rounds = 523
sim = Simulation((1,) * noPlayer, rounds, (noPlayer,0,0), 0.5, 0.5, 0.5, 3)
players, posts = sim.init_setup(seed)
gen = sim.execute(players, posts)

for _i in range(0, rounds):
    players, posts = next(gen)
    print(posts)
