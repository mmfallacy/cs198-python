
from os import makedirs, path
from src.persist import load_simulated, save_points_csv
from src.v2.const import ALGORITHMS, VFS

def run_clean():
  for fn in ALGORITHMS:
    for vf in VFS:
      filename = f"{fn.__name__}-vf={vf}"
      target = path.join("simulated", filename + ".json")    
      
      output_dir = path.join("plots", filename)

      # Create if not yet created.
      makedirs(output_dir, exist_ok=True)
      
      X, Y, Z = load_simulated(target)
      
      for k, v in Z.items():
          out = path.join(output_dir, k + ".csv")
          save_points_csv(out, X, Y, v)

    
      