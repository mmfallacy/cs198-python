import numpy as np
from os import path, makedirs

from src.const import ALGORITHMS, GRAN, VFS, X_LIM, Y_LIM
from src.lib import MTTC
from src.persist import save_points_csv

def calc(fn, vf):
  # Relative Acceleration
  X = np.linspace(-X_LIM, X_LIM, GRAN)
  # Relative Velocity
  Y = np.linspace(-Y_LIM, Y_LIM, GRAN)
  # Create list to hold Z.
  Z = []

  # Keep track of maximum Z value
  Z_max = float('-inf')

  # For each x in X
  for x in X:
    # For each y in Y
    for y in Y:
      # Calculate warning distance given y (vrel) and vf
      wd = fn(y, vf)

      # Set z to np.nan if warning distance is impossible. Otherwise get MTTC
      if(wd<0): z = np.nan
      else: z = MTTC(x,y,wd)

      # Discard nan or negative vl case.
      # y (vrel) > vf => vf-vl > vf => -vl > 0 => vl < 0.
      # negative vl is out of our scope.
      if(y > vf): z = np.nan

      # Update maximum Z value only if z is not np.nan
      if(not np.isnan(z) and Z_max < z): Z_max = z
      # Place computed Z in the list.
      Z.append((x,y,z))
  
  # Return maximum Z, linspace X and Y, list Z
  return Z_max, *zip(*Z)

def run_calc():
  for fn in ALGORITHMS:
    target_dir = path.join("calculated", fn.__name__)

    # Create target dir if not exists;
    if not path.exists(target_dir): makedirs(target_dir)
    
    for vf in VFS:

      output = path.join(target_dir, str(vf) + ".csv")
      
      if path.exists(output): 
        print(f"CALC: {output} already exists skipping.")
        continue

      print(f"CALC: Calculating {fn.__name__} for vf={vf}")
      
      _, X, Y, Z = calc(fn, vf)
      

      print(f"CALC: Calculation finished. Saving...")
      save_points_csv(output , X, Y, Z)

if __name__ == "__main__": run_calc()
