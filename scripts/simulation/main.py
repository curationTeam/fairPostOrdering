import random
from simulation import Simulation

def main():

    seed = random.randint(0, 1000)
    t_similar_list = []
    rounds = []

    for i in range(1,1000,100):
        # Simulation(rounds, noProfiles, a, b, regen_time, att_span)
        sim = Simulation(i, (100, 0, 10), 1/200, 1, 6.94*10-6, 10)
        players, posts = sim.init_setup(seed)
        players, posts = sim.execute(players, posts)
        t_similar, spearman, kendall_tau = sim.results(posts)

        rounds.append(i)
        t_similar_list.append(t_similar)

    sim.plot(rounds, t_similar_list)
    
    
if __name__== "__main__":
  main()