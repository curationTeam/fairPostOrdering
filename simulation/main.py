import random
from simulation import Simulation
import matplotlib.pyplot as plt

noProfiles = (9, 1, 20)
sp = (1,) * sum(noProfiles)
a = 1/200
b = 0.1
regen_time = 3 / (5*24*60) # as in Steem
att_span = 10
noRound = 200000
choice = 1 # 0 for uniform, 1 for beta

def plot(x, y, kind):
    plt.plot(x, y)
    plt.xlabel("Rounds")
    plt.ylabel(kind)
    name = "figures/" + str(x[-1]) + "_" + kind + ".png"
    plt.savefig(name)
    plt.show()

def all_votes_submitted(not_selfish_player_no, posts):
    for post in posts:
        if len(post.voters) < not_selfish_player_no:
            return False
    return True

def append_results(rounds, i, t_similar_list, t_similar, spearman_list,
                   spearman, kendall_tau_list, kendall_tau):
    rounds.append(i)
    t_similar_list.append(t_similar)
    spearman_list.append(spearman)
    kendall_tau_list.append(kendall_tau)

def get_random_likabilities(choice):
    profile_indexes = range(0, sum(noProfiles))
    post_indexes = range(0, noProfiles[0] + bool(noProfiles[1]))
    if choice:
        likabilities =  [[random.betavariate(
                (i+j+2)/(noRound/500),
                (i*i+2*j*j*j/3+1)/(noRound/5))
            for i in profile_indexes] for j in post_indexes]
    else:
        likabilities = [[random.uniform(0, 1)
            for i in profile_indexes] for j in post_indexes]
    if noProfiles[1] > 0: # handicap selfish post
        for i in range(0, sum(noProfiles)):
            likabilities[-1][i] = max(0, likabilities[-1][i] - 0.3)
    return likabilities

def position_of_post(author_id, posts):
    for i in range(0, len(posts)):
        if posts[i].author_id == author_id:
            return i

def real_position_of_post(author_id, sim):
    return position_of_post(author_id, sim.posts)

def ideal_position_of_post(author_id, sim):
    ideal_posts = sim.sort_by_ideal_score(sim.posts)
    return position_of_post(author_id, ideal_posts)

def main():
    seed = random.randint(0, 1000)
    t_similar_list = []
    spearman_list = []
    kendall_tau_list = []
    rounds = []
    lik_mat = get_random_likabilities(choice)

    sim = Simulation(sp, noRound, noProfiles, a, b, regen_time, att_span, lik_mat, seed)
    gen = sim.execute()
    for i in range(0, noRound):
        players, posts = next(gen)
        t_similar, spearman, kendall_tau = sim.stats()

        append_results(rounds, i, t_similar_list, t_similar, spearman_list,
                       spearman, kendall_tau_list, kendall_tau)
        not_selfish_player_no = noProfiles[0] + noProfiles[2]
        # next rounds will be the same
        if all_votes_submitted(not_selfish_player_no, posts):
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

    if noProfiles[1] > 0: # if there exist selfish players
        ideal_pos = ideal_position_of_post(noProfiles[0], sim)
        real_pos = real_position_of_post(noProfiles[0], sim)
        print("Ideal position of selfish post:", ideal_pos)
        print("Real position of selfish post:", real_pos)

if __name__== "__main__":
    main()
