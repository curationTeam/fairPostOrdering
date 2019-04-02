from pvs import PVS
import matplotlib.pyplot as plt
from utils import Utils

plt.rc('text', usetex = True)

honestNo = 100
selfishMax = 100
a = 1/50
b = 0.0001
regen_time = 3 / (5*24*60) # as in Steem x60
att_span = 10
noRound = 5000
choice = 0 # 0 for uniform, 1 for beta
handicap = 1

def main():
    sybil_size = []
    gains = []
    t_convs = []
    kendalls = []
    spearmans = []

    for i in range(0, selfishMax):
        print("selfish:", i)
        noProfiles = (100, i, 0)
        sp = (1,) * sum(noProfiles)
        gain, t_conv, kendall, spearman = PVS(noProfiles, sp, a, b, regen_time,
              att_span, noRound, choice, handicap).execute(output = False)

        sybil_size.append(i)
        gains.append(gain)
        t_convs.append(t_conv)
        kendalls.append(kendall)
        spearmans.append(spearman)

    Utils.plot_and_save(sybil_size, gains, "Voting Ring Size", "Positions Gained")
    Utils.plot_and_save(sybil_size, t_convs, "Voting Ring Size", "$t$-ideal rank")
    Utils.plot_and_save(sybil_size, kendalls, "Voting Ring Size", "Kendall's Tau")
    Utils.plot_and_save(sybil_size, spearmans, "Voting Ring Size", "Spearman's Rho")
    Utils.plot_and_save2(sybil_size, kendalls, spearmans,
                         "Voting Ring Size", "Kendall's Tau", "Spearman's Rho")

if __name__== "__main__":
    main()
