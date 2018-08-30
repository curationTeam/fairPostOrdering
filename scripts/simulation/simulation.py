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

    def __init__(self, spvec, rounds, noProfiles, a, b, regen, att_span):
        self.spvec = spvec
        self.rounds = rounds
        self.profile = ("honest", "greedy", "user")
        self.noProfiles = noProfiles
        self.a = a
        self.b = b
        self.regen = regen
        self.att_span = att_span

        assert type(noProfiles) == tuple
        assert len(noProfiles) == len(self.profile)
        assert len(spvec) == sum(noProfiles)
        assert rounds > 0
        assert att_span > 0
        for noProfile in noProfiles:
            assert type(noProfile) == int
            assert noProfile >= 0

    # Reseed and initialize players and posts
    def init_setup(self, seed):
        random.seed(seed) # reseed the prng
        players = self.init_players()
        posts = self.init_posts(players)

        return players, posts


    # Initialize players
    def init_players(self):
        players = []
        index = 0
        profile_index = 0

        for noProfile in self.noProfiles:
            # Create noProfile players of self.profile[profile_index]
            for _i in range(0, noProfile):
                mean = random.uniform(0, 1)
                std = 0.1
                players.append(Player(index, mean, std, self.profile[profile_index],
                self.spvec[index], self.att_span, self.a, self.b, self.regen))
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

        initial_order_posts = self.display_list(posts)
        #print('Initial order of posts:', initial_order_posts)

        return posts


    def execute(self, players, posts):
        for r in range(0, self.rounds):
            for player in players:
                player.regenerate_vp() # TODO: We have to define "regen" in terms of the rounds
                player.vote(r, self.rounds, posts)

            posts.sort(key = lambda x: x.real_score, reverse = True)
            yield players, posts

    # Return a list with the author_id of the posts
    def display_list(self, posts):
        return [p.author_id for p in posts]

    # Sort lists of posts by ideal score
    def sort_by_ideal_score(self, posts):
        return sorted(posts, key=lambda x: x.ideal_score, reverse = True)

    # Print results of execution
    def print_result(self, posts):
        order_posts = self.display_list(posts)
        quality_sorted = self.display_list(self.sort_by_quality(posts))
        print('Final ranking of posts:', order_posts)
        print('Quality sorted:', quality_sorted)
        print('Spearman:', stats.spearmanr(quality_sorted, order_posts)[0])
        print('KendallTau:', stats.kendalltau(quality_sorted, order_posts)[0])

    # Calculate t-similarity and spearman correlation coefficient
    def results(self, posts):
        t_similar = 0
        order_posts = self.display_list(posts)
        sorted_by_ideal_order = self.display_list(self.sort_by_ideal_score(posts))
        spearman = stats.spearmanr(sorted_by_ideal_order, order_posts)[0]
        kendall_tau = stats.kendalltau(sorted_by_ideal_order, order_posts)[0]

        for i in range(0, len(posts)):
            if order_posts[i] == sorted_by_ideal_order[i]:
                t_similar += 1
            else: break

        return t_similar, spearman, kendall_tau
