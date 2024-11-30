from os import makedirs, path
from persist import load_simulated, save_points_csv


def save_cleaned_simulated(target, SIMULATION_TPS_RUN=120):
    filename, _ = path.basename(target).split(".")
    target_dir = path.join("cleaned", filename)    

    # Create if not yet created.
    makedirs(target_dir, exist_ok=True)
    

    X, Y, Z = load_simulated(target)
    
    for k, v in Z.items():
        out = path.join(target_dir, k + ".csv")
        save_points_csv(out, X, Y, v)
    
def run_clean():
    save_cleaned_simulated("simulated/honda.json")
    save_cleaned_simulated("simulated/hirstgraham.json")
    save_cleaned_simulated("simulated/onecar.json")
    save_cleaned_simulated("simulated/bellarusso.json")
    
if __name__ == "__main__": run_clean()