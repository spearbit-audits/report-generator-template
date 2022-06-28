"""
This script will allow code listings longer than N lines to be split in more than one page.
By default N = 40, but it should be changed for different font sizes, font styles, and so on.
"""

import helpers

N = 40

# Open the report file
report = helpers.get_file_contents("./working/report.tex")

begins = []
ends   = []

# Find the beginnings and endings of code listings
for i in range(len(report)):
    if report[i].find("\\begin{minted}") >= 0:
        begins.append(i)
    if report[i].find("\\end{minted}") >= 0:
        ends.append(i)

# There should be the same amount of elements in both lists
assert(len(begins) == len(ends))

# If a code listing takes more than N lines, allow it to break pages
for i in range(len(begins)):
    code_length = ends[i] - begins[i]
    if code_length >= N:
        report[begins[i]] = report[begins[i]].replace("\\begin{minted}[]", "\\begin{minted}[samepage=false]")

# Save the report file
helpers.save_file_contents("./working/report.tex", report)