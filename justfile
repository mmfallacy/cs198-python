set shell := ["powershell.exe", "-c"]

default:
    @just --list

[confirm]
[group('purge')]
purge-calc:
    rm -r calculated\*
    
[confirm]
[group('purge')]
purge-cleaned:
    rm -r cleaned\*

[confirm]
[group('purge')]
purge-assets-cmpcalc:
    rm -r assets\calculated\*

[confirm]
[group('purge')]
purge-assets: purge-assets-cmpcalc

[confirm]
[group('purge')]
purge: purge-calc purge-cleaned purge-assets

calc:
    uv run calc.py

clean:
    uv run clean.py

compare-vf: calc
    uv run compare_per_vf.py

[group('repeat')]
recalc: purge-calc calc

[group('repeat')]
reclean: purge-cleaned clean

[confirm]
reall: purge calc clean