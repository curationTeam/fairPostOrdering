all: contentCuration.pdf

#.ONESHELL:
contentCuration.pdf: $(shell find latex/ *)
	if [ -e dot2tex ]; then rm -r dot2tex; fi
	mkdir dot2tex;
	export TEXINPUTS=.:./latex//:; \
	pdflatex --shell-escape contentCuration.tex; \
	bibtex contentCuration.aux; \
	pdflatex --shell-escape contentCuration.tex; \
	pdflatex --shell-escape contentCuration.tex; \
	rm -rf contentCuration.aux contentCuration.log contentCuration.out contentCuration.toc contentCuration.lof contentCuration.lot contentCuration.bbl contentCuration.blg
	-mv dot2tex/*.tex latex/figures/
	rm -r dot2tex

clean:
	rm -rf *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.pdf
