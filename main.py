from sys import argv
from shutil import rmtree
from os import path

logger = lambda *_: None

def includesAny(list, *rest):
    return any(el in list for el in rest)

def remove(dir):
    logger(f"Purging {dir} ...")
    if not path.exists(dir):  return logger(f"Purging failed as directory does not exist. Skipping...")
    return rmtree(dir)

# Commads:
# Purges
def purge_calc():
    return remove("./calculated")

def purge_cleaned():
    return remove("./cleaned")

def purge_cmp_per_vf():
    return remove("./assets/vf")

def purge_cmp_per_metric():
    return remove("./assets/metric")

def purge_cmp_sim():
    return remove("./assets/sim")

# Runs
def calc():
    from src.calc import run_calc
    logger("Running MTTC calculations...")
    return run_calc()

def clean():
    from src.clean import run_clean
    logger("Cleaning simulated json values into csvs of points...")
    return run_clean()

def cmp_per_vf(show=False):
    from src.compare_per_vf import run_cmp_per_vf
    logger("Plotting data for comparison per vf...")
    return run_cmp_per_vf(show)
    
def cmp_per_metric(show=False):
    from src.compare_per_metric import run_cmp_per_metric
    logger("Plotting data for comparison per metric...")
    return run_cmp_per_metric(show)

def cmp_sim(show=False):
    from src.compare_simulated import run_cmp_sim
    logger("Plotting data for comparison of simulated algorithms...")
    return run_cmp_sim(show)

def main():
    _, *args = argv
    
    shouldRun = True
    shouldPurge = False
    shouldPlot = False

    if includesAny(args, "-r", "--purge-then-run"):
        shouldPurge = True

    if includesAny(args, "-p", "--purge-only"):
        shouldRun = False
        shouldPurge = True

    if includesAny(args, "-v", "--verbose"):
        global logger
        logger = print
        
    if includesAny(args, "-s", "--show-plot"):
        shouldPlot = True

    if "calc" in args:
        if shouldPurge: purge_calc()
        if shouldRun: calc()

    if "clean" in args:
        if shouldPurge: purge_cleaned()
        if shouldRun: clean()
        
    if "cmp=vf" in args:
        if shouldPurge: purge_cmp_per_vf()
        if shouldRun: cmp_per_vf(show=shouldPlot)
    
    if "cmp=metric" in args:
        if shouldPurge: purge_cmp_per_metric()
        if shouldRun: cmp_per_metric(show=shouldPlot)
        
    if "cmp=sim" in args:
        if shouldPurge: purge_cmp_sim()
        if shouldRun: cmp_sim(show=shouldPlot)


if __name__ == "__main__": main()