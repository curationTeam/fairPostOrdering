all: contentCuration.pdf contentCurationfullversion.pdf contentCurationPENCIL.pdf

#.ONESHELL:
contentCuration.pdf: $(shell find latex/ *)
	export TEXINPUTS=.:./latex//:; \
	pdflatex contentCuration.tex; \
	bibtex contentCuration.aux; \
	pdflatex contentCuration.tex; \
	pdflatex contentCuration.tex; \
	rm -rf contentCuration.aux contentCuration.log contentCuration.out contentCuration.toc contentCuration.lof contentCuration.lot contentCuration.bbl contentCuration.blg contentCuration.vtc

contentCurationPENCIL.pdf: $(shell find latex/ *)
	export TEXINPUTS=.:./latex//:; \
	pdflatex contentCurationPENCIL.tex; \
	bibtex contentCurationPENCIL.aux; \
	pdflatex contentCurationPENCIL.tex; \
	pdflatex contentCurationPENCIL.tex; \
	rm -rf contentCurationPENCIL.aux contentCurationPENCIL.log contentCurationPENCIL.out contentCurationPENCIL.toc contentCurationPENCIL.lof contentCurationPENCIL.lot contentCurationPENCIL.bbl contentCurationPENCIL.blg contentCurationPENCIL.vtc

contentCurationfullversion.pdf: $(shell find latex/ *)
	export TEXINPUTS=.:./latex//:; \
	pdflatex contentCurationfullversion.tex; \
	bibtex contentCurationfullversion.aux; \
	pdflatex contentCurationfullversion.tex; \
	pdflatex contentCurationfullversion.tex; \
	rm -rf contentCurationfullversion.aux contentCurationfullversion.log contentCurationfullversion.out contentCurationfullversion.toc contentCurationfullversion.lof contentCurationfullversion.lot contentCurationfullversion.bbl contentCurationfullversion.blg

clean:
	rm -rf *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.pdf *.vtc
