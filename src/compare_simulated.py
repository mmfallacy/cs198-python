from os import makedirs, path

from matplotlib import pyplot as plt
from plot import compare_simulated


if __name__ == "__main__":
    for algo, fig in compare_simulated():
        out_dir = path.join("assets", "simulated")
        makedirs(out_dir, exist_ok=True)
        out = path.join(out_dir, "algo=" + str(algo) + ".png")
        fig.savefig(out)
        plt.show()