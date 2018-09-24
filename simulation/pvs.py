import random
from simulation import Simulation
from utils import Utils

noProfiles = (80, 0, 200)
sp = (1,) * sum(noProfiles)
a = 1/50
b = 0.0001
regen_time = 3 / (5*24*60*60) # as in Steem
att_span = 10
noRound = 200000
choice = 0 # 0 for uniform, 1 for beta
handicap = 1

class PVS:
    def __init__(self, noProfiles, sp, a, b, regen_time, att_span,
                 noRound, distribution_choice, selfish_handicap):
        self.noProfiles = noProfiles
        self.sp = sp
        self.a = a
        self.b = b
        self.regen_time = regen_time
        self.att_span = att_span
        self.noRound = noRound
        self.distribution_choice = distribution_choice
        self.selfish_handicap = selfish_handicap

    def all_votes_submitted(self, honest_no, not_selfish_no, selfish_no, posts, sim):
        if selfish_no > 0:
            selfish_post_pos = self.real_position_of_post(honest_no, sim)
            for post in posts[:selfish_post_pos]:
                if len(post.voters) != not_selfish_no:
                    return False

            if len(posts[selfish_post_pos].voters) != not_selfish_no + selfish_no:
                return False

            for post in posts[selfish_post_pos + 1:]:
                if len(post.voters) != not_selfish_no:
                    return False
        else:
            for post in posts:
                if len(post.voters) != not_selfish_no:
                    return False

        return True

    def append_results(self, rounds, i, t_similar_list, t_similar, spearman_list,
                       spearman, kendall_tau_list, kendall_tau):
        rounds.append(i)
        t_similar_list.append(t_similar)
        spearman_list.append(spearman)
        kendall_tau_list.append(kendall_tau)

    def get_random_likabilities(self, choice, handicap):
        profile_indexes = range(0, sum(self.noProfiles))
        post_indexes = range(0, self.noProfiles[0] + bool(self.noProfiles[1]))
        if choice:
            likabilities =  [[random.betavariate(
                    (i+j+2)/(self.noRound/500),
                    (i*i+2*j*j*j/3+1)/(self.noRound/5))
                for i in profile_indexes] for j in post_indexes]
        else:
            likabilities = [[random.uniform(0, 1)
                for i in profile_indexes] for j in post_indexes]
        if self.noProfiles[1] > 0: # handicap selfish post
            for i in range(0, sum(self.noProfiles)):
                likabilities[-1][i] = max(0, likabilities[-1][i] - handicap)
        return likabilities

    def position_of_post(self, author_id, posts):
        for i in range(0, len(posts)):
            if posts[i].author_id == author_id:
                return i

    def real_position_of_post(self, author_id, sim):
        return self.position_of_post(author_id, sim.posts)

    def ideal_position_of_post(self, author_id, sim):
        ideal_posts = sim.sort_by_ideal_score(sim.posts)
        return self.position_of_post(author_id, ideal_posts)

    def execute(self, output = False):
        seed = random.randint(0, 1000)
        t_similar_list = []
        spearman_list = []
        kendall_tau_list = []
        rounds = []
        lik_mat = self.get_random_likabilities(self.distribution_choice,
                                               self.selfish_handicap)

        sim = Simulation(self.sp, self.noRound, self.noProfiles, self.a,
                         self.b, self.regen_time, self.att_span, lik_mat, seed)
        gen = sim.execute()
        for i in range(0, self.noRound):
            players, posts = next(gen)
            t_similar, spearman, kendall_tau = sim.stats()

            self.append_results(rounds, i, t_similar_list, t_similar, spearman_list,
                           spearman, kendall_tau_list, kendall_tau)
            not_selfish_no = self.noProfiles[0] + self.noProfiles[2]
            # next rounds will be the same
            if self.all_votes_submitted(self.noProfiles[0], not_selfish_no,
                    self.noProfiles[1], posts, sim):
                for j in range(i, self.noRound):
                    self.append_results(rounds, j, t_similar_list, t_similar,
                                   spearman_list, spearman, kendall_tau_list, kendall_tau)
                break
            if i % 500 == 0:
              print("   ", i, "of", self.noRound, "done")

        ideal_pos = self.ideal_position_of_post(self.noProfiles[0], sim)
        real_pos = self.real_position_of_post(self.noProfiles[0], sim)

        if output:
            sim.print_result(posts)
            Utils.plot_and_save(rounds, t_similar_list, "Rounds", "$t$-similarity")
            Utils.plot_and_save(rounds, spearman_list, "Rounds", "Spearman's Rho")
            Utils.plot_and_save(rounds, kendall_tau_list, "Rounds", "Kendall's Tau")

            if self.noProfiles[1] > 0: # if there exist selfish players
                print("Ideal position of selfish post:", ideal_pos)
                print("Real position of selfish post:", real_pos)


        if self.noProfiles[1] > 0: # if there exist selfish players
            return ideal_pos - real_pos, t_similar_list[-1]

if __name__== "__main__":
    PVS(noProfiles, sp, a, b, regen_time, att_span, noRound,
        choice, handicap).execute(output = True)
