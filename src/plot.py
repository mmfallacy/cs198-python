
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

from src.const import ALGORITHMS, VFS, X_LIM, Y_LIM
from src.lib import iqrfilter, zscorefilter
from src.persist import load_points_csv

def clip(XYZ, filter=iqrfilter):
    X, Y, Z = XYZ
    return X, Y, filter(Z)

def add_plot(fig, ax, X,Y,_Z, max, cbar=False):
    Z = np.clip(_Z, None, max)
    ax.scatter(X,Y, s=1, c=Z, cmap="RdYlGn")
    sm = ScalarMappable(cmap='RdYlGn', norm=Normalize(vmin=np.nanmin(Z), vmax=np.nanmax(Z)))

    if(cbar): fig.colorbar(sm, ax=ax)
    ax.set_facecolor("black")
    ax.set_xlim(-X_LIM, X_LIM)
    ax.set_ylim(-Y_LIM,Y_LIM)

    def fmt(x, y):
        # get closest point with known data
        dist = np.linalg.norm(np.vstack([X - x, Y - y]), axis=0)
        idx = np.argmin(dist)
        z = Z[idx]
        xp = X[idx]
        yp = Y[idx]
        return 'x={x:.5f}  y={y:.5f}  z={z:.5f}'.format(x=xp, y=yp, z=z)
    ax.format_coord = fmt

def add_plot_norm(fig,ax, X,Y,Z, norm, cbar=False):
    ax.scatter(X,Y, s=1, c=Z, norm=norm, cmap="RdYlGn")
    ax.grid(True)

    sm = ScalarMappable(cmap='RdYlGn', norm=norm)
    if(cbar): fig.colorbar(sm, ax=ax)
    ax.set_facecolor("black")
    ax.set_xlim(-X_LIM, X_LIM)
    ax.set_ylim(-Y_LIM,Y_LIM)

    def fmt(x, y):
        # get closest point with known data
        dist = np.linalg.norm(np.vstack([X - x, Y - y]), axis=0)
        idx = np.argmin(dist)
        z = Z[idx]
        xp = X[idx]
        yp = Y[idx]
        return 'x={x:.5f}  y={y:.5f}  z={z:.5f}'.format(x=xp, y=yp, z=z)
    ax.format_coord = fmt