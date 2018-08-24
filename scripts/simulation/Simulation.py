
from scipy import stats
import random

from Strategy import Strategy
from Player import Player
from Post import Post

#honest and greedy content creators. users only vote and do not create content (and are honest)
profile = ["honest","greedy","user"]

#noProfiles should be a list of integers [3,4,5] denoting the number of players per strategy profile

'''
voting_power usage per vote           -->    VP' = VP - (a*VP*w + b)
voting_power regeneration per round   -->    VP' = min (VP + c, 1)
attention span --> d
'''

def simulation(seed,rounds,nStrategies,a,b,c,d): #poner nStrategies en tuple

    assert type(nStrategies) == list

    players,posts = init_setup(seed,nStrategies,d)

    for _round in range(rounds):
        random.shuffle(players) #randomize voting order in each round

        for player in players:

            player = regenerate_vp(player, c)
            post = player.vote(posts)
            #print(post)
            if post != False: #Check if the player actually vote for something
                player,posts = execute_vote(player,post,posts,a,b)

    print_result(posts) #ojo que los ordena por calidad...MIRAR ESTO---------------T0D0

    return posts,players

#Reseed and initialize players and posts
def init_setup(seed, noProfiles,d):
        
    random.seed(seed) #reseed the prng
    players = init_players(noProfiles,d)
    posts = init_posts(players)

    return players,posts
    
#Initialize players
def init_players(noProfiles,d):
    
    players = []
    index = 0
    profile_index = 0


    for noProfile in noProfiles:
        #Create noProfile players of profile_index and profile = ["honest", "greedy", "user"]
        for _i in range(0, noProfile):
            #Add a player (id,quality_range,strategy_profile,sp)
            players.append(Player(index,random.uniform(0,1),0.1,profile[profile_index],1,d))
            index += 1

        profile_index += 1

    return players

#Initialize posts
def init_posts(players):
    posts = []
    players_ids = list(range(len(players)))
    for player in players:

        #users do not create posts
        if str(player.strategy) != "user":

            assert (str(player.strategy) == "honest" or str(player.strategy) == "honest")

            post = player.create_post(player.quality, players_ids)
            posts.append(post)
        
    random.shuffle(posts) #randomize initial order of post ranking
    initial_order_posts = display_list(posts)
    print('Initial order of posts:', initial_order_posts)

    return posts

def execute_vote(player,post,posts,a,b):

    #Calculate vote as the product of player sp, player current vp and likability(weight)
    weight = post.likability[player.id]
    post.votes_received += player.sp * player.vp * weight
    post.voters.append(player.id)
    player = recalculate_vp(player,a,b) #Decrease voting power after vote
    posts.sort(key=lambda x: x.votes_received, reverse = True) #order post ranking by votes received
    return player,posts

def recalculate_vp(player,a,b):
    
    player.vp = player.vp - (a * player.vp * 1 + b)

    if player.vp < 0:
        player.vp = 0

    return player

def regenerate_vp(player,c):

    player.vp = min(player.vp + c, 1) #We have to define c in terms of the rounds

    return player

# Get the number of players in the simulation (as a sum of the number of players of each profile)
def get_number_players(noProfiles):

    ctr = 0
    for profile in noProfiles:
        ctr += profile

    return ctr

# Return a list with the author_id of the posts
def display_list(posts):
    posts_ranking = []
    for p in posts:
        posts_ranking.append(p.author_id)
    return posts_ranking

# Getter for the id of the attacker --------WIP
def get_attacker_id(players):
    for player in players:
        if (not player.honest):
            attacker_id = player.id

    return attacker_id

# Calculate the net position difference of the attacker against its expected position ---------WIP
def net_position(players,posts):
    ctr = 0
    attacker_id = get_attacker_id(players)
    for p in posts:
        if p.author_id == attacker_id:
            expected_quality_index = len(posts) - 1 - p.quality
            return ctr - expected_quality_index
        ctr += 1 

# Sort lists of posts by quality
def sort_by_quality(posts):
    posts.sort(key=lambda x: x.quality, reverse = True)# no cambiar orden de los posts
    quality_sorted = display_list(posts)
    return quality_sorted


# Print results of execution
def print_result(posts):

    order_posts = display_list(posts)
    quality_sorted = sort_by_quality(posts)
    print ('Final ranking of posts:',order_posts)
    print ('Quality sorted:',quality_sorted)
    print ('Spearman:',stats.spearmanr(quality_sorted, order_posts)[0])
    print ('KendallTau:',stats.kendalltau(quality_sorted, order_posts)[0])

def main():
  
  seed = random.randint(0,1000)
  simulation(seed,10,[15,0,10],0,0,1,5)

  
if __name__== "__main__":
  main()
