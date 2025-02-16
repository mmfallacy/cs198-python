
from os import makedirs, path
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

from src.v2.const import ALGORITHMS, VFS
from src.persist import load_points_csv
from src.plot import add_plot_norm, clip

def compare_per_algo(vf, metrics, clamp):
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
      XYZ = clip(load_points_csv(f"plots/{algo.__name__}-vf={vf}/{metric}.csv"))
      lowest = np.nanmin(XYZ[2], initial=lowest)
      highest = np.nanmax(XYZ[2], initial=highest)
      XYZs[algo.__name__] = XYZ
         
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
  fig.suptitle(f"algo comparison for {metstr}")
  fig.tight_layout()
  
  return fig

def run_cmp_per_algo(vf, metrics, clamp, showPlot=False):
  fig = compare_per_algo(vf, metrics, clamp)
  out_dir = path.join("assets")
  makedirs(out_dir, exist_ok=True)
  metstr = ",".join(metrics)
  out = path.join(out_dir, f"cmp=algo vf={vf} metrics={metstr}.png")

  fig.savefig(out)
  if showPlot: plt.show()
  