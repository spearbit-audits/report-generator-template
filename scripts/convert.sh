#!/bin/bash

# This is called from parent directory by generate_report.py to CONVERT .md to .tex
# All paths are relative to ..

# pandoc with gfm flavored markdown seems to have issues regarding
# Skipping --from gfm here
# pandoc summary.md -o summary.tex
pandoc --filter ./scripts/pandoc-minted.py --from gfm ./source/additional_comments.md -o ./working/additional_comments.tex
pandoc --filter ./scripts/pandoc-minted.py --from gfm ./source/appendix.md -o ./working/appendix.tex
pandoc --filter ./scripts/pandoc-minted.py --from gfm ./source/introduction.md -o ./working/introduction.tex
pandoc --filter ./scripts/pandoc-minted.py --from gfm ./source/report.md -o ./working/report.tex
pandoc --filter ./scripts/pandoc-minted.py --from gfm ./source/repositories.md -o ./working/repositories.tex
pandoc --filter ./scripts/pandoc-minted.py --from gfm ./source/reviewers.md -o ./working/reviewers.tex
pandoc --filter ./scripts/pandoc-minted.py --from gfm ./source/copywriters.md -o ./working/copywriters.tex
pandoc --filter ./scripts/pandoc-minted.py --from gfm ./source/spearbit_description.md -o ./working/spearbit_description.tex

cp -r ./templates/* ./working/

# A temporary work around to have page breaks.
# FIXME figure out a way to natively do this.
sed -i 's/textbackslash clearpage/clearpage/g' ./working/report.tex
# On github CI, pandoc seems to be generating the following
sed -i 's/textbackslash{}clearpage/clearpage/g' ./working/report.tex

# Adding Needspaces before subsections and subsubsections
# Maybe 6cm is not the perfect value here, but it works good enough
sed -i 's/\\subsubsection/\\Needspace{6cm}\\subsubsection/g' ./working/report.tex
sed -i 's/\\subsection/\\Needspace{8cm}\\subsection/g' ./working/report.tex

# Allow long code listings to break pages
python3 ./scripts/code_listings.py