
from Post import Post
from Strategy import Strategy

class Player:
    """
    Player class which determines the properties of a player.
    A player is determined by:
        id(int) -  id of the player
        quality(int,int) - Mean and st deviation of the quality of the posts created by the player
        strategy(Strategy) -  Strategy followed by the player
        vp(int)  -  Current Voting Power that the player has.
        attention(int) - Number of post that the player can view in a round.
    """
    def __init__(self, id, quality_mean, quality_st, type, sp, attention):

        self.id = id
        self.quality = [quality_mean,quality_st]
        self.strategy = Strategy(type,id)
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

    def set_quality(self,quality_mean, quality_st):

        """
        Set quality of "writing posts" of the player.
        """

        self.quality = [quality_mean,quality_st]

    def create_post(self,quality,players):

        """
        Player creates a Post given its quality parameters.
        Return:
        post(Post) - Post created by the player
        """

        post = Post(self.id,self.quality, players)
        return post

    def vote(self,posts):

        """
        Player votes for a post from a list of posts only if her Voting Power is greater than the Minimum
        Voting Power defined by her Strategy.
        Return: 
        post(Post) - post to be voted by the player (False if the player do not vote for any post) 
        """

        #Only vote if voting power greater or equal than minimum voting power of the strategy
        if self.vp >= self.strategy.min_vp:
            return self.strategy.vote(posts,self.attention)
        else:
            return False
