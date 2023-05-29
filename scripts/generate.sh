#!/bin/bash

# This is called from parent directory by generate_report.py
# All paths are relative to ..

cd working

pdflatex -shell-escape -interaction nonstopmode main.tex
# Running it a second time to generate references
pdflatex -shell-escape -interaction nonstopmode main.tex

cp main.pdf ../output/report.pdf