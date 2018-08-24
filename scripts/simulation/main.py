import random
from simulation import Simulation

def main():

  seed = random.randint(0, 1000)
  sim = Simulation(15, (15, 0, 10), 0, 0, 1, 10)
  players, posts = sim.init_setup(seed)
  sim.execute(players, posts)
  sim.t_similarity(posts)


if __name__== "__main__":
  main()