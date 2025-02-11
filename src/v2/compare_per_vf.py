
from os import makedirs, path
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

from src.v2.const import ALGORITHMS, VFS
from src.persist import load_points_csv
from src.plot import add_plot, add_plot_norm, clip

def compare_via_vf(metric):
  '''
    This function displays a specific metric as follows:
                |  honda  |  hirstgraham  |  bellarusso  |
    vf = 5
    vf = 11
    vf = 27
  '''

  fig, axs = plt.subplots(3, 4, figsize=(15,10), width_ratios=[1,1,1,0.1])
  
  for i, vf in enumerate(VFS):
    XYZs = {}
    lowest, highest = float("+inf"), float("-inf")
    
    for algo in ALGORITHMS:
      XYZ = clip(load_points_csv(f"plots/{algo.__name__}-vf={vf}/{metric}.csv")) 
      # lowest = np.nanmin(XYZ[2], initial=lowest)
      # highest = np.nanmax(XYZ[2], initial=highest)
      XYZs[algo.__name__] = XYZ

    lowest, highest = 0, 3.5
    norm = Normalize(vmin=lowest, vmax=highest) 

    for j, algo in enumerate(ALGORITHMS):
      XYZ = XYZs[algo.__name__]
      add_plot_norm(fig, axs[i][j], *XYZ, norm, None)
      axs[1][j].set_title(algo.__name__)
      axs[i][j].set_xlabel("dA")
      axs[i][j].set_facecolor("black")
    
    
    axs[i][0].set_ylabel(f"dV vf={vf}")
    sm = ScalarMappable(cmap="RdYlGn", norm=norm)
    fig.colorbar(sm, cax=axs[i][3])
    
  fig.suptitle(f"algo vf comparison (metric={metric})")
  fig.tight_layout()
  
  return fig

    
def run_cmp_per_vf(metric, showPlot=False):
  fig = compare_via_vf(metric)
  out_dir = path.join("assets")
  makedirs(out_dir, exist_ok=True)
  out = path.join(out_dir, f"cmp=vf metric={metric}.png")

  fig.savefig(out)
  if showPlot: plt.show()