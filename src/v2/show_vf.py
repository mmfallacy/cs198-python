
from os import makedirs, path
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import pyperclip

from src.v2.const import ALGORITHMS, VFS
from src.persist import load_points_csv
from src.plot import add_plot_norm, clip

def show_vf(algo, metrics, clamp):
  '''
    This function displays a specific metric as follows. 
                |  metric for metric in metric |
    vf = 5
    vf = 11
    vf = 27
  '''

  fig, axs = plt.subplots(len(VFS)+1, len(metrics), figsize=(4*len(metrics),10), height_ratios=[1,1,1,0.1], squeeze=False)

  for j, metric in enumerate(metrics):

    cmap = "RdYlGn"
    # Reverse RdYlGn cmap for ticks since high = bad
    if (metric in ["tick", "seconds"]): cmap = "RdYlGn_r"
    XYZs = {}
    lowest, highest = float("+inf"), float("-inf")

    for vf in VFS:
      XYZs[vf]= load_points_csv(f"plots/{algo}-vf={vf}/{metric}.csv")

    lowest = 0
    
    percentile = 99
    if (metric == "calculated"): percentile = 95

    highest = np.nanpercentile(np.concat(list(Z for X,Y,Z in XYZs.values())), percentile)

    if(clamp[0]): lowest = clamp[0]
    if(clamp[1]): highest = clamp[1]

    norm = Normalize(vmin=lowest, vmax=highest) 

    for i, vf in enumerate(VFS):
      XYZ = XYZs[vf]
      add_plot_norm(fig, axs[i][j], *XYZ, norm, cmap=cmap)
      axs[0][j].set_title(metric)
      axs[i][0].set_ylabel(f"dV vf={vf}")
      axs[i][j].set_xlabel("dA")
      axs[i][j].set_facecolor("black")
    
    
    

    sm = ScalarMappable(cmap=cmap, norm=norm)
    fig.colorbar(sm, cax=axs[-1][j], orientation='horizontal')
  
    
  metricsstr = ",".join(metrics)
  fig.suptitle(f"vf comp for {metricsstr} for {algo}")
  fig.tight_layout()
  
  # Sadly, this does not exactly match the displayed formatted string on the lower right of the figure.
  # This is due to the fact that event.xdata and event.ydata differ from the parameters received in format_coord
  def onclick(event):
      if event.inaxes is not None:
          ax = event.inaxes
          pyperclip.copy(ax.format_coord(event.xdata, event.ydata))

  fig.canvas.mpl_connect("button_press_event", onclick)

  return fig

    
def run_show_vf(algo, metrics, clamp, showPlot=False):
  fig = show_vf(algo, metrics, clamp)
  out_dir = path.join("assets")
  makedirs(out_dir, exist_ok=True)
  metricsstr = ",".join(metrics)
  out = path.join(out_dir, f"show=vf metric={metricsstr} algo={algo}.png")

  fig.savefig(out)
  if showPlot: plt.show()
