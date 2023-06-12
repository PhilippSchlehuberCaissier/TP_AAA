## Start of the configuration
## You can also overide these variables with make VAR=VALUE (https://www.gnu.org/software/make/manual/html_node/Overriding.html#Overriding)

DEPLOYMENT_DESTINATION = /lrde/perso/${USER}/www    # Where to deploy html + extra files
DEPLOYMENT_EXTRA_FILES =                         	# Deployment extra files ("static" directory is deployed by default)
PANDOC_EXE = pandoc                              	# Pandoc binary
PANDOC_ARGS = -H header.inc.tex	--pdf-engine=lualatex   # Pandoc extra arguments

SUBDIRS = figs                                      # Space separated list of directories for which we need to run "MAKE" recursively


## End of the configuration
############################################################################################################################################


MD_FILES := $(shell find . -name '*.md')
MD_FILES := $(filter-out ./README.md, $(MD_FILES))
SLIDES_PDF_FILES := ${MD_FILES:%.md=%.slides.pdf}
NOTES_PDF_FILES := ${MD_FILES:%.md=%.notes.pdf}
HANDOUT_PDF_FILES := ${MD_FILES:%.md=%.handout.pdf} 

all: slides

slides: recurse
	$(MAKE) ${SLIDES_PDF_FILES}

notes: export PANDOC_ARGS += -V classoption=notes,smaller
notes: recurse
	$(MAKE) -e ${NOTES_PDF_FILES}

recurse:
	for subdir in ${SUBDIRS}; do $(MAKE) -C "$${subdir}"; done


handout: export PANDOC_ARGS += -V handout -V aspectratio=32
handout: recurse
	$(MAKE)	-e ${HANDOUT_PDF_FILES}
	@echo "Generating 2x2 handhouts"
	@pdfjam --batch --nup 2x2 --landscape --suffix nup ${HANDOUT_PDF_FILES}
	@for f in $(basename ${HANDOUT_PDF_FILES}); do mv $$f-nup.pdf $$f.pdf; done

clean:
	rm -f ${SLIDES_PDF_FILES} ${HANDOUT_PDF_FILES}


final: ${SLIDES_PDF_FILES} ${HANDOUT_PDF_FILES}
	@echo "Compressing PDFs"
	parallel ghostscript -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile={.}.final.pdf {} ::: $^
	@for f in $(basename $^); do mv $$f.final.pdf $$f.pdf; done


DEPLOYMENT_FILES = ${SLIDES_PDF_FILES} ${HANDOUT_PDF_FILES}

deploy: final
	rsync -maR ${DEPLOYMENT_FILES} ${DEPLOYMENT_DESTINATION}

%.slides.pdf: %.md
	${PANDOC_EXE} ${PANDOC_ARGS} --from=markdown --to=beamer header.yaml $< -o $@

%.handout.pdf: %.md
	${PANDOC_EXE} ${PANDOC_ARGS} --from=markdown --to=beamer header.yaml $< -o $@

%.notes.pdf: %.md
	${PANDOC_EXE} ${PANDOC_ARGS} --from=markdown --to=beamer header.yaml $< -o $@


%.final.pdf: %.pdf
	ghostscript -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$@ $<
