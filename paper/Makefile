LATEX = pdflatex
BIBTEX = bibtex

all: acm ieee

acm: main-acm.tex
	$(LATEX) main-acm.tex
	$(BIBTEX) main-acm.aux
	$(LATEX) main-acm.tex

ieee: main-ieee.tex
	$(LATEX) main-ieee.tex 
	$(BIBTEX) main-ieee.aux
	$(LATEX) main-ieee.tex

clean:
	rm *.aux *.log *.pdf *.bbl *.blg
