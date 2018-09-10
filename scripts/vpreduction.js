class Exec {
  constructor(R, M, a, b, regen) {
    this.R = R
    this.M = M
    this.a = a
    this.b = b
    this.regen = regen
    this.vp = 1
  }

  isVoteRound(r) {
    if (this.R < this.M) {
      return true
    }
    const period = (this.R - 1) / (this.M - 1)
    return !Math.floor((r - 1) % period)
  }

  voteRounds() {
    for (let i = 1; i <= this.R; i++)
      if (this.isVoteRound(i))
        console.log(i)
  }

  votingPowerSequence() {
    for (let i = 1; i <= this.R; i++) {
      this.vp = Math.min(this.vp + this.regen, 1)
      console.log(`Voting power is ${this.vp} on round ${i} after regen.`)
      if (this.isVoteRound(i)) {
        if (this.vp < 1) console.log("ATTENTION: VOTING WITHOUT FULL VOTING POWER!")
        const cost = (this.a*this.vp + this.b)
        this.vp = Math.max(this.vp - cost, 0)
        console.log(`voted on ${i}! vp is ${this.vp} after vote.`)
      }
    }
  }

  reset() {
    this.vp = 1
  }

  condHolds() {
    const roundsForRegen = Math.ceil((this.a + this.b) / this.regen)
    return this.R - 1 >= (this.M - 1)*roundsForRegen
  }
}

module.exports = Exec
