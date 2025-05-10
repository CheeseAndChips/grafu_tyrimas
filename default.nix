{ pkgs ? import <nixpkgs> { }, ... }:

pkgs.stdenv.mkDerivation {
  name = "pdf";
  src = ./.;
  buildInputs = with pkgs; [
    # tex pkgs
    (texlive.combine {
      inherit (texlive)
        scheme-basic
        latexmk
        beamer
        pgf
        caption
        babel
        babel-lithuanian
        lithuanian
        metafont
        hyphen-lithuanian
        algorithms
        algorithmicx
        algpseudocodex;
    })
    zathura
    # python pkgs
    python312
  ] ++ (with pkgs.python312Packages; [
    ipython
    networkx
    matplotlib
    numpy
  ]);
  buildPhase = ''
    mkdir -p .cache/latex
    latexmk -interaction=nonstopmode -auxdir=.cache/latex -pdf main.tex
  '';
  installPhase = ''
    mkdir -p $out
    cp main.pdf $out
  '';
}
