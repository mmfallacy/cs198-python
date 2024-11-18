import numpy as np
from lib import MTTC, bellarusso, hirstgraham, honda

from os import path, makedirs

from persist import save_calc_csv

X_LIM, Y_LIM, GRAN = 10, 30, 300

VFS = [3, 6, 12, 18, 36]

# Calculate function
def calc(fn, vf, max_Z=float('+inf')):
  # Relative Acceleration
  X = np.linspace(-X_LIM, X_LIM, GRAN)
  # Relative Velocity
  Y = np.linspace(-Y_LIM, Y_LIM, GRAN)
  Z = np.zeros((GRAN,GRAN))
  # Create grid of Z values.
  
  # Keep track of maximum Z value
  Z_max = float('-inf')

  # Observe that Z is a 2d-array. Despite being a 2D array, its columns and rows directly translate to the X and Y axes shown in the plot.
  # refer to https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contourf.html.
  # That is, X pertains to the contourf's columns (hence why it is retrieved using j).
  # and consequently, Y pertains to the contourf's rows (hence why it is retrieved using i).
  for i in range(Z.shape[0]):
    for j in range(Z.shape[1]):
      # For row i and col j, get corresponding X and Y value

      x,y = X[j], Y[i]
      # Calculate warning distance given y (vrel) and vf
      wd = fn(y, vf)
      # If warning distance is impossible, set z to np.nan. Otherwise get MTTC
      if (wd<0): z = np.nan
      else: z = MTTC(x,y, wd)

      # Discard nan or negative vl case.
      # MTTC can output np.nan.
      # y (vrel) > vf => vf-vl > vf => -vl > 0 => vl < 0.
      # negative vl is out of our scope.
      if(y > vf or np.isnan(z)): Z[i,j] = np.nan

      else:
        # Update maximum Z value
        if(Z_max < z): Z_max = z
        # Place computed Z in the grid.
        Z[i,j] = z
  
  # Return maximum Z, linspace X and Y, grid Z
  return Z_max, X, Y, Z

def run_calc():
  for fn in [honda, hirstgraham, bellarusso]:
    target_dir = path.join("calculated", fn.__name__)

    # Create target dir if not exists;
    if not path.exists(target_dir): makedirs(target_dir)
    
    for vf in VFS:
      print(f"CALC: Calculating {fn.__name__} for vf={vf}")
      
      _, X, Y, Z = calc(fn, vf)
      
      output = path.join(target_dir, str(vf) + ".csv")

      print(f"CALC: Calculation finished. Saving...")
      save_calc_csv(output , X, Y, Z)

if __name__ == "__main__":
    run_calc()
