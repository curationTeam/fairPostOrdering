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
      if (this.vtr(i))
        console.log(i)
  }

  votingPowerSequence() {
    for (let i = 1; i <= this.R; i++) {
      this.vp = Math.min(this.vp + this.regen, 1)
      console.log(`Voting power is ${this.vp} on round ${i}.`)
      if (this.vtr(i)) {
        console.log(`voted on ${i}!`)
        const cost = (this.a*this.vp + this.b)
        this.vp = Math.max(this.vp - cost, 0)
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
