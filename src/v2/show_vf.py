
from os import makedirs, path
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import pyperclip

from src.v2.const import ALGORITHMS, VFS
from src.persist import load_points_csv
from src.plot import add_plot_norm, clip

def show_vf(algos, metric, clamp):
  '''
    This function displays a specific metric as follows. 
                |  algo for algo in algos |
    vf = 5
    vf = 11
    vf = 27
  '''

  fig, axs = plt.subplots(len(VFS)+1, len(algos), figsize=(4*len(algos),10), height_ratios=[1,1,1,0.1], squeeze=False)

  cmap = "RdYlGn"
  # Reverse RdYlGn cmap for ticks since high = bad
  if (metric == "tick"): cmap = "RdYlGn_r"

  for j, algo in enumerate(algos):
    XYZs = {}
    lowest, highest = float("+inf"), float("-inf")

    for vf in VFS:
      XYZ = clip(load_points_csv(f"plots/{algo}-vf={vf}/{metric}.csv"))
      lowest = np.nanmin(XYZ[2], initial=lowest)
      highest = np.nanmax(XYZ[2], initial=highest)
      XYZs[vf] = XYZ

    # lowest, highest = 0, 3.5
    if(clamp[0]): lowest = clamp[0]
    if(clamp[1]): highest = clamp[1]

    norm = Normalize(vmin=lowest, vmax=highest) 

    for i, vf in enumerate(VFS):
      XYZ = XYZs[vf]
      add_plot_norm(fig, axs[i][j], *XYZ, norm, cmap=cmap)
      axs[0][j].set_title(algo)
      axs[i][0].set_ylabel(f"dV vf={vf}")
      axs[i][j].set_xlabel("dA")
      axs[i][j].set_facecolor("black")
    
    
    

    sm = ScalarMappable(cmap=cmap, norm=norm)
    fig.colorbar(sm, cax=axs[-1][j], orientation='horizontal')
  
    
  algosstr = ",".join(algos)
  fig.suptitle(f"vf comp for {algosstr}\n(metric={metric})")
  fig.tight_layout()
  
  # Sadly, this does not exactly match the displayed formatted string on the lower right of the figure.
  # This is due to the fact that event.xdata and event.ydata differ from the parameters received in format_coord
  def onclick(event):
      if event.inaxes is not None:
          ax = event.inaxes
          pyperclip.copy(ax.format_coord(event.xdata, event.ydata))

  fig.canvas.mpl_connect("button_press_event", onclick)

  return fig

    
def run_show_vf(algos, metric, clamp, showPlot=False):
  fig = show_vf(algos, metric, clamp)
  out_dir = path.join("assets")
  makedirs(out_dir, exist_ok=True)
  out = path.join(out_dir, f"show=vf metric={metric}.png")

  fig.savefig(out)
  if showPlot: plt.show()
