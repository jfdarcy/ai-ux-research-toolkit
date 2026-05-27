"""
The UX Research Interview Refiner
A co-researcher tool that stress-tests draft interview guides against research objectives.
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from typing import Literal

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

ProviderId = Literal["claude", "gemini"]

ISSUES_URL = "https://github.com/jfdarcy/ai-ux-research-toolkit/issues/new/choose"

PROVIDERS: dict[ProviderId, dict[str, str]] = {
    "claude": {
        "label": "Claude (recommended)",
        "model": "claude-sonnet-4-20250514",
        "key_name": "ANTHROPIC_API_KEY",
        "key_url": "https://console.anthropic.com/",
    },
    "gemini": {
        "label": "Gemini",
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


def project_venv_python() -> Path:
    return Path(__file__).resolve().parent / ".venv" / "Scripts" / "python.exe"


def using_project_venv() -> bool:
    venv_python = project_venv_python()
    return venv_python.exists() and Path(sys.executable).resolve() == venv_python.resolve()


def venv_has_required_packages(venv_python: Path) -> bool:
    probe = (
        "import importlib.util, sys; "
        "sys.exit(0 if importlib.util.find_spec('anthropic') "
        "and importlib.util.find_spec('google.genai') else 1)"
    )
    result = subprocess.run(
        [str(venv_python), "-c", probe],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    return result.returncode == 0


def is_streamlit_cloud() -> bool:
    return os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud"


def resolve_api_key(provider: ProviderId, sidebar_key: str | None) -> str | None:
    """Sidebar key first; on Cloud, BYOK only (no host-provided secrets)."""
    if sidebar_key:
        return sidebar_key
    if is_streamlit_cloud():
        return None
    return get_api_key(provider)


def render_privacy_notice() -> None:
    hosted = is_streamlit_cloud()
    with st.expander("Privacy & confidentiality", expanded=hosted):
        st.markdown(
            "**This app is not air-gapped.** When you run a gap analysis, your objectives "
            "and draft interview guide are sent to the LLM provider you select (Anthropic or Google). "
            "Review their data policies before pasting client or confidential research."
        )
        if hosted:
            st.markdown(
                "You are using the **hosted demo** on Streamlit Community Cloud. Your inputs "
                "also pass through Streamlit's servers on the way to the provider. "
                "**Paste your own API key** in the sidebar — you pay for your usage; the host does not."
            )
            st.markdown(
                "For sensitive work, "
                "[run locally from GitHub]"
                "(https://github.com/jfdarcy/ai-ux-research-toolkit/tree/main/tools/interview-refiner) "
                "so data does not pass through this demo server."
            )
        else:
            st.markdown(
                "**Local run:** The Streamlit UI runs on your machine (`localhost`). "
                "Data still leaves your machine when sent to Claude or Gemini — local UI ≠ local AI."
            )
        st.caption(
            "Cost and data policies depend on your API key and provider account. "
            "Free-tier Gemini keys from AI Studio may use inputs to improve Google products. "
            "Claude usage is subject to Anthropic's terms."
        )


def render_setup_help(missing: list[str]) -> None:
    tool_dir = Path(__file__).resolve().parent
    venv_python = project_venv_python()
    venv_ready = venv_python.exists() and venv_has_required_packages(venv_python)
    use_venv_fix = venv_ready and not using_project_venv()

    st.error(
        f"Missing Python packages in this environment: **{', '.join(missing)}**"
    )

    if use_venv_fix:
        st.warning(
            f"Dependencies are installed in this project's `.venv`, but Streamlit is running with "
            f"`{sys.executable}` instead. On Windows, the global `streamlit` command often points "
            f"at Anaconda while `pip install` went into `.venv`."
        )
        st.markdown("**Recommended fix (PowerShell):**")
        st.code(
            f".\\.venv\\Scripts\\python.exe -m streamlit run interview_refiner.py",
            language="powershell",
        )
        st.markdown("**Or activate the venv first:**")
        st.code(
            ".\\.venv\\Scripts\\Activate.ps1\n"
            "python -m streamlit run interview_refiner.py",
            language="powershell",
        )
        st.caption(
            f"Run these from `{tool_dir}`. You can also use `.\\run.ps1` to start the app with the project venv."
        )
        return

    st.warning(
        f"Streamlit is running with `{sys.executable}`. "
        "Install dependencies into **this same Python**, not a different one."
    )
    if venv_python.exists():
        st.markdown("**Fix with the project venv (PowerShell):**")
        st.code(
            ".\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt\n"
            ".\\.venv\\Scripts\\python.exe -m streamlit run interview_refiner.py",
            language="powershell",
        )
    else:
        st.markdown("**Fix (PowerShell):**")
        st.code(
            "python -m venv .venv\n"
            ".\\.venv\\Scripts\\Activate.ps1\n"
            "python -m pip install -r requirements.txt\n"
            "python -m streamlit run interview_refiner.py",
            language="powershell",
        )
    st.caption(
        "Tip: If you use Anaconda and also have Python installed elsewhere, "
        "`pip install` and `streamlit run` may point at different environments. "
        "Using `.venv\\Scripts\\python.exe -m streamlit` keeps them aligned."
    )


def build_user_prompt(objectives: str, draft_guide: str) -> str:
    return USER_PROMPT_TEMPLATE.format(
        objectives=objectives.strip(),
        draft_guide=draft_guide.strip(),
    )


def get_api_key(provider: ProviderId) -> str | None:
    key_name = PROVIDERS[provider]["key_name"]

    env_key = os.environ.get(key_name)
    if env_key:
        return env_key

    try:
        return st.secrets[key_name]
    except (KeyError, StreamlitSecretNotFoundError):
        return None


def render_missing_api_key_help(key_name: str, key_url: str, label: str) -> None:
    st.error(f"No API key found for **{label}**.")
    st.markdown(f"Get a free key at [{key_url}]({key_url}), then use **one** of these options:")

    st.markdown("**Option 1 — Paste in the sidebar (easiest)**")
    st.caption("Enter your key in the **API key** field in the left sidebar, then click Run Gap Analysis again.")

    st.markdown("**Option 2 — Environment variable**")
    if sys.platform == "win32":
        st.code(
            f'$env:{key_name} = "your-key-here"\n'
            "python -m streamlit run interview_refiner.py",
            language="powershell",
        )
        st.caption("Set the variable in the same terminal session, then start (or restart) the app.")
    else:
        st.code(
            f'export {key_name}="your-key-here"\n'
            "python -m streamlit run interview_refiner.py",
            language="bash",
        )

    st.markdown("**Option 3 — Streamlit secrets file**")
    st.code(
        f'# tools/interview-refiner/.streamlit/secrets.toml\n{key_name} = "your-key-here"',
        language="toml",
    )


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


def render_provider_sidebar() -> tuple[ProviderId, str | None]:
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
            "Cost and privacy terms depend on your Google account and key type. "
            "Free-tier keys from AI Studio may use your inputs to improve Google products — "
            "do not paste confidential or client research if using a free-tier key.",
            icon="⚠️",
        )
        st.sidebar.caption(
            "Free keys are available via AI Studio; paid Google API keys are also supported."
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

    sidebar_key = st.sidebar.text_input(
        "API key",
        type="password",
        placeholder="Required — paste your key here" if is_streamlit_cloud() else "Paste your key here",
        help=(
            "Required on the hosted demo. On local run, optional if set via environment variable."
        ),
    )

    st.sidebar.caption(
        "You provide your own key — API usage is billed to you, not the app host."
    )

    st.sidebar.divider()
    st.sidebar.markdown(
        f"[Report a bug or suggest an improvement]({ISSUES_URL})"
    )
    st.sidebar.caption("Portfolio demo — issues reviewed when I can, no SLA.")

    return provider, sidebar_key.strip() or None


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

    provider, sidebar_key = render_provider_sidebar()

    st.title("The UX Research Interview Refiner")
    st.caption(
        "Augmented Rigor — treat AI as a co-researcher that challenges your draft, "
        "not a shortcut that rubber-stamps it."
    )

    if is_streamlit_cloud():
        st.info(
            "**Hosted demo** — paste your own API key in the sidebar. "
            "For confidential client work, run locally from GitHub instead.",
            icon="ℹ️",
        )

    render_privacy_notice()

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

        config = PROVIDERS[provider]
        api_key = resolve_api_key(provider, sidebar_key)
        if not api_key:
            render_missing_api_key_help(
                config["key_name"],
                config["key_url"],
                config["label"],
            )
            if is_streamlit_cloud():
                st.info("On the hosted demo, paste your key in the **API key** field in the sidebar.")
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
