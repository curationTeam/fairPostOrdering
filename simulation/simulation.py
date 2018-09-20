from scipy import stats
import random

from strategy import Strategy
from player import Player
from post import Post

class Simulation:

    '''
    honest and greedy content creators. users only vote and do not create content (and are honest)
    profile = ["honest", "greedy", "user"]
    noProfiles should be a list of integers [3, 4, 5] denoting the number of players per strategy profile


    voting_power usage per vote           -->    VP' = VP - (a*VP*w + b)
    voting_power regeneration per round   -->    VP' = min (VP + regen, 1)
    attention span --> att_span

    In Steem:

    regen -------> the regeneration per round is given by 3 / (5*24*60*60)
    rounds ------> the number of 3 seconds rounds in one weeks is 201600
    a ----------->  1/200
    b ----------->  1
    '''

    def __init__(self, spvec, rounds, noProfiles, a, b, regen, att_span, lik_mat, seed):
        self.profile = ("honest", "greedy", "user")

        assert type(noProfiles) == tuple
        assert len(noProfiles) == len(self.profile)
        assert len(spvec) == sum(noProfiles)
        assert rounds > 0
        assert att_span > 0
        for noProfile in noProfiles:
            assert type(noProfile) == int
            assert noProfile >= 0

        self.spvec = spvec
        self.rounds = rounds
        self.noProfiles = noProfiles
        self.a = a
        self.b = b
        self.regen = regen
        self.att_span = att_span
        self.posts = self.create_posts(lik_mat)
        self.players = self.init_players(len(self.posts))

        random.seed(seed) # reseed the prng

    def create_posts(self, likability_matrix):
        assert len(likability_matrix) == self.noProfiles[0] + self.noProfiles[1]
        for likability in likability_matrix:
          assert len(likability) == sum(self.noProfiles)

        posts = [Post(i, likability_matrix[i])
                 for i in range(0, len(likability_matrix))]
        random.shuffle(posts) # randomize initial order of post ranking
        return posts

    # Initialize players
    def init_players(self, noPosts):
        players = []
        index = 0
        profile_index = 0

        for noProfile in self.noProfiles:
            # Create noProfile players of self.profile[profile_index]
            for _i in range(0, noProfile):
                players.append(Player(index, self.profile[profile_index],
                self.spvec[index], self.att_span, self.a, self.b, self.regen,
                self.rounds, noPosts))
                index += 1
            profile_index += 1
        return players

    # Initialize posts
    def init_posts(self, players):
        posts = []
        players_ids = list(range(0, len(players)))
        for player in players:
            # users do not create posts
            if str(player.strategy) != "user":
                assert (str(player.strategy) == "honest" or str(player.strategy) == "greedy")
                post = player.create_post(player.quality, players_ids)
                posts.append(post)

        return posts


    def execute(self):
        for r in range(0, self.rounds):
            for player in self.players:
                player.regenerate_vp() # TODO: We have to define "regen" in terms of the rounds
                player.vote(r, self.posts)

            self.posts.sort(key = lambda x: x.real_score, reverse = True)
            yield self.players, self.posts

    # Return a list with the author_id of the posts
    def display_list(self, posts):
        return [(p.ideal_score, len(p.voters)) for p in posts]

    def get_names(self, posts):
        return [p.author_id for p in posts]

    # Sort lists of posts by ideal score
    def sort_by_ideal_score(self, posts):
        return sorted(posts, key=lambda x: x.ideal_score, reverse = True)

    def t_similarity(self, ideal_list, real_list):
        assert(len(ideal_list) == len(real_list))
        res = 0
        for i in range(0, len(ideal_list)):
            if ideal_list[i] == real_list[i]:
                res += 1
            else: break
        return res

    # Print results of execution
    def print_result(self, posts):
        order_posts = self.display_list(posts)
        ideal_score_sorted = self.display_list(self.sort_by_ideal_score(posts))
        print('Final ranking of posts:', order_posts)
        print('Quality sorted:', ideal_score_sorted)

        ideal_score_sorted = self.get_names(self.sort_by_ideal_score(posts))
        order_posts = self.get_names(posts)
        print('Spearman:', stats.spearmanr(ideal_score_sorted, order_posts)[0])
        print('KendallTau:', stats.kendalltau(ideal_score_sorted, order_posts)[0])

    # Calculate t-similarity, spearman and kendall-tau correlation coefficient
    def results(self, posts):
        order_posts = self.get_names(posts)
        sorted_by_ideal_order = self.get_names(self.sort_by_ideal_score(posts))
        spearman = stats.spearmanr(sorted_by_ideal_order, order_posts)[0]
        kendall_tau = stats.kendalltau(sorted_by_ideal_order, order_posts)[0]
        t_similar = self.t_similarity(sorted_by_ideal_order, order_posts)

        return t_similar, spearman, kendall_tau
