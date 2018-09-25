import matplotlib.pyplot as plt

class Utils:
    @staticmethod
    def plot_and_save(x, y, x_label, y_label):
        plt.rc('text', usetex = True)
        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        name = "figures/" + str(x[-1] + 1) + "_" + "".join(y_label.split(" ")) + ".png"
        plt.savefig(name)
        plt.show()

    @staticmethod
    def plot_and_save2(x, y1, y2, x_label, y1_label, y2_label):
        plt.rc('text', usetex = True)
        plt.plot(x, y1, label=y1_label)
        plt.plot(x, y2, label=y2_label)
        plt.xlabel(x_label)
        plt.legend()
        name = "figures/" + str(x[-1] + 1) + "_" + "y1y2" + "SUB.png"
        plt.savefig(name)
        plt.show()
