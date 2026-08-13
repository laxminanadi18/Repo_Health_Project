import requests
from crewai.tools import tool


@tool("GitHub Repository Metadata")
def get_repo_metadata(repo_url: str) -> str:
    """Fetch metadata from a GitHub repository."""

    try:
        parts = repo_url.rstrip("/").split("/")

        if len(parts) < 2:
            return "Invalid GitHub repository URL."

        owner = parts[-2]
        repo = parts[-1]

        url = f"https://api.github.com/repos/{owner}/{repo}"

        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            return f"GitHub API error: {response.status_code}"

        data = response.json()

        license_info = data.get("license")

        if license_info:
            license_name = license_info.get("name")
        else:
            license_name = "None"

        return f"""
Repository: {data.get("full_name")}
Description: {data.get("description")}
Stars: {data.get("stargazers_count")}
Forks: {data.get("forks_count")}
Open Issues: {data.get("open_issues_count")}
Language: {data.get("language")}
License: {license_name}
Created: {data.get("created_at")}
Last Updated: {data.get("updated_at")}
Last Push: {data.get("pushed_at")}
Default Branch: {data.get("default_branch")}
Archived: {data.get("archived")}
"""

    except Exception as e:
        return f"Error collecting repository metadata: {e}"


@tool("GitHub Issues")
def get_github_issues(repo_url: str) -> str:
    """Fetch open GitHub issues."""

    try:
        parts = repo_url.rstrip("/").split("/")

        if len(parts) < 2:
            return "Invalid GitHub repository URL."

        owner = parts[-2]
        repo = parts[-1]

        url = f"https://api.github.com/repos/{owner}/{repo}/issues"

        response = requests.get(
            url,
            params={
                "state": "open",
                "per_page": 20
            },
            timeout=15
        )

        if response.status_code != 200:
            return f"GitHub API error: {response.status_code}"

        issues = response.json()

        if not issues:
            return "No open issues found."

        result = "OPEN GITHUB ISSUES\n\n"

        for issue in issues:

            # Ignore pull requests
            if "pull_request" in issue:
                continue

            labels = [
                label["name"]
                for label in issue.get("labels", [])
            ]

            result += f"""
Issue #{issue.get("number")}
Title: {issue.get("title")}
Labels: {", ".join(labels) if labels else "None"}
Created: {issue.get("created_at")}
Updated: {issue.get("updated_at")}
Comments: {issue.get("comments")}
URL: {issue.get("html_url")}

"""

        return result

    except Exception as e:
        return f"Error collecting issues: {e}"


@tool("GitHub Repository Activity")
def get_repo_activity(repo_url: str) -> str:
    """Fetch recent repository commits."""

    try:
        parts = repo_url.rstrip("/").split("/")

        if len(parts) < 2:
            return "Invalid GitHub repository URL."

        owner = parts[-2]
        repo = parts[-1]

        url = f"https://api.github.com/repos/{owner}/{repo}/commits"

        response = requests.get(
            url,
            params={"per_page": 10},
            timeout=15
        )

        if response.status_code != 200:
            return f"GitHub API error: {response.status_code}"

        commits = response.json()

        if not commits:
            return "No recent commits found."

        result = "RECENT COMMITS\n\n"

        for commit in commits:

            commit_data = commit.get("commit", {})

            message = commit_data.get(
                "message",
                "No message"
            ).split("\n")[0]

            author_data = commit_data.get(
                "author",
                {}
            )

            author = author_data.get(
                "name",
                "Unknown"
            )

            date = author_data.get(
                "date",
                "Unknown"
            )

            result += f"""
Commit: {message}
Author: {author}
Date: {date}

"""

        return result

    except Exception as e:
        return f"Error collecting repository activity: {e}"