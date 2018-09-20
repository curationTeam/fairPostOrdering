from post import Post

class Strategy:
    """
    The Strategy class defines the heuristics a given player uses to vote other posts.
    It's defined by:
    type_strategy(str) - Core strategy of the player. It can be "honest", "selfish" and "user":
                        "honest": creates one post and votes according to likability of posts.
                        "selfish": creates one post and votes to maximize its utility (tbd)
                        "user": do not create posts and votes according to likability of posts

    id(int) - Strategy id. It is the same as the player id.
    min_vp(int) - It is the minimum voting power threshold the player is willing to reach.
    """

    def __init__(self, type_strategy, id, ring_leader_id = None):
        assert(type_strategy in ["honest", "user", "selfish"])
        if type_strategy in ["honest", "user"]:
            assert(ring_leader_id is None)
        else:
            assert(isinstance(ring_leader_id, int))

        self.type_strategy = type_strategy
        self.id = id
        self.ring_leader_id = ring_leader_id
        self.selfish_has_voted = False

    def vote(self, posts, attention):
        """
        Players vote according to their strategy.
        Honest and users select their favorite post from the short list of posts given their attention span.
        Selfish votes only for the post of the ring leader.
        Returns:
        post: a post or False in case the player do not want to vote.
        """
        if (self.type_strategy == "honest" or self.type_strategy == "user"):
            short_list = self.get_short_list(posts, attention)

            if len(short_list) > 0:
                favorite_post = max(short_list, key=lambda x: x.likability[self.id])
                return favorite_post, favorite_post.likability[self.id]
            else:
                return False, False

        elif self.type_strategy == "selfish":
            if not self.selfish_has_voted:
                for post in posts:
                    if (post.author_id == self.ring_leader_id and
                            self.id not in post.voters):
                        self.selfish_has_voted = True
                        return post, 1
                    elif (post.author_id == self.ring_leader_id and
                            self.id in post.voters):
                        raise Error("Optimisation with self.selfish_has_voted failed")
            return False, False
        raise ValueError("type_strategy should be \"honest\", \"user\" or \"selfish\".")

    def get_short_list(self, posts, attention):
        """
        Retrieves the k-top list of unvoted posts of the player, where k is defined by the attention parameter.
        Returns:
        list(posts): a list of posts of len == attention
        """
        short_list = []

        for post in posts:
            if (self.id not in post.voters and attention > len(short_list)):
                short_list.append(post)
            if (attention == len(short_list)):
                break

        return short_list

    def __str__(self):
        return str(self.type_strategy)
