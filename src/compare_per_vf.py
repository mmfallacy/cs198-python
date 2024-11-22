from os import makedirs, path

from matplotlib import pyplot as plt
from plot import compare_via_vf


if __name__ == "__main__":
    for vf, fig in compare_via_vf():
        out_dir = path.join("assets", "calculated")
        makedirs(out_dir, exist_ok=True)
        out = path.join(out_dir, "vf=" + str(vf) + ".png")
        fig.savefig(out)
        plt.show()