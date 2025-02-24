
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
  fig, axs = plt.subplots(1, n, figsize=(3*n, 10))
  
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

    
  for i, metric in enumerate(metrics):
    Zs = []

    for algo in ALGORITHMS:
      _, _, Z = load_points_csv(f"plots/{algo.__name__}-vf={vf}/{metric}.csv")
      Zs.append(Z)

    Zs = np.concatenate(Zs).ravel()

    clippedZ = np.clip(Zs, 0, None)

    ax = axs[i]
    ax.hist(clippedZ, bins=200)
    ax.set_xlabel(metric)

    for percentile, color in percentiles.items():
      ax.axvline(np.nanpercentile(Zs, percentile), color=color, linestyle="dashed")

    for quartile, color in quartiles.items():
      ax.axvline(np.nanpercentile(Zs, quartile), color=color)

  metstr = ",".join(metrics)
  fig.suptitle(f"vf={vf} unified Z distribution for {metstr}")
  fig.tight_layout()

  return fig
    
      
def run_show_zdist(vf, metrics, showPlot=False): 
  fig = show_zdist(vf, metrics)
  out_dir = path.join("assets")
  makedirs(out_dir, exist_ok=True)
  metstr = ",".join(metrics)
  out = path.join(out_dir, f"show=uzdist vf={vf} metrics={metstr}.png")

  fig.savefig(out)
  if showPlot: plt.show()