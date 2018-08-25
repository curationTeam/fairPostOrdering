import random
from simulation import Simulation

def main():

  seed = random.randint(0, 1000)
  # Simulation(rounds, noProfiles, a, b, regen_time, att_span)
  sim = Simulation(201600, (15, 0, 10), 1/200, 1, 6.94*10-6, 10)
  players, posts = sim.init_setup(seed)
  players, posts = sim.execute(players, posts)
  t_similar, spearman, kendall_tau = sim.results(posts)


if __name__== "__main__":
  main()