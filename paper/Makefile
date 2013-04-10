LATEX = pdflatex
BIBTEX = bibtex

all: paper

paper: main.tex
	$(LATEX) main.tex
	$(BIBTEX) main.aux
	$(LATEX) main.tex

clean:
	rm *.aux *.log *.pdf *.bbl *.blg
