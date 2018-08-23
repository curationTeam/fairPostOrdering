from scipy import stats
import random

from strategy import Strategy
from player import Player
from post import Post

# honest and greedy content creators. users only vote and do not create content (and are honest)
profile = ["honest", "greedy", "user"]

# noProfiles should be a list of integers [3, 4, 5] denoting the number of players per strategy profile

'''
voting_power usage per vote           -->    VP' = VP - (a*VP*w + b)
voting_power regeneration per round   -->    VP' = min (VP + regen, 1)
attention span --> att_span
'''

def simulation(seed, rounds, noProfiles, a, b, regen, att_span): # TODO: poner nStrategies en tuple
    assert type(noProfiles) == list

    players, posts = init_setup(seed, noProfiles, att_span)

    for _round in range(0, rounds):
        # TODO: no randomizing is necessary with the chosen model
        random.shuffle(players) # randomize voting order in each round

        for player in players:
            player.regenerate_vp(regen) # TODO: We have to define c in terms of the rounds
            post = player.vote(posts)
            #print(post)
            if post != False: #Check if the player actually voted for something
                player, posts = execute_vote(player, post, posts, a, b)

    print_result(posts) #ojo que los ordena por calidad...MIRAR ESTO---------------T0D0

    return posts, players

# Reseed and initialize players and posts
def init_setup(seed, noProfiles, att_span):
    random.seed(seed) # reseed the prng
    players = init_players(noProfiles, att_span)
    posts = init_posts(players)

    return players, posts

# Initialize players
def init_players(noProfiles, att_span):
    players = []
    index = 0
    profile_index = 0

    for noProfile in noProfiles:
        # Create noProfile players of profile_index and profile = ["honest", "greedy", "user"]
        for _i in range(0, noProfile):
            # Add a player (id, quality_range, strategy_profile, sp)
            mean = random.uniform(0, 1)
            std = 0.1
            players.append(Player(index, mean, std, profile[profile_index], 1, att_span))
            index += 1

        profile_index += 1

    return players

# Initialize posts
def init_posts(players):
    posts = []
    players_ids = list(range(0, len(players)))
    for player in players:
        # users do not create posts
        if str(player.strategy) != "user":
            assert (str(player.strategy) == "honest" or str(player.strategy) == "honest")

            post = player.create_post(player.quality, players_ids)
            posts.append(post)

    random.shuffle(posts) # randomize initial order of post ranking
    initial_order_posts = display_list(posts)
    print('Initial order of posts:', initial_order_posts)

    return posts

# TODO: score calculation should happen in the strategy/player method
def execute_vote(player, post, posts, a, b):
    # Calculate vote as the product of player sp, player current vp and likability(weight)
    weight = post.likability[player.id]
    # TODO: isn't it a * player.sp * player.vp * weight + b?
    post.votes_received += player.sp * player.vp * weight
    post.voters.append(player.id)
    player.spend_vp(a, weight, b) # Decrease voting power after vote
    return player, posts

# Return a list with the author_id of the posts
def display_list(posts):
    return [p.author_id for p in posts]

# Getter for the id of the attacker --------WIP
def get_attacker_id(players):
    for player in players:
        if (not player.honest):
            attacker_id = player.id

    return attacker_id

# Calculate the net position difference of the attacker against its expected position ---------WIP
def net_position(players, posts):
    ctr = 0
    attacker_id = get_attacker_id(players)
    for p in posts:
        if p.author_id == attacker_id:
            expected_quality_index = len(posts) - 1 - p.quality
            return ctr - expected_quality_index
        ctr += 1

# Sort lists of posts by quality
def sort_by_quality(posts):
    return sorted(posts, key=lambda x: x.quality, reverse = True)

# Print results of execution
def print_result(posts):
    order_posts = display_list(posts)
    quality_sorted = display_list(sort_by_quality(posts))
    print('Final ranking of posts:', order_posts)
    print('Quality sorted:', quality_sorted)
    print('Spearman:', stats.spearmanr(quality_sorted, order_posts)[0])
    print('KendallTau:', stats.kendalltau(quality_sorted, order_posts)[0])

def main():
  seed = random.randint(0, 1000)
  simulation(seed, 10, [15, 0, 10], 0, 0, 1, 5)

if __name__== "__main__":
  main()
