from os import makedirs, path

from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import numpy as np

from src.const import ALGORITHMS
from src.persist import load_points_csv
from src.plot import add_plot, clip

def compare_per_metric():
    
    METRICS = ["first_mttc", "ave_headway", "ave_vx", "tick"]

    for metric in METRICS:
        
        fig, axs = plt.subplots(1,4, figsize=(15,5), width_ratios=[1,1,1,0.1])
        
        metric_max = float("-inf");

        data = {}

        for algo in ALGORITHMS:
            X, Y, Z = clip(load_points_csv(F"cleaned/{algo.__name__}/{metric}.csv"))

            data[algo.__name__] = (X, Y, Z)
            metric_max = max(metric_max, np.nanmax(Z))
            
        # Create and add color bar based on max
        sm = ScalarMappable(cmap='RdYlGn', norm=Normalize(vmin=0, vmax=metric_max))

        for i, (label, xyz) in enumerate(data.items()):
            add_plot(fig, axs[i], *xyz, metric_max)
            axs[i].set_title(label)
            axs[i].set_xlabel("Relative acceleration dA (af-al)")
            axs[i].set_facecolor("black")

        # Set only one y axis label for all plots
        axs[0].set_ylabel("Relative velocities dV (vf-vl)")

        fig.colorbar(sm, cax=axs[3])

        # Differentiate figures based on vf
        fig.suptitle(metric)

        fig.tight_layout()

        yield metric, fig

def run_cmp_per_metric(show=False):
    for metric, fig in compare_per_metric():
        out_dir = path.join("assets", "metric")
        makedirs(out_dir, exist_ok=True)
        out = path.join(out_dir, str(metric) + ".png")
        fig.savefig(out)
        if show: plt.show()

if __name__ == "__main__": run_cmp_per_metric()