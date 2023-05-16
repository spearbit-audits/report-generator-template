# A Markdown based template for writing audit reports
Forked from [Spearbit](https://github.com/spearbit-audits/report-generator-template).

## Introduction

This repository is meant to be a single-step solution to:

- Fetch all issues from a given repository
- Sort them by severity according to their labels
- Generate a single Markdown file with all issues sorted by descending severity
- Integrate that Markdown file into a LaTeX template
- Generate a PDF report with all the issues and other relevant information

## Directory structure

There are five directories:

- `source`: Contains the source Markdown files with all information needed for the report.
- `scripts`: Contains various scripts needed to convert files and generate the PDF.
- `templates`: The LaTeX files used as template for the final report.
- `output`: Output directory where the final report will be saved. All files can be safely erased.
- `working`: A directory where the temporary files will be stored. All files can be safely erased.

## Procedure

Check contents and **manually update** the following files in `source/`:

- `summary_information.conf`: Information to be replaced in the title page and the summary.
- `lead_auditors.md`: List of lead auditors who participated during the engagement.
- `assisting_auditors.md` : List of lead auditors who participated during the engagement.
- `about_cyfrin.md`: Cyfrin description.
- `disclaimer.md`: Information about the audit review process.
- `protocol_summary.md`: Information about the protocol.
- `additional_comments.md`: For extra information at the end of the report. It is commented by DEFAULT, please change if required.
- `appendix.md`: For extra information at the end of the report. It is commented by DEFAULT, please change if required.

All `.md` files can be formatted and will be converted to LaTeX by the scripts located in `scripts/`.

The `.conf` files store text-only information, and are replaced verbatim in the final report. This means all
formatting should be removed, as the template already contains formatting.

Once all information is filled in, running `python generate_report.py` will result in the creation
of the `report.pdf` file in `output`. The `report.md` and `severity_counts.conf` files will be automatically
generated from the issues in the repository. Temporary files will be created in `working`, and they can be safely
deleted after the report is generated.

By default, there are `.gitignore` rules in place to avoid tracking the following:

- Any file in `working` (Except its own `.gitignore`)
- Any file in `output` (Except its own `.gitignore`)
- `source/report.md` and `source/severity_counts.conf` as they are automatically generated
