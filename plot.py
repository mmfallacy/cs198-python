
from os import makedirs, path
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

if __name__ == "__main__":
    for vf, fig in compare_via_vf():
        out_dir = path.join("assets", "calculated")
        makedirs(out_dir, exist_ok=True)
        out = path.join(out_dir, "vf=" + str(vf) + ".png")
        plt.savefig(out)
        plt.show()
        break