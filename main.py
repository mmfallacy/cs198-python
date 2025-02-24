from sys import argv
from shutil import rmtree
from os import path
from src.const import ALGORITHMS

logger = lambda *_: None

def includesAny(list, *rest):
    return any(el in list for el in rest)

def meets(*rest):
    return all(rest)

def remove(dir):
    logger(f"Purging {dir} ...")
    if not path.exists(dir):  return logger(f"Purging failed as directory does not exist. Skipping...")
    return rmtree(dir)

def getInput(args, key, default=None):
    match  = list(filter(lambda arg: f"{key}=" in arg, args))
    if(len(match) < 1): 
        if default is None: raise RuntimeError(f"Missing argument {key}!")
        else: return default
    _, value = match[0].split("=")
    return value

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

    v2Flag = includesAny(args, "--v2", "--new", "-2")
    if meets(v2Flag, includesAny(args, "calc")):
        from src.v2.calc import run_calc
        return run_calc()

    if meets(v2Flag, includesAny(args, "clean")):
        from src.v2.clean import run_clean
        return run_clean()
 
    # Process clamp
    # Clamp is lowest,highest (e.g. 0,7 or ,7 if lowest is None)
    clamp = getInput(args, "clamp", default=",")
    clamp = tuple(int(i) if i.isnumeric() else None for i in clamp.split(","))
    assert type(clamp) is tuple and len(clamp) == 2
    assert clamp[0] is None or type(clamp[0]) is int
    assert clamp[1] is None or type(clamp[1]) is int

    if meets(v2Flag, includesAny(args, "cmp=vf")):
        # Process metric input
        # Metric can be any in [ave_headway, ave_vx, calculated, first_mttc, tick]
        metric = getInput(args, "metric")
        assert metric in ["ave_headway", "ave_vx", "calculated", "first_mttc", "tick", "seconds"]
        
        from src.v2.compare_per_vf import run_cmp_per_vf
        return run_cmp_per_vf(metric, clamp, showPlot=shouldPlot)
    
    if meets(v2Flag, includesAny(args, "cmp=metric")):
        # Process metrics input
        metrics = getInput(args, "metrics")
        metrics = metrics.split(",")
        for metric in metrics:
            assert metric in ["ave_headway", "ave_vx", "calculated", "first_mttc", "tick", "seconds"]
        
        # Process vf input
        vf = getInput(args, "vf")
        
        from src.v2.compare_per_metric import run_cmp_per_metric 
        return run_cmp_per_metric(vf, metrics, clamp, showPlot=shouldPlot)

    if meets(v2Flag, includesAny(args, "cmp=algo")):
        # Process metrics input
        metrics = getInput(args, "metrics")
        metrics = metrics.split(",")
        for metric in metrics:
            # Only calculated and first_mttc are similar metrics values.
            assert metric in ["calculated", "first_mttc"]
        
        # Process vf input
        vf = getInput(args, "vf")
        
        from src.v2.compare_per_algo import run_cmp_per_algo
        return run_cmp_per_algo(vf, metrics, clamp, showPlot=shouldPlot)
        
    if meets(v2Flag, includesAny(args, "show=vf")):
        # Process metric input
        metric = getInput(args, "metric")
        assert metric in ["ave_headway", "ave_vx", "calculated", "first_mttc", "tick", "seconds"]

        # Process algos input
        algos = getInput(args, "algos")
        algos = algos.split(",")
        for algo in algos:
            assert algo in map(lambda fn: fn.__name__,ALGORITHMS)
         
        from src.v2.show_vf import run_show_vf
        return run_show_vf(algos, metric, clamp, showPlot=shouldPlot)

    if meets(v2Flag, includesAny(args, "show=zdist")):
        # Process metrics input
        metrics = getInput(args, "metrics")
        metrics = metrics.split(",")
        for metric in metrics:
            assert metric in ["ave_headway", "ave_vx", "calculated", "first_mttc", "tick", "seconds"]
        
        # Process vf input
        vf = getInput(args, "vf")
        
        from src.v2.show_zdist import run_show_zdist
        return run_show_zdist(vf, metrics, showPlot=shouldPlot)

    if meets(v2Flag, includesAny(args, "show=zdist")):
        # Process metrics input
        metrics = getInput(args, "metrics")
        metrics = metrics.split(",")
        for metric in metrics:
            assert metric in ["ave_headway", "ave_vx", "calculated", "first_mttc", "tick", "seconds"]
        
        # Process vf input
        vf = getInput(args, "vf")
        
        from src.v2.show_uzdist import run_show_zdist
        return run_show_zdist(vf, metrics, showPlot=shouldPlot)


    if includesAny(args, "calc", "all"):
        if shouldPurge: purge_calc()
        if shouldRun: calc()

    if includesAny(args, "clean", "all"):
        if shouldPurge: purge_cleaned()
        if shouldRun: clean()
        
 
    if includesAny(args, "cmp=vf", "all", "cmp"):
        if shouldPurge: purge_cmp_per_vf()
        if shouldRun: cmp_per_vf(show=shouldPlot)
    
    if includesAny(args, "cmp=metric", "all", "cmp"):
        if shouldPurge: purge_cmp_per_metric()
        if shouldRun: cmp_per_metric(show=shouldPlot)
        
    if includesAny(args, "cmp=sim", "all", "cmp"):
        if shouldPurge: purge_cmp_sim()
        if shouldRun: cmp_sim(show=shouldPlot)
        


if __name__ == "__main__": main()
