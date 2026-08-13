import os
import streamlit as st

from dotenv import load_dotenv
from crewai import Crew, Process

from agent import (
    repo_metadata_collector,
    community_signal_researcher,
    issue_triage_engineer,
    health_report_writer
)

from task import (
    metadata_task,
    community_task,
    issue_task,
    health_report_task
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* =========================================================
   MAIN APP BACKGROUND
   ========================================================= */

.stApp {
    background: linear-gradient(
        135deg,
        #F8FAFC 0%,
        #E2E8F0 50%,
        #F1F5F9 100%
    );
}


/* =========================================================
   MAIN CONTENT
   ========================================================= */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}


/* =========================================================
   MAIN TITLE
   ========================================================= */

h1 {
    color: #1E293B !important;
    font-size: 42px !important;
    font-weight: 800 !important;
    text-align: center;
    margin-bottom: 10px;
}


/* =========================================================
   SUBTITLE / NORMAL TEXT
   ========================================================= */

p {
    color: #475569;
    font-size: 16px;
}


/* =========================================================
   SECTION HEADINGS
   ========================================================= */

h2, h3 {
    color: #1E293B !important;
    font-weight: 700 !important;
}


/* =========================================================
   TEXT INPUT
   ========================================================= */

.stTextInput > div > div > input {
    background-color: #FFFFFF !important;
    color: #1E293B !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 12px 15px !important;
    font-size: 16px !important;
}


/* INPUT FOCUS */

.stTextInput > div > div > input:focus {
    border: 2px solid #6366F1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15) !important;
}


/* =========================================================
   ANALYZE BUTTON
   ========================================================= */

.stButton > button {
    width: 100%;
    background: #1E293B !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    transition: all 0.3s ease !important;
}


/* BUTTON HOVER */

.stButton > button:hover {
    background: #334155 !important;
    color: #FFFFFF !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(30, 41, 59, 0.25);
}


/* =========================================================
   SUCCESS MESSAGE
   ========================================================= */

div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
}


/* =========================================================
   EXPANDER
   ========================================================= */

.streamlit-expanderHeader {
    background-color: #FFFFFF !important;
    color: #1E293B !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}


/* =========================================================
   REPORT CONTAINER
   ========================================================= */

div[data-testid="stMarkdownContainer"] {
    color: #334155;
}


/* =========================================================
   DOWNLOAD BUTTON
   ========================================================= */

.stDownloadButton > button {
    width: 100%;
    background: #6366F1 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
}


/* DOWNLOAD BUTTON HOVER */

.stDownloadButton > button:hover {
    background: #4F46E5 !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.25);
}


/* =========================================================
   SPINNER
   ========================================================= */

.stSpinner > div {
    color: #6366F1 !important;
}


/* =========================================================
   CODE / REPORT AREA
   ========================================================= */

code {
    color: #1E293B !important;
    background-color: #F8FAFC !important;
}


/* =========================================================
   HORIZONTAL LINE
   ========================================================= */

hr {
    border: none;
    height: 1px;
    background-color: #CBD5E1;
    margin: 25px 0;
}


/* =========================================================
   RESPONSIVE DESIGN
   ========================================================= */

@media (max-width: 768px) {

    h1 {
        font-size: 32px !important;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Repo Health Auditor",
    page_icon="🔍",
    layout="wide"
)


# ==========================================================
# TITLE
# ==========================================================

st.title("🔍 Repo Health Auditor")

st.write(
    "Analyze a GitHub repository using four AI agents."
)


# ==========================================================
# CHECK API KEY
# ==========================================================

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error(
        "OPENROUTER_API_KEY is missing in your .env file."
    )
    st.stop()


st.success("OpenRouter API key loaded successfully.")


# ==========================================================
# GITHUB URL INPUT
# ==========================================================

repo_url = st.text_input(
    "Enter GitHub repository URL",
    placeholder="https://github.com/username/repository"
)


# ==========================================================
# ANALYZE BUTTON
# ==========================================================

analyze_button = st.button(
    "🚀 Analyze Repository",
    type="primary"
)


# ==========================================================
# RUN ANALYSIS
# ==========================================================

if analyze_button:

    if not repo_url.strip():

        st.warning(
            "Please enter a GitHub repository URL."
        )
        st.stop()


    if "github.com" not in repo_url:

        st.error(
            "Please enter a valid GitHub repository URL."
        )
        st.stop()


    inputs = {
        "repo_url": repo_url.strip()
    }


    # ======================================================
    # CREW 1 - METADATA
    # ======================================================

    st.subheader(
        "1️⃣ Repository Metadata"
    )

    with st.spinner(
        "Collecting repository metadata..."
    ):

        try:

            metadata_crew = Crew(
                agents=[
                    repo_metadata_collector
                ],

                tasks=[
                    metadata_task
                ],

                process=Process.sequential,

                verbose=True
            )

            metadata_result = metadata_crew.kickoff(
                inputs=inputs
            )

            st.success(
                "Repository metadata collected successfully."
            )

            with st.expander(
                "View Metadata Result"
            ):

                st.write(
                    str(metadata_result)
                )

        except Exception as e:

            st.error(
                f"Metadata analysis failed: {e}"
            )

            st.stop()


    # ======================================================
    # CREW 2 - COMMUNITY
    # ======================================================

    st.subheader(
        "2️⃣ Community Signals"
    )

    with st.spinner(
        "Researching community signals..."
    ):

        try:

            community_crew = Crew(
                agents=[
                    community_signal_researcher
                ],

                tasks=[
                    community_task
                ],

                process=Process.sequential,

                verbose=True
            )

            community_result = community_crew.kickoff(
                inputs=inputs
            )

            st.success(
                "Community analysis completed."
            )

            with st.expander(
                "View Community Result"
            ):

                st.write(
                    str(community_result)
                )

        except Exception as e:

            st.error(
                f"Community analysis failed: {e}"
            )

            st.stop()


    # ======================================================
    # CREW 3 - ISSUES
    # ======================================================

    st.subheader(
        "3️⃣ Issue Analysis"
    )

    with st.spinner(
        "Analyzing GitHub issues..."
    ):

        try:

            issue_crew = Crew(
                agents=[
                    issue_triage_engineer
                ],

                tasks=[
                    issue_task
                ],

                process=Process.sequential,

                verbose=True
            )

            issue_result = issue_crew.kickoff(
                inputs=inputs
            )

            st.success(
                "Issue analysis completed."
            )

            with st.expander(
                "View Issue Result"
            ):

                st.write(
                    str(issue_result)
                )

        except Exception as e:

            st.error(
                f"Issue analysis failed: {e}"
            )

            st.stop()


    # ======================================================
    # FINAL REPORT
    # ======================================================

    st.subheader(
        "4️⃣ Final Repository Health Report"
    )

    health_report_task.description = f"""

    Create a comprehensive GitHub repository health report.

    Repository URL:
    {repo_url}


    REPOSITORY METADATA:
    {metadata_result}


    COMMUNITY ANALYSIS:
    {community_result}


    ISSUE ANALYSIS:
    {issue_result}


    Include:

    1. Repository Overview
    2. Repository Activity
    3. Community Health
    4. Issue Health
    5. Strengths
    6. Weaknesses
    7. Maintenance Risks
    8. Recommendations
    9. Overall Health Score from 0 to 100

    Explain why the selected health score was given.

    Use only the information provided above.
    Do not invent repository statistics.
    """


    with st.spinner(
        "Generating final health report..."
    ):

        try:

            final_crew = Crew(

                agents=[
                    health_report_writer
                ],

                tasks=[
                    health_report_task
                ],

                process=Process.sequential,

                verbose=True
            )

            final_result = final_crew.kickoff(
                inputs={
                    "repo_url": repo_url,
                    "metadata_result": str(
                        metadata_result
                    ),
                    "community_result": str(
                        community_result
                    ),
                    "issue_result": str(
                        issue_result
                    )
                }
            )

        except Exception as e:

            st.error(
                f"Final report generation failed: {e}"
            )

            st.stop()


    # ======================================================
    # DISPLAY FINAL REPORT
    # ======================================================

    st.success(
        "Repository health report generated successfully!"
    )

    st.markdown(
        "## 📊 Final Health Report"
    )

    st.markdown(
        str(final_result)
    )


    # ======================================================
    # SAVE REPORT
    # ======================================================

    report_text = str(final_result)

    with open(
        "repo_health_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            report_text
        )


    # ======================================================
    # DOWNLOAD BUTTON
    # ======================================================

    st.download_button(

        label="📥 Download Health Report",

        data=report_text,

        file_name="repo_health_report.txt",

        mime="text/plain"
    )

    st.success(
        "Report saved as repo_health_report.txt"
    )