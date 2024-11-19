from os import makedirs, path

from matplotlib import pyplot as plt
from plot import compare_per_metric


if __name__ == "__main__":
    for metric, fig in compare_per_metric():
        out_dir = path.join("assets", "simulated")
        makedirs(out_dir, exist_ok=True)
        out = path.join(out_dir, "metric=" + str(metric) + ".png")
        fig.savefig(out)
        plt.show()