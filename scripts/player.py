from post import Post
from strategy import Strategy

class Player:
    """
    Player class which determines the properties of a player.
    A player is determined by:
        id(int) - id of the player
        quality(int, int) - Mean and st deviation of the quality of the posts created by the player
        strategy(Strategy) - Strategy followed by the player
        vp(int) - Current Voting Power that the player has.
        attention(int) - Number of posts that the player can view in a round.
    """

    def __init__(self, id, quality_mean, quality_sd, type, sp, attention):
        self.id = id
        # TODO: use a function that returns a tuple of N numbers in [0, 1]
        #       instead of mean and standard deviation for quality
        self.quality = [quality_mean, quality_sd]
        self.strategy = Strategy(type, id)
        self.sp = sp
        self.vp = 1
        self.attention = attention

    def set_strategy(self, strategy):
        """
        Set core strategy of the player (e.g. honest or greedy).
        """
        self.strategy = strategy

    def set_sp(self, sp):
        """
        Set Steem Power of the player.
        """
        self.sp = sp

    def set_vp(self, vp):
        """
        Set Voting Power of the player.
        """
        self.vp = vp

    def set_quality(self, quality_mean, quality_sd):
        """
        Set quality of "writing posts" of the player.
        """
        self.quality = [quality_mean, quality_sd]

    def spend_vp(self, a, weight, b):
        self.vp = max(self.vp - (a * self.vp * weight + b), 0)

    def regenerate_vp(self, c):
        self.vp = min(self.vp + c, 1) # TODO: We have to define c in terms of the rounds

    def create_post(self, quality, players):
        """
        Player creates a Post given its quality parameters.
        Return:
        post(Post) - Post created by the player
        """
        post = Post(self.id, self.quality, players)
        return post

    def vote(self, posts):
        """
        Player votes for a post from a list of posts only if her Voting Power is greater than the Minimum
        Voting Power defined by her Strategy.
        Return:
        post(Post) - post to be voted by the player (False if the player does not vote for any post)
        """
        #Only vote if voting power greater or equal than minimum voting power of the strategy
        if self.vp >= self.strategy.min_vp:
            return self.strategy.vote(posts, self.attention)
        else:
            return False
