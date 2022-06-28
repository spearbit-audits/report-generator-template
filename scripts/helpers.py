import configparser
from os.path import exists as check_file
import re

# Define file paths
OUTPUT_PATH = './source/'
OUTPUT_REPORT = OUTPUT_PATH + 'report.md'
SEVERITY_COUNTS = OUTPUT_PATH + 'severity_counts.conf'
SUMMARY_INFORMATION = OUTPUT_PATH + 'summary_information.conf'

# Possible severity labels from github issues
SEVERITY_LABELS = ['Severity: Critical Risk', 'Severity: High Risk', 'Severity: Medium Risk', 'Severity: Low Risk', 'Severity: Gas Optimization', 'Severity: Informational']

# Little helper to get issues with a certain label
def get_issue_count(dict, label):
    try:
        count = len(dict[label])
    except:
        count = 0
    finally:
        return count


def title_to_link(title):
    """
    title_to_link converts an issue title to an internal link

    see https://stackoverflow.com/questions/2822089/how-to-link-to-part-of-the-same-document-in-markdown
    """
    # all non-alphanumeric characters should be removed, and spaces replaced with hyphens
    pattern = re.compile('[^a-zA-Z0-9 ]')
    link_anchor = re.sub(pattern, '', title.lower()).replace(" ", "-")
    full_link = f"[*{title}*](#{link_anchor})"
    return full_link


def replace_internal_links(issues, issues_by_number):
    """
    replace_internal_links Replaces github's issue links (#xx) with internal document links
    """
    for label in issues:
        for issue in issues[label]:
            # Find every occurrence of ' #' followed by a number of up to 4 digits
            p = re.findall(" #\d{1,4}", issue)
            if p:
                for match in p:
                    # Extract the issue number to link to
                    number = int(match[2:])
                    # Create the internal link to the issue
                    try:
                        # The space below is needed, because the regexp match includes the space. Otherwise it would be lost.
                        target = " " + title_to_link(issues_by_number[number])
                    except KeyError as e:
                        # Common error occurs when there is a '#' in the issue description i.e "Fix implemented in #2"
                        print(f"Issue '{issue}' references issue #{number} but there is no such issue. KeyError {e}. Make sure there aren't any `#`s written in the Issue description.")
                        exit(1)
                    # Replace with link
                    index = issues[label].index(issue)
                    new_issue = issues[label][index].replace(match, target)
                    issues[label][index] = new_issue
                    issue = new_issue
    return issues


def get_issues(repository, github):
    """
    get_issues Reads all the issues from the repo configured in config.py and generates a .md file.

    A simple script that collects issues from a repo and generate a markdown
    file (report.md). A personal access token will need to be configured. Also the repo name will
    need to be provided. Add these in `config.py`.

    This code was mostly copied from the compile-issues repo, with some minor tweaks. 
    I don't take credit for it, but I don't know who the original author is.
    """

    # The dictionary where the issues will be stored, by severity.
    issue_dict : dict[str, list[str]] = {}

    # Dictionary for issues by github number, to replace #xx links
    issues_by_number : dict[int, str] = {}

    # TODO catch get_repo() 404 errors and produce a gentle suggestion on what's wrong.
    # "GitHub's REST API v3 considers every pull request an issue"--need to filter them out.
    try:
        for issue in github.get_repo(repository).get_issues():
            if issue.state == 'open' and issue.pull_request is None:
                # get issue number and title for replacing links
                issues_by_number[issue.number] = issue.title

                # filter issue labels for only severity labels
                severity_labels_in_issue = [label.name for label in issue.labels if label.name in SEVERITY_LABELS]

                assert len(severity_labels_in_issue) == 1, f"Issue {issue.html_url} has more than one (or no) severity label."
                label = issue.labels[0].name
                if label not in issue_dict:
                    issue_dict[label] = []
                issue_dict[label].append(f"\n\n### {issue.title}\n\n{issue.body}\n")
    except Exception as e:
        print(f"I couldn't fetch the issues from repository {repository}.\nError:{e} \n")
        return 0

    issue_dict = replace_internal_links(issue_dict, issues_by_number)

    with open(OUTPUT_REPORT, "w") as report:
        for label in SEVERITY_LABELS:
            # Do nothing if there are no issues with this label
            if get_issue_count(issue_dict, label) == 0:
                continue

            report.write(f"\n\n## {label[10:]}\n")
            for content in issue_dict[label]:
                report.write(content.replace("\r\n", "\n"))

    total_count = 0
    with open(SEVERITY_COUNTS, "w") as counts_file:
        counts_file.write('[counts]' + '\n')
        for label in SEVERITY_LABELS:
            variable_name = label[10:].lower().replace(" risk", "").replace(" ", "_") + " = "
            count = get_issue_count(issue_dict, label)
            counts_file.write(variable_name + str(count) + '\n')
            total_count += count
        counts_file.write('total = ' + str(total_count) + '\n')

    return total_count

def get_file_contents(filename):
    """
    get_file_contents Reads the contents of a file and returns a list where every element is a line in the file. Newlines are stripped.

    :param filename: Name of the file to read
    :return: List of all lines in the file, with the newline character removed.
    """ 

    if not check_file(filename):
        print("I can't find the requested file: '" + filename + "'. Make sure it exists.")
        exit(1)

    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    
    return lines
    

def save_file_contents(filename, contents):
    """
    save_file_contents Saves a list to disk, one element per line

    :param filename: Name of the file to write to
    :param contents: List containing the information to save
    """ 

    with open(filename, "w") as file:
        file.write("\n".join(contents))


def replace_in_file_content(file_content, replacement):
    """
    replace_in_file_content Finds text in every element of a list and replaces it as required.

    :param file_content: List containing the string elements to be replaced
    :param replacement: A list of two-element lists containing text to replace, and what to replace it with.
    :return: Input with text replaced.
    """ 

    lines = []

    for line in file_content:
        if line.find("__PLACEHOLDER__") >= 0:
            for r in replacement:
                line = line.replace(r[0], r[1])
        lines.append(line)
    
    return lines


def get_summary_information():
    """
    get_summary_information Retrieves all strings needed to fill summary.tex and title.tex

    :return: A dictionary with all strings needed to replace in the tex files.
    """ 

    if not check_file(SUMMARY_INFORMATION):
        print("I can't find summary_information.conf. Make sure it is in the source folder.")
        exit(1)
    
    config = configparser.ConfigParser()
    config.read(SUMMARY_INFORMATION)
    
    summary : dict[str, str] = {}
    
    # Copy to dictionary
    for key, value in config['summary'].items():
        summary[key] = value
    
    return summary


def get_severity_counts():
    """
    get_severity_counts Retrieves all information needed to fill the amount of findings in summary.tex

    :return: A dictionary with all severity counts.
    """ 

    if not check_file(SEVERITY_COUNTS):
        print("I can't find severity_counts.conf. Make sure it is in the source folder.")
        exit(1)

    config = configparser.ConfigParser()
    config.read(SEVERITY_COUNTS)
    
    counts : dict[str, int] = {}
    
    for key, value in config['counts'].items():
        counts[key] = value

    # If integers are needed instead of strings:
    #for key, value in config['counts'].items():
    #    try:
    #        counts[key] = int(value)
    #    except ValueError:
    #        counts[key] = 0
    
    return counts
