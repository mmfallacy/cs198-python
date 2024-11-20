import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as pltcolors
from matplotlib.cm import ScalarMappable
import math

# Honda function. Reliant on vrel only
def honda(vrel, vf):
  return 2.2 * vrel + 6.2
# Hirst & Graham's proposed function. Reliant on both vrel and vf.
def hirstgraham(vrel, vf):
  return 3 * vrel + 0.4905 * vf
# Bella & Russo's proposed function. Reliant on both vrel and vf
def bellarusso(vrel,vf):
  return 1.25 * vrel + 1.55 * vf

# Given dA, dV, wd, calculate the MTTC.
# This outputs the modified time to collision between two vehicles if their headway distance is equal to the warning distance.
# That is, the following car maintains the warning distance.
def MTTC(dA, dV, wd):
    # 1/2dAt^2 + dVt -wd
    roots = np.roots([1/2 * dA, dV, -1 * wd])
    # Only positive real roots
    posreals = roots[(roots>0) & np.isreal(roots)]
    if(len(posreals) < 1): return np.nan # No MTTC/ Impossible to collide.
    # Return minimum positive real root
    return np.min(posreals)

# range() generator function but for floats.
def frange(start, end, step=1):
  while start < end:
    start += step
    yield start

# Conversion of kilometers per hour to meters per second
def kph2mps(kph):
  return kph * 0.27777778

# Conversion of kilometers per sq hour to meters per sq second
def kpsqh2mpsqs(kpsqh):
  return kpsqh / 12960
  
def iqrfilter(Z, scale=1.5):
  q1, q3 = np.percentile(Z, [25,75])

  iqr = q3-q1

  min = q1 - scale * iqr
  max = q3 + scale * iqr

  return np.clip(Z, min, max)