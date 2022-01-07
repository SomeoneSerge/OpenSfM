let
  pkgs = import <nixpkgs> { };
  opensfm = pkgs.python3Packages.callPackage ./release.nix { };
in
pkgs.mkShell {
  inputsFrom = [ opensfm ];
  dontUseSetuptoolsShellHook = true;
}
