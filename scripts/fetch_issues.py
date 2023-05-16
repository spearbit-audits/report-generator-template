import os
from dotenv import load_dotenv
from github import Github
from .helpers import get_issues, get_summary_information


load_dotenv()

# Load github repo information and personal access token
REPO = get_summary_information()['private_github']
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
github = Github(GITHUB_TOKEN)

def fetch_issues():
    # Get all issues from the repo. This will create `report.md` and `severity_counts.conf`
    print(f"Fetching issues from repository {REPO} ...")
    issues_obtained = get_issues(REPO, github)
    if(issues_obtained) > 0:
        print(f"Done. {issues_obtained} issues obtained.\n")
    else:
        print(f"Done. No issues obtained.\n")
