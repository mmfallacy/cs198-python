
from os import makedirs, path
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import pyperclip

from src.v2.const import ALGORITHMS, VFS
from src.persist import load_points_csv
from src.plot import add_plot_norm, clip

def compare_via_vf(metric, clamp):
  '''
    This function displays a specific metric as follows:
                |  honda  |  hirstgraham  |  bellarusso  |
    vf = 5
    vf = 11
    vf = 27
  '''

  fig, axs = plt.subplots(3, 4, figsize=(15,10), width_ratios=[1,1,1,0.1])

  cmap = "RdYlGn"
  # Reverse RdYlGn cmap for ticks since high = bad
  if (metric in ["tick", "seconds"]): cmap = "RdYlGn_r"
  
  for i, vf in enumerate(VFS):
    XYZs = {}
    lowest, highest = float("+inf"), float("-inf")
    
    for algo in ALGORITHMS:
      XYZs[algo.__name__]= clip(load_points_csv(f"plots/{algo.__name__}-vf={vf}/{metric}.csv")) 

    lowest = 0 
    percentile = 99
    if (metric == "calculated"): percentile = 95

    highest = np.nanpercentile(np.concat(list(Z for X,Y,Z in XYZs.values())), percentile)

    if(clamp[0]): lowest = clamp[0]
    if(clamp[1]): highest = clamp[1]

    norm = Normalize(vmin=lowest, vmax=highest) 

    for j, algo in enumerate(ALGORITHMS):
      XYZ = XYZs[algo.__name__]
      add_plot_norm(fig, axs[i][j], *XYZ, norm, cmap=cmap)
      axs[0][j].set_title(algo.__name__)
      axs[i][j].set_xlabel("dA")
      axs[i][j].set_facecolor("black")
    
    
    axs[i][0].set_ylabel(f"dV vf={vf}")
    

    sm = ScalarMappable(cmap=cmap, norm=norm)
    fig.colorbar(sm, cax=axs[i][3])
    
  fig.suptitle(f"algo vf comparison (metric={metric})")
  fig.tight_layout()
  
  # Sadly, this does not exactly match the displayed formatted string on the lower right of the figure.
  # This is due to the fact that event.xdata and event.ydata differ from the parameters received in format_coord
  def onclick(event):
      if event.inaxes is not None:
          ax = event.inaxes
          pyperclip.copy(ax.format_coord(event.xdata, event.ydata))

  fig.canvas.mpl_connect("button_press_event", onclick)

  return fig

    
def run_cmp_per_vf(metric, clamp, showPlot=False):
  fig = compare_via_vf(metric, clamp)
  out_dir = path.join("assets")
  makedirs(out_dir, exist_ok=True)
  out = path.join(out_dir, f"cmp=vf metric={metric}.png")

  fig.savefig(out)
  if showPlot: plt.show()