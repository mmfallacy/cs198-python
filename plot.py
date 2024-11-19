
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as pltcolors
from matplotlib.cm import ScalarMappable
from calc import X_LIM, Y_LIM

from persist import load_points_csv, load_simulated

def add_plot(fig, ax, X,Y,_Z, max):
    Z = np.clip(_Z, None, max)
    ax.scatter(X,Y, c=Z, cmap="RdYlGn")
    sm = ScalarMappable(cmap='RdYlGn', norm=pltcolors.Normalize(vmin=np.nanmin(Z), vmax=np.nanmax(Z)))
    fig.colorbar(sm, ax=ax)
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


if __name__ == "__main__":
    loaded = load_points_csv("calculated/bellarusso/36.csv")
    fig, ax = plt.subplots()

    add_plot(fig, ax, *loaded, 7)

    plt.show()