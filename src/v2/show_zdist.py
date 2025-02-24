
from os import makedirs, path
from matplotlib import pyplot as plt
import numpy as np
from src.const import ALGORITHMS
from src.persist import load_points_csv


def show_zdist(vf, metrics):
  '''
    This function displays a specific metric as follows:
                |  metric[0]  |  ...  |  metric[-1]  |
    honda
    hirstgraham
    bellarusso
  '''

  n = len(metrics)
  fig, axs = plt.subplots(3, n, figsize=(3*n, 10))
  
  percentiles = {
    99: "purple",
    # 98: "green",
    # 97: "yellow",
    95: "red",
    90: "black"
  }
  quartiles = {
    25: "cyan",
    75: "orange",
  }

    
  for i, algo in enumerate(ALGORITHMS):
    for j, metric in enumerate(metrics):
      _,_,Z = load_points_csv(f"plots/{algo.__name__}-vf={vf}/{metric}.csv")

      clippedZ = np.clip(Z, 0, None)
      
      ax = axs[i][j]
      ax.hist(clippedZ, bins=100)
      for percentile, color in percentiles.items():
        ax.axvline(x=np.nanpercentile(Z, percentile), color=color, linestyle="dashed")
      for quartile, color in quartiles.items():
        ax.axvline(x=np.nanpercentile(Z, quartile), color=color)
      ax.set_xlabel(metric)

    axs[i][0].set_ylabel(algo.__name__)
  
  metstr = ",".join(metrics)
  fig.suptitle(f"vf={vf} value distribution for {metstr}")
  fig.tight_layout()
  return fig
      
def run_show_zdist(vf, metrics, showPlot=False): 
  fig = show_zdist(vf, metrics)
  out_dir = path.join("assets")
  makedirs(out_dir, exist_ok=True)
  metstr = ",".join(metrics)
  out = path.join(out_dir, f"show=zdist vf={vf} metrics={metstr}.png")

  fig.savefig(out)
  if showPlot: plt.show()