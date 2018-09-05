import random

class Post:
    """
    The Post class defines the characteristics of the posts in the social media platform.
    It's defined by:
    author_id(int) - id of the player who created the post.
    likability(list(int)) - determines how much each player likes (in [0, 1]) a post
    ideal_score(int) - average of the likability of a post (needed to give the ideal ordering)
    real_score(float) - value of all received votes
    voters(list(int)) - ids of player who have already voted the post
    """

    def __init__(self, player_id, likability):
        self.author_id = player_id
        self.likability = likability
        self.ideal_score = sum(self.likability) / len(self.likability)
        self.real_score = 0
        self.voters = set()

    def __str__(self):
        return str(self.author_id)

    def __repr__(self):
        return "Post(author = %r, ideal score = %r, real score = %r)" % \
          (self.author_id, self.ideal_score, self.real_score)
