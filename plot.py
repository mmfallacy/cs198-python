
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as pltcolors
from matplotlib.cm import ScalarMappable

from const import ALGORITHMS, VFS, X_LIM, Y_LIM
from persist import load_points_csv

def add_plot(fig, ax, X,Y,_Z, max, cbar=False):
    Z = np.clip(_Z, None, max)
    ax.scatter(X,Y, c=Z, cmap="RdYlGn")
    sm = ScalarMappable(cmap='RdYlGn', norm=pltcolors.Normalize(vmin=np.nanmin(Z), vmax=np.nanmax(Z)))

    if(cbar): fig.colorbar(sm, ax=ax)
    ax.set_facecolor("black")
    ax.set_xlim(-X_LIM, X_LIM)
    ax.set_ylim(-Y_LIM,Y_LIM)

    def fmt(x, y):
        # get closest point with known data
        dist = np.linalg.norm(np.vstack([X - x, Y - y]), axis=0)
        idx = np.argmin(dist)
        z = Z[idx]
        return 'x={x:.5f}  y={y:.5f}  z={z:.5f}'.format(x=x, y=y, z=z)
    ax.format_coord = fmt


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
            add_plot(fig, axs[i], *XYZ, 7)

            # Differentiate subplots based on algo name
            axs[i].set_title(algo.__name__)
            axs[i].set_xlabel("Relative acceleration dA (af-al)")

            axs[i].set_facecolor("black")
        

        # Set only one y axis label for all plots
        axs[0].set_ylabel("Relative velocities dV (vf-vl)")

        # Differentiate figures based on vf
        fig.suptitle(f"MTTC vs dA and dV (vf={vf})")

        # Create and add color bar
        sm = ScalarMappable(cmap='RdYlGn', norm=pltcolors.Normalize(vmin=0, vmax=7))
        fig.colorbar(sm, cax=axs[3])

        fig.tight_layout()
        
        yield vf, fig
        
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
        data["calculated"][2] = np.clip(data["calculated"][2], None, 7)
        data["first_mttc"][2] = np.clip(data["first_mttc"][2], None, 7)

        fig, axs = plt.subplots(1,5, figsize=(20,5))

        for i, (label, xyz) in enumerate(data.items()):
            add_plot(fig, axs[i], *xyz, None, cbar=True)
            axs[i].set_title(label)
            axs[i].set_xlabel("Relative acceleration dA (af-al)")
            axs[i].set_facecolor("black")
        
        # Set only one y axis label for all plots
        axs[0].set_ylabel("Relative velocities dV (vf-vl)")

        # Differentiate figures based on vf
        fig.suptitle(algo.__name__)

        fig.tight_layout()
        yield algo.__name__, fig

def compare_per_metric():
    
    METRICS = ["first_mttc", "ave_headway", "ave_vx", "tick"]

    for metric in METRICS:
        
        fig, axs = plt.subplots(1,4, figsize=(15,5), width_ratios=[1,1,1,0.1])
        
        metric_max = float("-inf");

        data = {}

        for algo in ALGORITHMS:
            X, Y, _Z = load_points_csv(F"cleaned/{algo.__name__}/{metric}.csv")
            
            if(metric=="first_mttc"): Z = np.clip(_Z, None, 7)
            else: Z = _Z
            
            data[algo.__name__] = (X, Y, Z)
            metric_max = max(metric_max, np.nanmax(Z))
            
        # Create and add color bar based on max
        sm = ScalarMappable(cmap='RdYlGn', norm=pltcolors.Normalize(vmin=0, vmax=metric_max))

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