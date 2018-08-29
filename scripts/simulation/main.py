import random
from simulation import Simulation

sp = (1,) * (100+10)
noProfiles = (100, 0, 10)
a = 1/200
b = 0.01
regen_time = 3 / (5*24*60*60)
att_span = 5

def main():
    seed = random.randint(0, 1000)
    t_similar_list = []
    rounds = []

    for i in range(1,1000,100):
        # Simulation(rounds, noProfiles, a, b, regen_time, att_span)
        sim = Simulation(sp, i, noProfiles, a, b, regen_time, att_span)
        players, posts = sim.init_setup(seed)
        players, posts = sim.execute(players, posts)
        t_similar, spearman, kendall_tau = sim.results(posts)

        rounds.append(i)
        t_similar_list.append(t_similar)

    sim.plot(rounds, t_similar_list)

if __name__== "__main__":
    main()
