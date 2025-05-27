LATEXMK:=latexmk
OUTDIR:=build
TEXFLAGS:=-Werror -pdf -output-directory="$(OUTDIR)"
TEXMAIN:=main.tex

.PHONY: pdf
pdf:
	mkdir -p $(OUTDIR)
	$(LATEXMK) $(TEXFLAGS) $(TEXMAIN)

.PHONY: watch
watch:
	mkdir -p $(OUTDIR)
	$(LATEXMK) $(TEXFLAGS) -interaction=nonstopmode -pvc $(TEXMAIN)

.PHONY: watch2
watch2:
	mkdir -p $(OUTDIR)
	$(LATEXMK) $(TEXFLAGS) -interaction=nonstopmode -pvc ./pytex/g1.tex
