
from src.lib import MTTC, bellarusso, hirstgraham, honda


def compute(dA, dV, vf, fn): 
  wd = fn(dV, vf)
  if(wd<0): return print("wd is negative!")
  
  z = MTTC(dA, dV, wd)
  
  print(z)

def run_compute(dA,dV,vf,algos):
  for algo in algos:
    match algo:
      case "honda":
        fn = honda
      case "hirstgraham":
        fn = hirstgraham
      case "bellarusso":
        fn = bellarusso
      case _: 
        raise RuntimeError("Unsupported algorithm")
    
    compute(float(dA), float(dV), float(vf), fn)