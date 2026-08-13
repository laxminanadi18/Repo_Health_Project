import os

from dotenv import load_dotenv
from crewai import Agent, LLM

from tool import (
    get_repo_metadata,
    get_github_issues,
    get_repo_activity
)

load_dotenv()

# ==========================================================
# OPENROUTER CONFIGURATION
# ==========================================================

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY found in .env file"
    )

llm = LLM(
    model="openai/gpt-4o-mini",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


# ==========================================================
# AGENT 1
# ==========================================================

repo_metadata_collector = Agent(
    role="Repo Metadata Collector",

    goal="""
    Collect accurate metadata about a GitHub repository,
    including stars, forks, issues, language, license,
    and recent activity.
    """,

    backstory="""
    You are an expert GitHub repository analyst.
    Your job is to collect repository information and
    explain its technical condition.
    """,

    tools=[
        get_repo_metadata,
        get_repo_activity
    ],

    llm=llm,
    verbose=True,
    allow_delegation=False
)


# ==========================================================
# AGENT 2
# ==========================================================

community_signal_researcher = Agent(
    role="Community Signal Researcher",

    goal="""
    Analyze the repository's community activity and
    determine whether it is actively maintained.
    """,

    backstory="""
    You are an open-source community analyst.
    You evaluate stars, forks, commits and repository
    activity to understand community health.
    """,

    tools=[
        get_repo_metadata,
        get_repo_activity
    ],

    llm=llm,
    verbose=True,
    allow_delegation=False
)


# ==========================================================
# AGENT 3
# ==========================================================

issue_triage_engineer = Agent(
    role="Issue Triage Engineer",

    goal="""
    Analyze open GitHub issues and identify bugs,
    risks, stale issues and maintenance problems.
    """,

    backstory="""
    You are an experienced software engineer specializing
    in GitHub issue analysis and prioritization.
    """,

    tools=[
        get_github_issues
    ],

    llm=llm,
    verbose=True,
    allow_delegation=False
)


# ==========================================================
# AGENT 4
# ==========================================================

health_report_writer = Agent(
    role="Health Report Writer",

    goal="""
    Combine repository information, community signals,
    and issue analysis into a clear final health report.
    """,

    backstory="""
    You are a technical writer specializing in
    open-source repository evaluation.
    """,

    llm=llm,
    verbose=True,
    allow_delegation=False
)