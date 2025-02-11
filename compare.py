from os import makedirs, path
import sys

from matplotlib import pyplot as plt
import numpy as np

from src.const import ALGORITHMS
from src.persist import load_points_csv
from src.plot import add_plot, clip

def compare(a, b):

    fig, axs = plt.subplots(2,4, figsize= (15,10))

    for i, file in enumerate([a,b]):
        data = {
            "first_mttc": list(load_points_csv(f"cleaned/{file}/first_mttc.csv")),
            "ave_headway": load_points_csv(f"cleaned/{file}/ave_headway.csv"),
            "ave_vx": load_points_csv(f"cleaned/{file}/ave_vx.csv"),
            "ticks" :load_points_csv(f"cleaned/{file}/tick.csv")
        }
        
        # Clamping:
        data["first_mttc"][2] = np.clip(data["first_mttc"][2], None, 7)

        for j, (label, xyz) in enumerate(data.items()):
            add_plot(fig, axs[i,j], *clip(xyz), None, cbar=True)
            axs[i,j].set_title(label)
            axs[i,j].set_xlabel("Relative acceleration dA (af-al)")
            axs[i,j].set_facecolor("black")
        
        # Set only one y axis label for all plots
        axs[i,0].set_ylabel("Relative velocities dV (vf-vl)")

    # Differentiate figures based on vf
    fig.suptitle(f"{a} vs {b}")

    fig.tight_layout()
    return fig

def run_cmp(a, b,show=False):
    fig = compare(a, b)
    out_dir = path.join("assets", "sim")
    makedirs(out_dir, exist_ok=True)
    out = path.join(out_dir, str(f"{a}vs{b}") + ".png")
    fig.savefig(out)
    if show: plt.show()

if __name__ == "__main__": 
    prog, *args = sys.argv
    run_cmp(args[0], args[1], True)