"""
Thematic Analyzer
A co-researcher tool that runs blind thematic analysis on transcripts and surfaces divergences.
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
APP_FILE = "thematic_analyzer.py"

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

PHASE1_SYSTEM_PROMPT = """You are a rigorous UX research synthesizer acting as a tireless co-researcher.

Your role is NOT to validate the researcher's coding—it is to analyze the transcript independently with methodological rigor.

Analyze the interview transcript provided. Do NOT assume any prior themes from the researcher—you are seeing this data for the first time.

Produce a structured Markdown report with exactly these sections:

## Independent Thematic Analysis

### Emergent Themes
For each theme (aim for 5–8):
- **Theme name** — one-sentence definition
- Supporting quotes (2–3 verbatim excerpts from the transcript)
- Why this theme matters for UX/product decisions

### Internal Contradictions
Tensions or contradictions within the participant's responses. Cite quotes.

### Surprises
Patterns counter to common UX assumptions or worth flagging to the research team.

Be direct, specific, and quote-grounded."""

PHASE2_SYSTEM_PROMPT = """You are a rigorous UX research synthesizer acting as a tireless co-researcher.

You previously completed an independent thematic analysis of an interview transcript. The researcher has now shared their working themes from their own coding pass.

Your job is to compare the two perspectives and report ONLY where they diverge. Do not restate agreements.

Produce a structured Markdown report with exactly these sections:

## Divergence Report

### Missed Themes
Themes present in the independent analysis but absent or weak in the researcher's working themes. For each: explain the gap and cite evidence.

### Underweighted Evidence
Quotes or patterns the researcher may have treated as minor that the independent analysis flagged as central—or vice versa. Cite transcript excerpts.

### Framing Differences
Same quote or pattern interpreted differently between the two analyses. Show both framings.

### Segment or Context Gaps
Patterns the independent analysis connected that the researcher's themes did not surface.

If there are no meaningful divergences in a section, write "None identified" and briefly explain why.

Be direct and evidence-based."""

PHASE1_USER_TEMPLATE = """## Interview Transcript

{transcript}

---

Perform your independent thematic analysis now. Output the full structured Markdown report as specified."""

PHASE2_USER_TEMPLATE = """## Interview Transcript (reference)

{transcript}

---

## Independent Analysis (Phase 1 — completed blind)

{independent_analysis}

---

## Researcher's Working Themes

{working_themes}

---

Compare the independent analysis to the researcher's working themes. Output the Divergence Report only, as specified."""


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
    if sidebar_key:
        return sidebar_key
    if is_streamlit_cloud():
        return None
    return get_api_key(provider)


def get_api_key(provider: ProviderId) -> str | None:
    key_name = PROVIDERS[provider]["key_name"]
    env_key = os.environ.get(key_name)
    if env_key:
        return env_key
    try:
        return st.secrets[key_name]
    except (KeyError, StreamlitSecretNotFoundError):
        return None


def render_privacy_notice() -> None:
    hosted = is_streamlit_cloud()
    with st.expander("Privacy & confidentiality", expanded=hosted):
        st.markdown(
            "**This app is not air-gapped.** When you run an analysis, your transcript "
            "(and optional working themes) are sent to the LLM provider you select (Anthropic or Google). "
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
                "(https://github.com/jfdarcy/ai-ux-research-toolkit/tree/main/tools/thematic-analyzer) "
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

    st.error(f"Missing Python packages in this environment: **{', '.join(missing)}**")

    if use_venv_fix:
        st.warning(
            f"Dependencies are installed in this project's `.venv`, but Streamlit is running with "
            f"`{sys.executable}` instead. On Windows, the global `streamlit` command often points "
            f"at Anaconda while `pip install` went into `.venv`."
        )
        st.markdown("**Recommended fix (PowerShell):**")
        st.code(
            f".\\.venv\\Scripts\\python.exe -m streamlit run {APP_FILE}",
            language="powershell",
        )
        st.markdown("**Or activate the venv first:**")
        st.code(
            f".\\.venv\\Scripts\\Activate.ps1\npython -m streamlit run {APP_FILE}",
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
            f".\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt\n"
            f".\\.venv\\Scripts\\python.exe -m streamlit run {APP_FILE}",
            language="powershell",
        )
    else:
        st.markdown("**Fix (PowerShell):**")
        st.code(
            "python -m venv .venv\n"
            ".\\.venv\\Scripts\\Activate.ps1\n"
            "python -m pip install -r requirements.txt\n"
            f"python -m streamlit run {APP_FILE}",
            language="powershell",
        )
    st.caption(
        "Tip: If you use Anaconda and also have Python installed elsewhere, "
        "`pip install` and `streamlit run` may point at different environments. "
        "Using `.venv\\Scripts\\python.exe -m streamlit` keeps them aligned."
    )


def render_missing_api_key_help(key_name: str, key_url: str, label: str) -> None:
    st.error(f"No API key found for **{label}**.")
    st.markdown(f"Get a key at [{key_url}]({key_url}), then use **one** of these options:")

    st.markdown("**Option 1 — Paste in the sidebar (easiest)**")
    st.caption(
        "Enter your key in the **API key** field in the left sidebar, then click Run Thematic Analysis again."
    )

    st.markdown("**Option 2 — Environment variable**")
    if sys.platform == "win32":
        st.code(
            f'$env:{key_name} = "your-key-here"\npython -m streamlit run {APP_FILE}',
            language="powershell",
        )
    else:
        st.code(
            f'export {key_name}="your-key-here"\npython -m streamlit run {APP_FILE}',
            language="bash",
        )

    st.markdown("**Option 3 — Streamlit secrets file**")
    st.code(
        f"# tools/thematic-analyzer/.streamlit/secrets.toml\n{key_name} = \"your-key-here\"",
        language="toml",
    )


def call_claude(api_key: str, system: str, user: str) -> str:
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=PROVIDERS["claude"]["model"],
        max_tokens=8192,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return message.content[0].text


def call_gemini(api_key: str, system: str, user: str) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=PROVIDERS["gemini"]["model"],
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=8192,
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty response. Try again or switch to Claude.")
    return response.text


def call_provider(provider: ProviderId, api_key: str, system: str, user: str) -> str:
    if provider == "claude":
        return call_claude(api_key, system, user)
    return call_gemini(api_key, system, user)


def run_independent_analysis(provider: ProviderId, api_key: str, transcript: str) -> str:
    user_prompt = PHASE1_USER_TEMPLATE.format(transcript=transcript.strip())
    return call_provider(provider, api_key, PHASE1_SYSTEM_PROMPT, user_prompt)


def run_divergence_analysis(
    provider: ProviderId,
    api_key: str,
    transcript: str,
    independent_analysis: str,
    working_themes: str,
) -> str:
    user_prompt = PHASE2_USER_TEMPLATE.format(
        transcript=transcript.strip(),
        independent_analysis=independent_analysis.strip(),
        working_themes=working_themes.strip(),
    )
    return call_provider(provider, api_key, PHASE2_SYSTEM_PROMPT, user_prompt)


def run_thematic_analysis(
    provider: ProviderId,
    api_key: str,
    transcript: str,
    working_themes: str | None,
    status=None,
) -> str:
    if status is not None:
        status.update(label="Phase 1: Running blind thematic analysis…")
    independent = run_independent_analysis(provider, api_key, transcript)

    if not working_themes or not working_themes.strip():
        return f"# Thematic Analysis Report\n\n{independent.strip()}"

    if status is not None:
        status.update(label="Phase 2: Comparing perspectives and surfacing divergences…")
    divergence = run_divergence_analysis(
        provider, api_key, transcript, independent, working_themes
    )
    return f"# Thematic Analysis Report\n\n{independent.strip()}\n\n---\n\n{divergence.strip()}"


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
            "Claude is recommended for the most rigorous thematic analysis.",
            icon="ℹ️",
        )

    key_name = config["key_name"]
    st.sidebar.markdown(
        f"Requires `{key_name}`. [Get a key →]({config['key_url']})"
    )

    sidebar_key = st.sidebar.text_input(
        "API key",
        type="password",
        placeholder="Required — paste your key here" if is_streamlit_cloud() else "Paste your key here",
        help="Required on the hosted demo. On local run, optional if set via environment variable.",
    )

    st.sidebar.caption("You provide your own key — API usage is billed to you, not the app host.")

    st.sidebar.divider()
    st.sidebar.markdown(f"[Report a bug or suggest an improvement]({ISSUES_URL})")
    st.sidebar.caption("Portfolio demo — issues reviewed when I can, no SLA.")

    return provider, sidebar_key.strip() or None


def main() -> None:
    st.set_page_config(
        page_title="Thematic Analyzer",
        page_icon="📊",
        layout="wide",
    )

    missing = missing_packages()
    if missing:
        st.title("Thematic Analyzer")
        render_setup_help(missing)
        return

    provider, sidebar_key = render_provider_sidebar()

    st.title("Thematic Analyzer")
    st.caption(
        "Augmented Rigor — a blind co-researcher pass on your transcript, "
        "then divergence-only comparison with your working themes."
    )

    if is_streamlit_cloud():
        st.info(
            "**Hosted demo** — paste your own API key in the sidebar. "
            "For confidential client work, run locally from GitHub instead.",
            icon="ℹ️",
        )

    render_privacy_notice()

    col_left, col_right = st.columns([3, 2])

    with col_left:
        transcript = st.text_area(
            "Interview Transcript",
            height=320,
            placeholder=(
                "Paste one interview transcript.\n\n"
                "Example:\n"
                "Interviewer: Walk me through the last time you tried to...\n"
                "Participant: Sure, so I was on my phone and..."
            ),
        )

    with col_right:
        working_themes = st.text_area(
            "Your Working Themes (optional)",
            height=320,
            placeholder=(
                "Paste theme names, a rough codebook, or notes from your first coding pass.\n\n"
                "Example:\n"
                "- Onboarding confusion — user couldn't find settings\n"
                "- Trust in pricing — worried about hidden fees\n"
                "- Mobile-first workflow\n\n"
                "Leave blank for independent analysis only."
            ),
        )

    run_clicked = st.button("Run Thematic Analysis", type="primary", use_container_width=True)

    if run_clicked:
        if not transcript.strip():
            st.error("Please paste an interview transcript before running the analysis.")
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

        with st.status(f"Analyzing with {PROVIDERS[provider]['label']}…", expanded=True) as status:
            try:
                report = run_thematic_analysis(
                    provider,
                    api_key,
                    transcript,
                    working_themes,
                    status=status,
                )
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
                return
            status.update(label="Analysis complete", state="complete")

        st.divider()
        st.subheader("Thematic Analysis Report")
        phase_note = (
            "Includes independent analysis and divergence report."
            if working_themes.strip()
            else "Independent analysis only (no working themes provided)."
        )
        st.caption(
            f"Generated with {PROVIDERS[provider]['label']} ({PROVIDERS[provider]['model']}) · {phase_note}"
        )
        st.markdown(report)

        st.download_button(
            label="Download Report (.md)",
            data=report,
            file_name="thematic-analysis-report.md",
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()
