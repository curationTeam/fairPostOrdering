from math import floor, ceil
from post import Post
from strategy import Strategy

class Player:
    """
    Player class which determines the properties of a player.
    A player is determined by:
        id(int) - id of the player
        strategy(Strategy) - Strategy followed by the player
        vp(int) - Current Voting Power that the player has.
        attention(int) - Number of posts that the player can view in a round.
    """

    def __init__(self, id, type, sp, attention, a, b, regen, rounds, noPost):
        self.id = id
        self.strategy = Strategy(type, id)
        self.sp = sp
        self.vp = 1
        self.attention = attention
        self.a = a
        self.b = b
        self.regen = regen
        self.voteRounds = self.buildVoteRounds(rounds, noPost)

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

    def spend_vp(self, weight):
        self.vp = max(self.vp - (self.a * self.vp * weight + self.b), 0)

    def calculate_vote_score(self, weight):
        return self.sp * (self.a * self.vp * weight + self.b)

    def regenerate_vp(self):
        self.vp = min(self.vp + self.regen, 1) # TODO: Define regen in terms of rounds

    def buildVoteRounds(self, R, noPost):
        voteRounds = set()
        # if there are many rounds,
        # leave isVoteRound() to vote when vp is full
        if R - 1 < (noPost - 1)*ceil((self.a + self.b) / self.regen):
            for i in range(0, R):
                voteRound = floor(i * (R - 1) / (noPost - 1))
                if voteRound > R:
                    break
                voteRounds.add(voteRound)
        return voteRounds

    def isVoteRound(self, r, voteRounds):
        if self.vp == 1:
            return True
        return r in voteRounds

    def vote(self, r, posts):
        """
        Player votes for a post from a list of posts only if her Voting Power is greater than the Minimum
        Voting Power defined by her Strategy.
        Return:
        post(Post) - post to be voted by the player (False if the player does not vote for any post)
        """
        if self.isVoteRound(r, self.voteRounds):
            post, weight = self.strategy.vote(posts, self.attention)
            if post:
                assert(self.id not in post.voters)
                post.real_score += self.calculate_vote_score(weight)
                post.voters.add(self.id)
                self.spend_vp(weight)
