set shell := ["powershell.exe", "-c"]

clean:
    rm -r calculated\*

calc:
    uv run calc.py