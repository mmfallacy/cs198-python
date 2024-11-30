from sys import argv
from shutil import rmtree

logger = lambda *_: None

def includesAny(list, *rest):
    return any(el in list for el in rest)

def remove(path):
    logger(f"Purging {path} ...")
    return rmtree(path)

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

def main():
    _, *args = argv
    
    shouldRun = True
    shouldPurge = False

    if includesAny(args, "-r", "--purge-then-run"):
        shouldPurge = True

    if includesAny(args, "-p", "--purge-only"):
        shouldRun = False
        shouldPurge = True

    if includesAny(args, "-v", "--verbose"):
        global logger
        logger = print
        

    if "calc" in args:
        if shouldPurge: purge_calc()
        if shouldRun: calc()

    if "clean" in args:
        if shouldPurge: purge_cleaned()
        if shouldRun: clean()


if __name__ == "__main__": main()