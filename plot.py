
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as pltcolors
from matplotlib.cm import ScalarMappable
import math
from calc import X_LIM, Y_LIM

from persist import load_calc_csv, load_simulated

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plotlyplot(X, Y, Z, max, label):
    fig = go.Figure(
    data=go.Contour(
        z=Z,       # Z values
        x=X,       # X axis
        y=Y,       # Y axis
        colorscale='RdYlGn',  # Set the color scale
        contours_coloring='fill',  # Filled contours
        colorbar=dict(title='Z values')  # Colorbar title
    )
)
    fig.show()

def plot(X,Y,Z, max, label, cbar=False):
    norm = pltcolors.Normalize(vmin=0, vmax=max)

    plt.contourf(X, Y, np.clip(Z, None, max), 800, norm=norm, cmap="RdYlGn")
    plt.xlabel("Relative Acceleration (af-al)")
    plt.ylabel("Relative Velocity (vf-vl)")
    plt.title(f"MTTC vs dA and dV ({label})")
    plt.gca().set_facecolor('black')

    plt.show()


if __name__ == "__main__":
    loaded = load_calc_csv("calculated/hirstgraham/36.csv")
    X,Y,Z = load_simulated("simulated/bellarusso.json")
    plotlyplot(X, Y, Z["first_mttc"], 7, "honda")

    fig, axs = plt.subplots(1,4, figsize=(25,5))

    Z_clipped = [
        np.clip(Z["first_mttc"], None, 7),
        np.clip(Z["ave_headway"], None, 8),
        # Z["ave_headway"],
        Z["tick"],
        np.clip(Z["ave_vx"], 0, None)
    ]

    for (i,Z) in enumerate(Z_clipped):
        scatter = axs[i].scatter(X,Y, c=Z, cmap="RdYlGn")
        sm = ScalarMappable(cmap='RdYlGn', norm=pltcolors.Normalize(vmin=np.min(Z), vmax=np.max(Z)))
        cbar = fig.colorbar(sm, ax=axs[i])
        axs[i].set_facecolor("black")
        axs[i].set_xlim(-X_LIM, X_LIM)
        axs[i].set_ylim(-Y_LIM,Y_LIM)

    axs[0].set_title("mttc on first hit")
    axs[1].set_title("average headway")
    axs[2].set_title("simulation seconds")
    axs[3].set_title("FV average velocity")

    plt.show()

    # plot(*loaded, 7, "honda")