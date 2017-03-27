all: thesis
cleanall: clean-all

clean-all: clean
	rm -f *.ps *.pdf
clean:
	rm -f *.aux *.log *.dvi

thesis: thesis.pdf
knizka-web: knizka-web.pdf

thesis.dvi: %.dvi: $(wildcard *.tex)
		vlna -l -r $^
		cslatex thesis.tex
		cslatex thesis.tex
		cslatex thesis.tex
thesis.pdf: thesis.dvi
		dvipdf thesis.dvi
.PHONY: clean-all cleanall clean all
FORCE:
