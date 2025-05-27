{ pkgs ? import <nixpkgs> { }, ... }:

pkgs.stdenv.mkDerivation {
  name = "pdf";
  src = ./.;
  buildInputs = with pkgs; [
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
        makecell
        framed
        gnuplottex
        moreverb
        catchfile
        psfrag
        pst-pdf
        auto-pst-pdf
        pstricks
        luatex85
        environ
        preview
        algorithms
        algorithmicx
        algpseudocodex
        listings
        titling
        tocbibind
        geometry
        natbib
        amsmath
        wrapfig
        float
        hyperref
        underscore;
    })
    zathura
    # python pkgs
    python312
  ] ++ (with pkgs.python312Packages; [
    ipython
    networkx
    matplotlib
    numpy
    tqdm
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
