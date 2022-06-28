import subprocess
from sys import stderr
import scripts.helpers as helpers
import scripts.linter as linter

# Get static info from conf files
summary_data = helpers.get_summary_information()
severity_count_data = helpers.get_severity_counts()

# Project name taken from summary_information.conf, inserted in Title section -> title.tex file
REPLACE_TITLE = [["__PLACEHOLDER__PROJECT_NAME", summary_data['name']]]


# Information from summary_information.conf, inserted in Summary section -> summary.tex file
REPLACE_SUMMARY = [["__PLACEHOLDER__REVIEW_LENGTH", summary_data['review_length']],
                   ["__PLACEHOLDER__TEAM_NAME", summary_data['team_name']],
                   ["__PLACEHOLDER__TEAM_WEBSITE", summary_data['team_website']],
                   ["__PLACEHOLDER__PROJECT_NAME", summary_data['project_name']],
                   ["__PLACEHOLDER__PROJECT_WEBSITE", summary_data['project_website']],
                   ["__PLACEHOLDER__PROJECT_TYPE", summary_data['project_type']],
                   ["__PLACEHOLDER__REVIEW_TIMELINE", summary_data['review_timeline']],
                   ["__PLACEHOLDER__REVIEW_METHODS", summary_data['review_methods']],
                   ["__PLACEHOLDER__DOCUMENTATION", summary_data['documentation']],
                   ["__PLACEHOLDER__TESTING_COVERAGE", summary_data['testing_coverage']]]


# Severities count taken from severity_count.conf, inserted in Total Issues section -> summary.tex file
REPLACE_SEVERITIES = [["__PLACEHOLDER__ISSUE_CRITICAL_COUNT", severity_count_data['critical']],
                      ["__PLACEHOLDER__ISSUE_HIGH_COUNT", severity_count_data['high']],
                      ["__PLACEHOLDER__ISSUE_MEDIUM_COUNT", severity_count_data['medium']],
                      ["__PLACEHOLDER__ISSUE_LOW_COUNT", severity_count_data['low']],
                      ["__PLACEHOLDER__ISSUE_GAS_OPTIMIZATION_COUNT", severity_count_data['gas_optimization']], 
                      ["__PLACEHOLDER__ISSUE_INFORMATIONAL_COUNT" ,severity_count_data['informational']],
                      ["__PLACEHOLDER__ISSUE_TOTAL_COUNT", severity_count_data['total']]]



# Lint the report.md
print("Linting the report.md file ...")
report = helpers.get_file_contents(helpers.OUTPUT_REPORT)
report = linter.lint(report, summary_data['name'])
helpers.save_file_contents(helpers.OUTPUT_REPORT, report)
print(f"Done.\n")

# Convert all .md to .tex and save to working dir
print("Converting Markdown files to LaTeX ...")
with open("./working/conversion.log", "w") as log:
    subprocess.call("./scripts/convert.sh", stdout=log, stderr=log)
print(f"Done.\n")

# Process for title.tex: Get the file and replace placeholders. 
print("Replacing information in title.tex ...")
title = helpers.get_file_contents("./templates/title.tex")
title = helpers.replace_in_file_content(title, REPLACE_TITLE)
helpers.save_file_contents("./working/title.tex", title)
print(f"Done.\n")

# Process for summary.tex: Get the file and replace placeholders.
print("Replacing information in summary.tex ...")
summary = helpers.get_file_contents("./templates/summary.tex")
summary = helpers.replace_in_file_content(summary, REPLACE_SUMMARY)
summary = helpers.replace_in_file_content(summary, REPLACE_SEVERITIES)
helpers.save_file_contents("./working/summary.tex", summary)
print(f"Done.\n")

# Generate PDF in output folder
print("Generating report PDF file ...")
with open("./working/generation.log", "w") as log:
    subprocess.call("./scripts/generate.sh", stdout=log, stderr=log)
print(f"\nAll tasks completed. Report should be in the 'output' folder.")
print(f"If it wasn't generated, check 'working/conversion.log' and 'working/generation.log'.")