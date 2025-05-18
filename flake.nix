{
  description = "LaTeX template";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        packages.py = pkgs.callPackage ./default.nix { };
        packages.tex_doc = pkgs.callPackage ./doc/default.nix { };
      });
}
