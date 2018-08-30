import random
from simulation import Simulation
import matplotlib.pyplot as plt

noProfiles = (200, 0, 100)
sp = (1,) * sum(noProfiles)
a = 5/200
b = 0.1
regen_time = 3 / (5*24*60) # as in Steem
att_span = 10
noRound = 50000

def plot(x, y, kind):
    plt.plot(x, y)
    plt.xlabel("Rounds")
    plt.ylabel(kind)
    name = "figures/" + str(x[-1]) + "_" + kind + ".png"
    plt.savefig(name)
    plt.show()

def all_votes_submitted(players, posts):
    all_votes = True
    for post in posts:
        if len(post.voters) != len(players): # TODO: incompatible with greedy
            all_votes = False
            break
    return all_votes

def append_results(rounds, i, t_similar_list, t_similar, spearman_list,
                   spearman, kendall_tau_list, kendall_tau):
    rounds.append(i)
    t_similar_list.append(t_similar)
    spearman_list.append(spearman)
    kendall_tau_list.append(kendall_tau)

def main():
    seed = random.randint(0, 1000)
    t_similar_list = []
    spearman_list = []
    kendall_tau_list = []
    rounds = []

    sim = Simulation(sp, noRound, noProfiles, a, b, regen_time, att_span)
    players, posts = sim.init_setup(seed)
    gen = sim.execute(players, posts)
    for i in range(0, noRound):
        players, posts = next(gen)
        t_similar, spearman, kendall_tau = sim.results(posts)

        append_results(rounds, i, t_similar_list, t_similar, spearman_list,
                       spearman, kendall_tau_list, kendall_tau)
        if all_votes_submitted(players, posts): # next simulations will be the same
            for j in range(i, noRound):
                append_results(rounds, j, t_similar_list, t_similar,
                               spearman_list, spearman, kendall_tau_list, kendall_tau)
            break
        if i % 500 == 0:
          print(i, "of", noRound, "done")

    sim.print_result(posts)
    plot(rounds, t_similar_list, "t_similarity")
    plot(rounds, spearman_list, "spearman")
    plot(rounds, kendall_tau_list, "kendall_tau")

if __name__== "__main__":
    main()
