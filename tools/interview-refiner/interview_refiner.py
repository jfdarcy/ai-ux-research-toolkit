"""
The UX Research Interview Refiner
A co-researcher tool that stress-tests draft interview guides against research objectives.
"""

import os

import streamlit as st
from anthropic import Anthropic

MODEL = "claude-sonnet-4-20250514"

SYSTEM_PROMPT = """You are a rigorous UX Research Methodologist acting as a tireless co-researcher.

Your role is NOT to approve the researcher's work—it is to challenge it with methodological rigor.

When given research objectives and a draft interview guide, you must:

1. Independently generate a parallel interview guide based ONLY on the stated objectives
   (do not anchor on the user's draft structure, wording, or assumptions).

2. Compare your independent guide against the user's draft.

3. Produce a structured Markdown report with exactly these sections:

## Independent Parallel Guide
(Brief intro, then your full alternative guide organized by topic/objective)

## Gap Analysis Report

### 1. Blind Spots
Objectives or research questions implied by the objectives that the user's draft
does not adequately cover. For each item: cite the objective, explain the gap, and
suggest a specific question or probe to add.

### 2. Framing Bias
Leading questions, loaded language, false dichotomies, or unstated assumptions
embedded in the user's draft. For each item: quote the problematic text, explain
why it biases responses, and offer a neutral reframe.

### 3. Missed Angles
Creative questions, edge cases, counter-scenarios, or participant segments the user's
draft overlooks—things your independent guide surfaced that add depth or reduce risk.
For each item: explain the angle and provide a ready-to-use question.

Be direct, specific, and evidence-based. Prefer actionable recommendations over general advice."""

USER_PROMPT_TEMPLATE = """## Research Objectives

{objectives}

---

## Draft Interview Guide (User's Version)

{draft_guide}

---

Perform your independent parallel guide generation and gap analysis now. Output the full
structured Markdown report as specified."""


def get_api_key() -> str | None:
    if "ANTHROPIC_API_KEY" in st.secrets:
        return st.secrets["ANTHROPIC_API_KEY"]
    return os.environ.get("ANTHROPIC_API_KEY")


def run_gap_analysis(client: Anthropic, objectives: str, draft_guide: str) -> str:
    message = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(
                    objectives=objectives.strip(),
                    draft_guide=draft_guide.strip(),
                ),
            }
        ],
    )
    return message.content[0].text


def main() -> None:
    st.set_page_config(
        page_title="UX Research Interview Refiner",
        page_icon="🔍",
        layout="wide",
    )

    st.title("The UX Research Interview Refiner")
    st.caption(
        "Augmented Rigor — treat AI as a co-researcher that challenges your draft, "
        "not a shortcut that rubber-stamps it."
    )

    col_left, col_right = st.columns(2)

    with col_left:
        objectives = st.text_area(
            "Research Objectives",
            height=220,
            placeholder=(
                "List your research objectives, key questions, and success criteria.\n\n"
                "Example:\n"
                "- Understand how first-time users discover core features\n"
                "- Identify friction in the onboarding flow\n"
                "- Explore mental models around pricing"
            ),
        )

    with col_right:
        draft_guide = st.text_area(
            "Draft Interview Guide",
            height=220,
            placeholder=(
                "Paste your draft interview guide—questions, probes, and section headers.\n\n"
                "Example:\n"
                "1. Tell me about the last time you signed up for a new app...\n"
                "2. Was the onboarding easy or difficult?\n"
                "3. Did you find the pricing clear?"
            ),
        )

    run_clicked = st.button("Run Gap Analysis", type="primary", use_container_width=True)

    if run_clicked:
        if not objectives.strip():
            st.error("Please enter your Research Objectives before running the analysis.")
            return
        if not draft_guide.strip():
            st.error("Please enter your Draft Interview Guide before running the analysis.")
            return

        api_key = get_api_key()
        if not api_key:
            st.error(
                "No API key found. Set the `ANTHROPIC_API_KEY` environment variable, "
                "or add it to `.streamlit/secrets.toml`."
            )
            st.code("export ANTHROPIC_API_KEY=your-key-here", language="bash")
            return

        with st.spinner("Running comparative gap analysis…"):
            try:
                client = Anthropic(api_key=api_key)
                report = run_gap_analysis(client, objectives, draft_guide)
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
                return

        st.divider()
        st.subheader("Gap Analysis Report")
        st.markdown(report)

        st.download_button(
            label="Download Report (.md)",
            data=report,
            file_name="interview-gap-analysis.md",
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()
