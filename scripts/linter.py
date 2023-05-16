import re


def lint(report, team_name, source_org, internal_org):

    # Check for link structures ( format [something](url) ) that don't start with http
    for line in report:
        pos = line.find("](")
        while pos != -1:
            # Check if the first 4 characters after the open-paren are "http"
            if line[pos+2:pos+6] != "http" and line[pos+2] != "#":
                position = report.index(line)
                print(f"Possible broken link at report.md line {position}: ")
                print(f"\t{line}")
            else:
                # Check for internal organization repo links
                start_link = pos + 2
                end_link = line.find(")", start_link)
                if end_link != -1:
                    link = line[start_link:end_link]
                    if re.search(internal_org, link, re.IGNORECASE):
                        # Replace internal organization link with source repo link (case-insensitive)
                        new_link = re.sub(internal_org, source_org, link, flags=re.IGNORECASE)
                        new_line = line[:start_link] + new_link + line[end_link:]
                        report[report.index(line)] = new_line
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
        if (
            (line.startswith("**Description:**") and len(line) < len("**Description:**") + 5) or
            (line.startswith("**Impact:**") and len(line) < len("**Impact:**") + 5) or
            (line.startswith("**Proof of Concept:**") and len(line) < len("**Proof of Concept:**") + 5) or
            (line.startswith("**Recommended Mitigation:**") and len(line) < len("**Recommended Mitigation:**") + 5) or
            (line.startswith("**Cyfrin:**") and len(line) < len("**Cyfrin:**") + 5) or
            (line.startswith("**" + team_name + ":**") and len(line) < len("**" + team_name + ":**") + 5)):
            
            # There might be more than one empty lines following the header, remove them
            while report[lineNumber + 1] == "":
                del report[lineNumber + 1]

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
