import random

class Post:
    """
    The Post class defines the characteristics of the posts in the social media platform.
    It's defined by:
    author_id(int) - id of the player who created the post.
    likability(list(int)) - determines how much each player likes (in [0, 1]) a post
    quality(int) - average of the likability of a post (needed to give the ideal ordering)
    votes_received(float) - value of all received votes
    voters(list(int)) - ids of player who have already voted the post
    """

    def __init__(self, player_id, quality, players):
        self.author_id = player_id
        self.likability = self.get_likability(quality, players)
        self.quality = sum(self.likability) / len(self.likability)
        self.votes_received = 0
        self.voters = []

    def get_likability(self, quality, players):
        """
        Assigns the likability of the post to each of the players given the quality of the author of the post.
        In practice, it just gives a random variable following a gaussian distribution with a determined mean
        and std deviation.
        Return:
        likability (list(int)) - list of integers which determines how much each of the players likes a post
                                 It's defined from [0, 1] for each of the N players.
        """
        likability = []

        for _player in players:
            random_like = random.gauss(quality[0], quality[1])

            if random_like >= 1:
                random_like = 1

            elif random_like <= 0:
                random_like = 0

            likability.append(random_like)

        return likability

    def __str__(self):
        return str(self.author_id)

    def __repr__(self):
        return "Post(author = %r, quality = %r, votes = %r)" % \
          (self.author_id, self.quality, self.votes_received)
