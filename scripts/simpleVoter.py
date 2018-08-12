# Creates a list of two posts and two players. Each player votes for
# each post in the order that they appear in the list and the list is
# reordered after each player completes its vote. We assume that both
# players have 1 SP. We have selected player preferences that show
# that the final order of posts does not correspond to the ideal
# order.

class Post:
  def __init__(self, name, score = 0):
    assert isinstance(name, str)

    self.name = name
    self.score = score

  def __repr__(self):
    return "Post(%r, %r)" % (self.name, self.score)

  def setScore(self, score):
    self.score = score

  def getScore(self):
    return self.score

class Player:
  def __init__(self, name, likes, vpLimit = 0):
    assert isinstance(likes, dict)
    assert isinstance(name, str)
    assert all(0 <= likes[post] <= 1 for post in likes)

    self.name = name
    self.likes = likes
    self.vpLimit = vpLimit

  def __repr__(self):
    return "Player(%r, %r, %r)" % (self.name, self.likes, self.vpLimit)

  def __str__(self):
    return self.name

  def vote(self, posts):
    assert isinstance(posts, list)
    assert all(isinstance(post, Post) for post in posts)
    assert all(0 <= post.getScore() for post in posts)
    assert all(post in self.likes for post in posts)

    vp = 1
    votecost = 0.02 # Cost of full-weight vote in Steem
    votes = {}
    for post in posts:
      votes[post] = self.likes[post] * vp
      vp -= self.likes[post] * votecost
      if vp <= self.vpLimit:
        break
    return votes

def applyVotes(posts, votes):
  assert isinstance(posts, list)
  assert all(isinstance(post, Post) for post in posts)
  assert all(0 <= post.getScore() for post in posts)

  assert isinstance(votes, dict)
  assert all(0 <= votes[post] for post in votes)

  for post in posts:
    if post in votes:
      post.setScore(post.getScore() + votes[post])

  posts.sort(key=lambda x: x.getScore(), reverse = True)

def idealOrder(posts, players):
  assert isinstance(posts, list)
  assert all(isinstance(post, Post) for post in posts)
  assert all(0 <= post.getScore() for post in posts)

  assert isinstance(players, list)
  for player in players:
    assert isinstance(player, Player)
    assert isinstance(player.likes, dict)
    assert all(0 <= player.likes[post] <= 1 for post in player.likes)

  for post in posts:
    post.setScore(0)
    for player in players:
      post.setScore(post.getScore() + player.likes[post])

  posts.sort(key=lambda x: x.getScore(), reverse = True)

posts = [Post('a'), Post('b')]

players = [Player('A', {posts[0]: 0.001, posts[1]: 0.5}),
  Player('B', {posts[0]: 1, posts[1]: 0.5})]

for player in players:
  applyVotes(posts, player.vote(posts))
print('real order:', posts)

idealOrder(posts, players)
print('ideal order:', posts)
