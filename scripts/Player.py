
from Post import Post
from Strategy import Strategy

class Player:
    def __init__(self, id, quality_mean, quality_st, type, sp, attention):

        self.id = id
        self.quality = [quality_mean,quality_st]
        self.strategy = Strategy(type,id)
        self.sp = sp
        self.vp = 1
        self.attention = attention
        
    def set_strategy(self, strategy):
        self.strategy = strategy

    def set_sp(self, sp):
        self.sp = sp

    def set_vp(self, vp):
        self.vp = vp

    def set_quality(self,quality_mean, quality_st):

        self.quality = [quality_mean,quality_st]

    def create_post(self,quality,players):
        post = Post(self.id,self.quality, players)
        return post

    def vote(self,posts):
        #Only vote if voting power greater or equal than minimum voting power of the strategy
        if self.vp >= self.strategy.min_vp:
            return self.strategy.vote(posts,self.attention)
        else:
            return False
