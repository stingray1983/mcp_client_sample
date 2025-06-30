from github import Github
import os

def get_open_issues(repo_owner, repo_name):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        print("Please set it to your GitHub Personal Access Token.")
        return []

    g = Github(token)
    repo = g.get_user(repo_owner).get_repo(repo_name)
    
    open_issues = []
    for issue in repo.get_issues(state="open"):
        open_issues.append({
            "number": issue.number,
            "title": issue.title,
            "body": issue.body,
            "html_url": issue.html_url,
            "labels": [label.name for label in issue.labels]
        })
    return open_issues

if __name__ == "__main__":
    owner = "stingray1983"
    repo_name = "mcp_client_sample"
    issues = get_open_issues(owner, repo_name)
    if issues:
        print(f"Found {len(issues)} open issues:")
        for issue in issues:
            print(f'Issue #{issue["number"]}: {issue["title"]}')
            print(f'  URL: {issue["html_url"]}')
            if issue["labels"]:
                print(f'  Labels: {", ".join(issue["labels"])}')
            print(f"""  Body:
{issue["body"]}
---
""")
    else:
        print("No open issues found.")

