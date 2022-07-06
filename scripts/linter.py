def lint(report, reviewName):

    # Check for link structures ( format [something](url) ) that don't start with http
    for line in report:
        pos = line.find("](")
        while pos != -1:
            # Check if the first 4 characters after the open-paren are "http"
            if line[pos+2:pos+6] != "http" and line[pos+2] != "#":
                position = report.index(line)
                print(f"Possible broken link at report.md line {position}: ")
                print(f"\t{line}")
            pos = line.find("](", pos+1)

    # Check for raw links ("http" string not immediately preceded by a link structure)
    for line in report:
        pos = line.find("http")
        while pos != -1:
            # Check if the character to the left of "http" is an open-paren preceded by a close-bracket
            if line[pos-2:pos] != "](":
                position = report.index(line)
                print(f"Possible raw link at report.md line {position}: ")
                print(f"\t{line}")
            pos = line.find("http", pos+1)

    # Check for descriptions not starting in the same line as the headers
    lineNumber = 0
    for line in report:        
        # If there's a newline, merge the next line with the current one
        if ((line.startswith("**Severity:**") and len(line) < len("**Severity:**") + 5) or
            (line.startswith("**Context:**") and len(line) < len("**Context:**") + 5) or
            (line.startswith("**Description:**") and len(line) < len("**Description:**") + 5) or
            (line.startswith("**Spearbit:**") and len(line) < len("**Spearbit:**") + 5) or
            (line.startswith("**Recommendation:**") and len(line) < len("**Recommendation:**") + 5) or
            (line.startswith("**" + reviewName + ":**") and len(line) < len("**" + reviewName + ":**") + 5)):
            
           # There might be more than one empty lines following the header, remove them
            while lineNumber + 1 < len(report):
                if report[lineNumber + 1] != "": break
                del report[lineNumber + 1]
                

            # if next line is out of range then stop
            if lineNumber + 1 >= len(report): break

            nextLine = report[lineNumber + 1]
            
            # If it's a list, code or quote, don't merge
            if (not nextLine.lstrip().startswith("-") and 
                not nextLine.lstrip().startswith("1.") and 
                not nextLine.lstrip().startswith("```") and
                not nextLine.lstrip().startswith("#") and
                not nextLine.lstrip().startswith(">")): 
                
                report[lineNumber] = line + " " + nextLine.lstrip()
                del report[lineNumber + 1]

        lineNumber = lineNumber + 1

    return report