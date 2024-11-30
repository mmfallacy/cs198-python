from os import makedirs, path

from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

from src.const import ALGORITHMS, VFS
from src.persist import load_points_csv
from src.plot import add_plot, clip

def compare_via_vf():
    # Compare algorithms per vf according to calculated analyses
    for vf in VFS:
        # Create 1 row 4 col (honda, hirstgraham, bellarusso, color bar)
        fig, axs = plt.subplots(1, 4, figsize=(15,5), width_ratios=[1,1,1,0.1])

        # For each algorithm
        for i, algo in enumerate(ALGORITHMS):
            # Load points
            XYZ = load_points_csv(f"calculated/{algo.__name__}/{vf}.csv")
            # Create plot (scatter plot, since points are loaded)
            add_plot(fig, axs[i], *clip(XYZ), 7)

            # Differentiate subplots based on algo name
            axs[i].set_title(algo.__name__)
            axs[i].set_xlabel("Relative acceleration dA (af-al)")

            axs[i].set_facecolor("black")
        

        # Set only one y axis label for all plots
        axs[0].set_ylabel("Relative velocities dV (vf-vl)")

        # Differentiate figures based on vf
        fig.suptitle(f"MTTC vs dA and dV (vf={vf})")

        # Create and add color bar
        sm = ScalarMappable(cmap='RdYlGn', norm=Normalize(vmin=0, vmax=7))
        fig.colorbar(sm, cax=axs[3])

        fig.tight_layout()
        
        yield vf, fig

def run_cmp_per_vf(show=False):
    for vf, fig in compare_via_vf():
        out_dir = path.join("assets", "vf")
        makedirs(out_dir, exist_ok=True)
        out = path.join(out_dir, "vf=" + str(vf) + ".png")
        fig.savefig(out)
        if show: plt.show()

if __name__ == "__main__": run_cmp_per_vf()