{ pkgs, ... }:
let
  python = pkgs.python310Full;
in
pkgs.mkShell {
  packages = [
    python
    pkgs.uv
  ];

  env =
    {
      UV_PYTHON_DOWNLOADS = "never";
      UV_PYTHON = python.interpreter;
    }
    // pkgs.lib.optionalAttrs pkgs.stdenv.isLinux {
      LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath pkgs.pythonManylinuxPackages.manylinux1;
      # Use Tkinter backend for linux
      MPLBACKEND = "TkAgg";
    };

  shellHook = ''
    # undo dependency propagation from nixpkgs 
    # [1](https://nixos.org/manual/nixpkgs/stable/#setup-hook-python) 
    # [2](https://github.com/NixOS/nixpkgs/blob/b841c624fda46a8e28a007684eb56d407fb246b8/pkgs/development/interpreters/python/setup-hook.sh)
    unset PYTHONPATH
  '';
}
