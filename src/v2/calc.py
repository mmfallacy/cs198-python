
from os import makedirs, path
from src.calc import calc
from src.const import ALGORITHMS
from src.v2.const import VFS

from src.persist import save_points_csv


def run_calc():
  for fn in ALGORITHMS:
    for vf in VFS:

      target_dir = path.join("plots", f"{fn.__name__}-vf={vf}")

      # Create target dir if not exists;
      if not path.exists(target_dir): makedirs(target_dir)
    

      output = path.join(target_dir, f"calculated.csv")
      
      if path.exists(output): 
        print(f"CALC: {output} already exists skipping.")
        continue

      print(f"CALC: Calculating {fn.__name__} for vf={vf}")
      
      _, X, Y, Z = calc(fn, vf)
      

      print(f"CALC: Calculation finished. Saving...")
      save_points_csv(output , X, Y, Z)

if __name__ == "__main__": run_calc()
