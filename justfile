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
purge: purge-calc purge-cleaned

calc:
    uv run calc.py

clean:
    uv run clean.py

[group('repeat')]
recalc: purge-calc calc

[group('repeat')]
reclean: purge-cleaned clean

[confirm]
reall: purge calc clean