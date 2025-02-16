
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import pyperclip

from src.const import ALGORITHMS, VFS, X_LIM, Y_LIM
from src.lib import iqrfilter, zscorefilter
from src.persist import load_points_csv

def clip(XYZ, filter=iqrfilter):
    X, Y, Z = XYZ
    return X, Y, filter(Z)
    
def createFormatter(X,Y,Z):
    THRESH = 0.1
    def fmt(x, y):
        # get closest point with known data
        dist = np.linalg.norm(np.vstack([X - x, Y - y]), axis=0)
        idx = np.argmin(dist)
        delta = np.nanmin(dist)
        # if distance is more than threshold, it means the cursor far in the black region.
        z = np.nan if delta > THRESH else Z[idx]
        xp = X[idx]
        yp = Y[idx]
        # xy pertains to the current point the cursor is in
        # xyp pertains to the x and y of the nearest datapoint
        # z pertains to the nearest Z value. 
        # Since we cull invalid and nan cases, we set z to np.nan 
        # when cursor is significantly far from the nearest data point
        return 'xy=({x:.5f},{y:.5f}) xyp=({xp:.5f},{yp:.5f}) z={z:.5f}'.format(x=x, y=y, xp=xp, yp=yp, z=z)
    return fmt

def add_plot(fig, ax, X,Y,_Z, max, cmap="RdYlGn", cbar=False):
    Z = np.clip(_Z, None, max)
    ax.scatter(X,Y, s=1, c=Z, cmap=cmap)
    sm = ScalarMappable(cmap=cmap, norm=Normalize(vmin=np.nanmin(Z), vmax=np.nanmax(Z)))

    if(cbar): fig.colorbar(sm, ax=ax)
    ax.set_facecolor("black")
    ax.set_xlim(-X_LIM, X_LIM)
    ax.set_ylim(-Y_LIM,Y_LIM)

    ax.format_coord =  createFormatter(X,Y,Z)

    def onclick(event):
        if event.xdata is not None and event.ydata is not None: pyperclip.copy(ax.format_coord(event.xdata, event.ydata))

    fig.canvas.mpl_connect("button_press_event", onclick)

def add_plot_norm(fig,ax, X,Y,Z, norm, cmap="RdYlGn", cbar=False):
    ax.scatter(X,Y, s=1, c=Z, norm=norm, cmap=cmap)
    ax.grid(True)

    sm = ScalarMappable(cmap=cmap, norm=norm)
    if(cbar): fig.colorbar(sm, ax=ax)
    ax.set_facecolor("black")
    ax.set_xlim(-X_LIM, X_LIM)
    ax.set_ylim(-Y_LIM,Y_LIM)

    ax.format_coord = createFormatter(X,Y,Z)
    
    def onclick(event):
        if event.xdata is not None and event.ydata is not None: pyperclip.copy(ax.format_coord(event.xdata, event.ydata))

    fig.canvas.mpl_connect("button_press_event", onclick)
    