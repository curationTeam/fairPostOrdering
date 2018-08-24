from post import Post

class Strategy:
    """
    The Strategy class defines the heuristics a given player uses to vote other posts.
    It's defined by:
    type_strategy(str) - Core strategy of the player. It can be "honest", "greedy" and "user":
                        "honest": creates one post and votes according to likability of posts.
                        "greedy": creates one post and votes to maximize its utility (tbd)
                        "user": do not create posts and votes according to likability of posts

    id(int) - Strategy id. It is the same as the player id.
    min_vp(int) - It is the minimum voting power threshold the player is willing to reach.
    """

    # TODO: attention should be renamed att_span, changed to player property and set in __init__()
    def __init__(self, type_strategy, id):
        self.type_strategy = type_strategy
        self.id = id
        self.min_vp = 1

    def vote(self, posts, attention):
        """
        Players vote according to their strategy.
        Honest and users select their favorite post from the short list of posts given their attention span.
        Greedy (WIP) votes only for her post.
        Returns:
        post: a post or False in case the player do not want to vote.
        """
        if (self.type_strategy == "honest" or self.type_strategy == "user"):
            short_list = self.get_short_list(posts, attention)
            favorite_post = max(short_list, key=lambda x: x.likability[self.id])

            return favorite_post

        elif self.type_strategy == "greedy": #WIP---------
            for post in posts:
                if(post.author_id == self.id and self.id not in post.voters):
                    return post
            return False

    def get_short_list(self, posts, attention):
        """
        Retrieves the k-top list of unvoted posts of the player, where k is defined by the attention parameter.
        Returns:
        list(posts): a list of posts of len ~ attention
        """
        number_posts = 0
        short_list = []

        for post in posts:
            if (self.id not in post.voters and attention > number_posts):
                short_list.append(post)
                number_posts += 1
            if (attention == number_posts):
                break

        return short_list

    def __str__(self):
        return str(self.type_strategy)
