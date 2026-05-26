"""
The UX Research Interview Refiner
A co-researcher tool that stress-tests draft interview guides against research objectives.
"""

import importlib.util
import os
import sys
from typing import Literal

import streamlit as st

ProviderId = Literal["claude", "gemini"]

PROVIDERS: dict[ProviderId, dict[str, str]] = {
    "claude": {
        "label": "Claude (recommended)",
        "model": "claude-sonnet-4-20250514",
        "key_name": "ANTHROPIC_API_KEY",
        "key_url": "https://console.anthropic.com/",
    },
    "gemini": {
        "label": "Gemini (free tier)",
        "model": "gemini-2.5-flash",
        "key_name": "GEMINI_API_KEY",
        "key_url": "https://aistudio.google.com/apikey",
    },
}

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


def missing_packages() -> list[str]:
    missing: list[str] = []
    if importlib.util.find_spec("anthropic") is None:
        missing.append("anthropic")
    if importlib.util.find_spec("google.genai") is None:
        missing.append("google-genai")
    return missing


def render_setup_help(missing: list[str]) -> None:
    st.error(
        f"Missing Python packages in this environment: **{', '.join(missing)}**"
    )
    st.warning(
        f"Streamlit is running with `{sys.executable}`. "
        "Install dependencies into **this same Python**, not a different one."
    )
    st.markdown("**Fix (PowerShell):**")
    st.code(
        "python -m pip install -r requirements.txt\n"
        "python -m streamlit run interview_refiner.py",
        language="powershell",
    )
    st.caption(
        "Tip: If you use Anaconda and also have Python installed elsewhere, "
        "`pip install` and `streamlit run` may point at different environments. "
        "Using `python -m pip` and `python -m streamlit` keeps them aligned."
    )


def build_user_prompt(objectives: str, draft_guide: str) -> str:
    return USER_PROMPT_TEMPLATE.format(
        objectives=objectives.strip(),
        draft_guide=draft_guide.strip(),
    )


def get_api_key(provider: ProviderId) -> str | None:
    key_name = PROVIDERS[provider]["key_name"]
    if key_name in st.secrets:
        return st.secrets[key_name]
    return os.environ.get(key_name)


def run_gap_analysis_claude(api_key: str, objectives: str, draft_guide: str) -> str:
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=PROVIDERS["claude"]["model"],
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(objectives, draft_guide)}],
    )
    return message.content[0].text


def run_gap_analysis_gemini(api_key: str, objectives: str, draft_guide: str) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=PROVIDERS["gemini"]["model"],
        contents=build_user_prompt(objectives, draft_guide),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=8192,
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty response. Try again or switch to Claude.")
    return response.text


def run_gap_analysis(provider: ProviderId, api_key: str, objectives: str, draft_guide: str) -> str:
    if provider == "claude":
        return run_gap_analysis_claude(api_key, objectives, draft_guide)
    return run_gap_analysis_gemini(api_key, objectives, draft_guide)


def render_provider_sidebar() -> ProviderId:
    st.sidebar.header("AI Provider")

    provider: ProviderId = st.sidebar.radio(
        "Choose a model",
        options=["claude", "gemini"],
        format_func=lambda pid: PROVIDERS[pid]["label"],
        index=0,
    )

    config = PROVIDERS[provider]
    st.sidebar.caption(f"Model: `{config['model']}`")

    if provider == "gemini":
        st.sidebar.warning(
            "Gemini free tier may use your inputs to improve Google products. "
            "Do not paste confidential or client research material.",
            icon="⚠️",
        )
    else:
        st.sidebar.info(
            "Claude is recommended for the most rigorous gap analysis.",
            icon="ℹ️",
        )

    key_name = config["key_name"]
    st.sidebar.markdown(
        f"Requires `{key_name}`. "
        f"[Get a key →]({config['key_url']})"
    )

    return provider


def main() -> None:
    st.set_page_config(
        page_title="UX Research Interview Refiner",
        page_icon="🔍",
        layout="wide",
    )

    missing = missing_packages()
    if missing:
        st.title("The UX Research Interview Refiner")
        render_setup_help(missing)
        return

    provider = render_provider_sidebar()

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

        key_name = PROVIDERS[provider]["key_name"]
        api_key = get_api_key(provider)
        if not api_key:
            st.error(
                f"No API key found for {PROVIDERS[provider]['label']}. "
                f"Set `{key_name}` as an environment variable or in `.streamlit/secrets.toml`."
            )
            st.code(f'export {key_name}="your-key-here"', language="bash")
            return

        with st.spinner(f"Running comparative gap analysis with {PROVIDERS[provider]['label']}…"):
            try:
                report = run_gap_analysis(provider, api_key, objectives, draft_guide)
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
                return

        st.divider()
        st.subheader("Gap Analysis Report")
        st.caption(f"Generated with {PROVIDERS[provider]['label']} ({PROVIDERS[provider]['model']})")
        st.markdown(report)

        st.download_button(
            label="Download Report (.md)",
            data=report,
            file_name="interview-gap-analysis.md",
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()
