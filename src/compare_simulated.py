from os import makedirs, path

from matplotlib import pyplot as plt
import numpy as np

from src.const import ALGORITHMS
from src.persist import load_points_csv
from src.plot import add_plot, clip

def compare_simulated():
    # Compare algorithms as such:
    # Calculated (vf=36) | Simulated: first_mttc, ave_headway, ave_vx, ticks

    for algo in ALGORITHMS:
        data = {
            "calculated": list(load_points_csv(f"calculated/{algo.__name__}/36.csv")),
            "first_mttc": list(load_points_csv(f"cleaned/{algo.__name__}/first_mttc.csv")),
            "ave_headway": load_points_csv(f"cleaned/{algo.__name__}/ave_headway.csv"),
            "ave_vx": load_points_csv(f"cleaned/{algo.__name__}/ave_vx.csv"),
            "ticks" :load_points_csv(f"cleaned/{algo.__name__}/tick.csv")
        }
        
        # Clamping:
        data["calculated"][2] = np.clip(data["calculated"][2], None, 4)
        data["first_mttc"][2] = np.clip(data["first_mttc"][2], None, 4)

        fig, axs = plt.subplots(1,5, figsize=(20,5))

        for i, (label, xyz) in enumerate(data.items()):
            add_plot(fig, axs[i], *clip(xyz), None, cbar=True)
            axs[i].set_title(label)
            axs[i].set_xlabel("Relative acceleration dA (af-al)")
            axs[i].set_facecolor("black")
        
        # Set only one y axis label for all plots
        axs[0].set_ylabel("Relative velocities dV (vf-vl)")

        # Differentiate figures based on vf
        fig.suptitle(algo.__name__)

        fig.tight_layout()
        yield algo.__name__, fig

def run_cmp_sim(show=False):
    for algo, fig in compare_simulated():
        out_dir = path.join("assets", "sim")
        makedirs(out_dir, exist_ok=True)
        out = path.join(out_dir, str(algo) + ".png")
        fig.savefig(out)
        if show: plt.show()

if __name__ == "__main__": run_cmp_sim()