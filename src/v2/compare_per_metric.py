
from os import makedirs, path
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import pyperclip

from src.v2.const import ALGORITHMS, VFS
from src.persist import load_points_csv
from src.plot import add_plot_norm, clip

def getMinMax(X, Y, Z): 
  min = np.nanargmin(Z)
  max = np.nanargmax(Z)
  
  return (X[min], Y[min], Z[min]), (X[max], Y[max], Z[max])

def prune(metric, X,Y,Z):
  if metric=="tick":
    mask = Z < 100_000
  elif metric == "seconds":
    mask = Z < 833.33
  elif metric == "ave_vx":
    mask = Z >= 0
  else:
    return X, Y, Z
    
  return X[mask], Y[mask], Z[mask]

def compare_per_metric(vf, metrics, clamp):
  '''
    This function displays a specific metric as follows:
                |  metric[0]  |  ...  |  metric[-1]  |
    honda
    hirstgraham
    bellarusso
  '''

  n = len(metrics)
  fig, axs = plt.subplots(4, n, figsize=(3*n,10), height_ratios=[1,1,1,0.1])
  
  for j, metric in enumerate(metrics):
    XYZs = {}
    lowest, highest = np.inf, -np.inf
    
    for algo in ALGORITHMS:
      XYZ = load_points_csv(f"plots/{algo.__name__}-vf={vf}/{metric}.csv")
      min, max = getMinMax(*XYZ)
      fmt = "dA = {0:.2f}\ndV = {1:.2f}\n{2:.2f}"
      print(metric, algo.__name__, "Minimum")
      print(fmt.format(*min))
      print(metric, algo.__name__, "Maximum")
      print(fmt.format(*max))
      XYZs[algo.__name__] = XYZ
       
    lowest = 0
    
    percentile = 99
    if (metric == "calculated"): percentile = 95
    if (metric in ["tick", "seconds"]): percentile = 70

    highest = np.nanpercentile(np.concat(list(Z for X,Y,Z in XYZs.values())), percentile)

    if(clamp[0]): lowest = clamp[0]
    if(clamp[1]): highest = clamp[1]

    norm = Normalize(vmin=lowest, vmax=highest)

    cmap = "RdYlGn"
    # Reverse RdYlGn cmap for ticks since high = bad
    if (metric in ["tick", "seconds"]): cmap = "RdYlGn_r"
    
    for i, algo in enumerate(ALGORITHMS):
      XYZ = XYZs[algo.__name__]
      add_plot_norm(fig, axs[i][j], *XYZ, norm, cmap=cmap)
      axs[i][0].set_ylabel(f"dV {algo.__name__}")
      axs[i][j].set_xlabel("dA")
      axs[i][j].set_facecolor("black")

    axs[0][j].set_title(metric)
    sm = ScalarMappable(cmap=cmap, norm=norm)
    fig.colorbar(sm, cax=axs[-1][j], orientation='horizontal')
      
    
    
  metstr = ",".join(metrics)
  fig.suptitle(f"vf={vf} per metric comparison for {metstr}")
  fig.tight_layout()

  # Sadly, this does not exactly match the displayed formatted string on the lower right of the figure.
  # This is due to the fact that event.xdata and event.ydata differ from the parameters received in format_coord
  def onclick(event):
      if event.inaxes is not None:
          ax = event.inaxes
          pyperclip.copy(ax.format_coord(event.xdata, event.ydata))

  fig.canvas.mpl_connect("button_press_event", onclick)
  
  return fig

def run_cmp_per_metric(vf, metrics, clamp, showPlot=False):
  fig = compare_per_metric(vf, metrics, clamp)
  out_dir = path.join("assets")
  makedirs(out_dir, exist_ok=True)
  metstr = ",".join(metrics)
  out = path.join(out_dir, f"cmp=metric vf={vf} metrics={metstr}.png")

  fig.savefig(out)
  if showPlot: plt.show()
  