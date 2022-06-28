import config
import scripts.helpers as helpers
from github import Github

# Load github repo information and personal token from config.py
REPO = config.REPO
github = Github(config.TOKEN)

# Get all issues from the repo. This will create `report.md` and `severity_counts.conf`
print(f"Fetching issues from repository {REPO} ...")
issues_obtained = helpers.get_issues(REPO, github)
if(issues_obtained) > 0:
    print(f"Done. {issues_obtained} issues obtained.\n")
else:
    print(f"Done. No issues obtained.\n")
    exit()