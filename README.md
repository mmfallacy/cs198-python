This repository holds the python scripts used for analysis and data visualization for the CS 198/199 thesis entitled "Comparative Analysis of Perceptual Forward Collision Warning Algorithms"

# Comparative Analysis of Perceptual Forward Collision Warning Algorithms

Rear-end collisions account for a significant portion of road accidents in Metro
Manila, highlighting the need for advanced driver assistance systems (ADAS) such
as Forward Collision Warning (FCW) systems. These systems aim to improve road
safety by providing timely alerts to drivers, helping prevent rear-end accidents.
This study evaluates three perceptual algorithms–Honda, Hirst & Graham, and
Bella & Russo–within a two-car following system.

A computational analysis was conducted using NumPy to examine trends in
Modified Time to Collision (MTTC) based on relative velocity and acceleration.
Additionally, an ad-hoc simulator is developed to evaluate the impact of these
algorithms on driver behavior and efficiency. Results indicate that while all three
algorithms contribute to improved safety, variations in warning distances affect
driver response patterns, with implications for both driving efficiency and envi-
ronmental impact.

This study emphasizes the need to balance safety and efficiency in FCW sys-
tems to minimize false positives, avoid overly conservative warnings, and reduce
unnecessary braking events that increase fuel consumption and carbon emissions.
Future research should explore real-world implementation and extend the analysis
to more complex traffic scenarios, such as vehicle platoons, to further refine FCW
performance.

## Overview

This repository contains code for the following elements of the study:
1. Theoretical calculations for MTTC estimates.
2. Simulation Data Pre-processing
3. Data visualization tools

Specifically, this python project utilizes `numpy` and `matplotlib` to run theoretical estimates of the three perceptual
warning algorithms: `honda`, `hirstgraham`, and `bellarusso`. These warning algorithms are implemented as warning distance 
models within the project, and is used by a `calc` function to estimate the MTTC of two-car following systems with varying 
relative velocities and acceleration. 
> Estimates are run for the following parameter values
> Relative Acceleration = X = dA = [-10, 10] m/s^2
> Relative Velocity = Y = dV = [-30, 30]  m/s
> Initial FV Velocity = vf = [5, 11, 27] m/s

Also, data exported as JSON from the ad-hoc simulator is processed into multiple per-metric CSV files. The simulation data
analyzed within the study is cached as part of this repository, located in `simulated/{algo}-vf={vf}.json`. The per-metric
CSV files are then extracted into `plots/{algo}-vf={vf}/{metric}.csv`.

Lastly, there are a few visualization scripts available which helped me generate the plots required for the analysis. These include:
- Metric value distribution for a specified vf on the algorithms: `show_zdist`
- Unified metric value distribution for a specified vf: `show_uzdist`
- Per-algorithm comparison of a metric across varying vf: `show_vf`
- Per-metric comparison of the algorithms on a specific vf: `cmp_metric`
- Per-vf comparison of the algorithms on a specific metric: `cmp_vf`
- Per-algorithm comparison of metrics on a specified vf: `cmp_algo`

Other scripts include:
- Bulk compute theoretical MTTC estimate for multiple dV, dA for a specified vf: `compute` 

## How to use:
### Prerequisites

<details>
<summary>- Running through `nix`</summary>
- Run `nix develop` to bootstrap a shell that includes `python310` and `uv`
> You can also use this devShell (`./nix/devShell.nix`) as your development environment!
</details>

<details>
<summary>- Other systems</summary>
- install Python >3.10 and [`astral-sh/uv`](https://docs.astral.sh/uv/getting-started/installation/)
</details>

### Running

Refer to `main.py` for valid commands and the arguments they require. Command invocations are always prefixed by 
`uv run main.py <args>` as we use `uv` to run the project's entry point.

> This repository underwent significant changes, hence the `v2` folder. Majority of the scripts used for the study is included
> here. To explicitly run version 2 of the scripts, add `-2` as an argument

Common flags:
- `-r` or `--purge-then-run`: Delete cached output, either cleaned CSV or image export of plots before running the script. *v1 only*
- `-p` or `--purge-only`: Delete cached output only, do not run script. *v1 only*
- `-v` or `--verbose`: Enable console logging. *v1 only*
- `-s` or `--show-plot`: For plot scripts, show matplotlib plot instead of only exporting an image.

Version 2 Commands:
- `calc` : Run `calc`.
- `clean` : Run `clean`.
- `cmp=vf metric=metric1 clamp=low,high`: Run `cmp_vf` for metric1. Clamp color mappings from low to high. Low and high can be set to none thru `clamp=,high` or `clamp=low,`
- `cmp=metric metrics=m1,m2,... vf=... clamp=...`: Run `cmp_metric` for m1,m2,... for a specified vf. Valid vf values are based on available per-metric CSV data. See above for clamp.
- `cmp=algo metrics=m1,m2,... vf=... clamp=...`: Run `cmp=algo` for m1,m2,... for a specified vf.
- `show=vf metric=... algos=algo1,algo2,.... clamp=...`: Run `show_vf` for a specified metric and algos. Valid algos are `honda`, `hirstgraham`, and `bellarusso`.  
- `show=zdist metrics=m1,m2,... vf=...`: Run `show_zdist` for specified metrics and vf.
- `show=uzdist metrics=... vf=...`: Run `show_uzdist` for specified metrics and vf.
- `compute algos=algo,... dV=float,... dA=float,... vf=` Run `compute` for specified algos, dV and dA. dV and dA are comma separated float values. vf is a single float value.

## Remarks and Recommendation

This project is created solely for the associated thesis study. This will be archived once the paper is completed. Feel free to raise issues for suggestions, but this repository will not be maintained. In case you wish to reuse this for a future related study, do not hesitate to fork it.

Due to time constraints, implementation is a bit unclean. Hence, I recommend that you continue the v2 refactor and push to remove the v1 scripts after. Also, consider to use proper command line argument parsers like `clap` for better argument and flag handling. 

## Acknowledgements
This project was developed as part of my undergraduate thesis under the [Scientific Computing Laboratory](https://scl.dcs.upd.edu.ph/) of the [Department of Computer Science](https://dcs.upd.edu.ph/), [College of Engineering](https://coe.upd.edu.ph/) at the [University of the Philippines Diliman](https://upd.edu.ph/).

Special thanks to [Dr. Jaymar B. Soriano](https://scl.dcs.upd.edu.ph/members/jbsoriano) for his guidance and support throughout the research.

Copyright (C) 2025, Michael M. <mlmonasterial@up.edu.ph>.
