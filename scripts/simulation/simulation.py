from scipy import stats
import random
import matplotlib.pyplot as plt

from strategy import Strategy
from player import Player
from post import Post

class Simulation:

    '''
    honest and greedy content creators. users only vote and do not create content (and are honest)
    profile = ["honest", "greedy", "user"]
    noProfiles should be a list of integers [3, 4, 5] denoting the number of players per strategy profile


    voting_power usage per vote           -->    VP' = VP - (a*VP*w + b)
    voting_power regeneration per round   -->    VP' = min (VP + regen_time, 1)
    attention span --> att_span

    In Steem:

    regen_time --> the regeneration per round is given by 3/(5*24*60*60) = 6.94*10-6
    rounds ------> the number of 3 seconds rounds in one weeks is 201600
    a ----------->  1/200
    b ----------->  1
    ''' 

    def __init__(self, rounds, noProfiles, a, b, regen_time, att_span):

        self.rounds = rounds
        self.profile = ("honest", "greedy", "user")
        self.noProfiles = noProfiles
        self.a = a
        self.b = b
        self.regen_time = regen_time
        self.att_span = att_span

        assert type(noProfiles) == tuple
        assert len(noProfiles) == len(self.profile)
        assert rounds > 0
        assert att_span > 0
        for noProfile in noProfiles:
            assert type(noProfile) == int
            assert noProfile >= 0

    # Reseed and initialize players and posts
    def init_setup(self,seed):
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
            # Create noProfile players of profile_index and profile = ["honest", "greedy", "user"]
            for _i in range(0, noProfile):
                # Add a player (id, quality_range, strategy_profile, sp)
                mean = random.uniform(0, 1)
                std = 0.1
                players.append(Player(index, mean, std, self.profile[profile_index], 1, self.att_span))
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
                assert (str(player.strategy) == "honest" or str(player.strategy) == "honest")
                post = player.create_post(player.quality, players_ids)
                posts.append(post)

        random.shuffle(posts) # randomize initial order of post ranking
        initial_order_posts = self.display_list(posts)
        print('Initial order of posts:', initial_order_posts)

        return posts


    def execute(self, players, posts):

        for _round in range(0, self.rounds):
            
            for player in players:
                player.regenerate_vp(self.regen_time) # TODO: We have to define "regen" in terms of the rounds
                post = player.vote(posts)
                #print(post)
                if post != False: #Check if the player actually voted for something
                    player, posts = self.execute_vote(player, post, posts)

            posts.sort(key = lambda x: x.votes_received, reverse = True)

        self.print_result(posts) 

        return players, posts

    # TODO: score calculation should happen in the strategy/player method
    def execute_vote(self,player, post, posts):
        # Calculate vote as the product of player sp, player current vp and likability(weight)
        weight = post.likability[player.id]
        post.votes_received += (self.a *  player.vp * weight + self.b) * player.sp
        post.voters.append(player.id)
        player.spend_vp(self.a, weight, self.b) # Decrease voting power after vote
        return player, posts

    # Return a list with the author_id of the posts
    def display_list(self, posts):
        return [p.author_id for p in posts]


    # Sort lists of posts by quality
    def sort_by_quality(self, posts):
        return sorted(posts, key=lambda x: x.quality, reverse = True)

    # Print results of execution
    def print_result(self, posts):
        order_posts = self.display_list(posts)
        quality_sorted = self.display_list(self.sort_by_quality(posts))
        print('Final ranking of posts:', order_posts)
        print('Quality sorted:', quality_sorted)
        print('Spearman:', stats.spearmanr(quality_sorted, order_posts)[0])
        print('KendallTau:', stats.kendalltau(quality_sorted, order_posts)[0])


    #Calculate t-similarity and spearman correlation coefficient
    def results(self, posts):
        t_similar = 0
        order_posts = self.display_list(posts)
        quality_sorted = self.display_list(self.sort_by_quality(posts))
        spearman = stats.spearmanr(quality_sorted, order_posts)[0]
        kendall_tau = stats.kendalltau(quality_sorted, order_posts)[0]

        for i in range(0, len(posts)):
            if order_posts[i] == quality_sorted[i]:
                t_similar += 1
            else: break

        return t_similar, spearman, kendall_tau


    def plot (self, x, y):
        
        plt.plot(x,y)
        plt.xlabel("Rounds")
        plt.ylabel("t-similarity")
        plt.show()
