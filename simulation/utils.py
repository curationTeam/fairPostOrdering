import matplotlib.pyplot as plt

class Utils:
    @staticmethod
    def plot_and_save(x, y, x_label, y_label):
        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        name = "figures/" + str(x[-1] + 1) + "_" + y_label + ".png"
        plt.savefig(name)
        plt.show()
