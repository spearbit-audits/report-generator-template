#!/bin/bash

# This is called from parent directory by generate_report.py
# All paths are relative to ..

cd working

docker run --rm -i --user="$(id -u):$(id -g)" --net=none -v "$PWD":/data blang/latex:ubuntu pdflatex -shell-escape -interaction nonstopmode main.tex
# Running it a second time to generate references
docker run --rm -i --user="$(id -u):$(id -g)" --net=none -v "$PWD":/data blang/latex:ubuntu pdflatex -shell-escape -interaction nonstopmode main.tex

cp /data/main.pdf ../output/report.pdf