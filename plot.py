
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as pltcolors
from matplotlib.cm import ScalarMappable
import math

from persist import load_calc_csv

def plot(X,Y,Z, max, label, cbar=False):
    norm = pltcolors.Normalize(vmin=0, vmax=max)

    plt.contourf(X, Y, np.clip(Z, None, max), 800, norm=norm, cmap="RdYlGn")
    plt.xlabel("Relative Acceleration (af-al)")
    plt.ylabel("Relative Velocity (vf-vl)")
    plt.title(f"MTTC vs dA and dV ({label})")

    plt.show()


if __name__ == "__main__":
    loaded = load_calc_csv("calculated/honda/36.csv")

    plot(*loaded, 7, "honda")