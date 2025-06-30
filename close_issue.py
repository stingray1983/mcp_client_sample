from github import Github
import os

repo_owner = "stingray1983"
repo_name = "mcp_client_sample"
issue_number = 1

token = os.getenv("GITHUB_TOKEN")
if not token:
    print("Error: GITHUB_TOKEN environment variable not set.")
else:
    g = Github(token)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    issue = repo.get_issue(number=issue_number)
    issue.edit(state="closed")
    print(f"Successfully closed issue #{issue_number} in {repo_owner}/{repo_name}.")
