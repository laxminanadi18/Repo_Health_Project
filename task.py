
from crewai import Task

from agent import (
    repo_metadata_collector,
    community_signal_researcher,
    issue_triage_engineer,
    health_report_writer
)

# ==========================================================
# TASK 1
# ==========================================================

metadata_task = Task(
    description="""
    Analyze this GitHub repository:

    {repo_url}

    Collect:
    - Repository name
    - Description
    - Stars
    - Forks
    - Open issues
    - Programming language
    - License
    - Last update
    - Last push
    - Archived status
    """,

    expected_output="""
    A structured repository metadata report.
    """,

    agent=repo_metadata_collector
)


# ==========================================================
# TASK 2
# ==========================================================

community_task = Task(
    description="""
    Analyze the community health of:

    {repo_url}

    Examine:
    - Stars
    - Forks
    - Recent commits
    - Repository activity
    - Maintenance signals
    - Community interest
    """,

    expected_output="""
    A community health analysis containing positive
    signals, warning signals and overall assessment.
    """,

    agent=community_signal_researcher
)


# ==========================================================
# TASK 3
# ==========================================================

issue_task = Task(
    description="""
    Analyze the open issues of:

    {repo_url}

    Identify:
    - Critical issues
    - High priority issues
    - Medium priority issues
    - Low priority issues
    - Bugs
    - Stale issues
    - Maintenance risks
    """,

    expected_output="""
    A prioritized issue analysis with risks and
    recommendations.
    """,

    agent=issue_triage_engineer
)


# ==========================================================
# TASK 4
# ==========================================================

health_report_task = Task(
    description="""
    Create a final health report for:

    {repo_url}

    Use the repository analysis and issue analysis.

    Include:

    1. Repository Overview
    2. Repository Activity
    3. Community Health
    4. Issue Health
    5. Strengths
    6. Weaknesses
    7. Risks
    8. Recommendations
    9. Overall Health Score from 0 to 100
    """,

    expected_output="""
    A professional GitHub repository health report
    with an overall score from 0 to 100.
    """,

    agent=health_report_writer
)

