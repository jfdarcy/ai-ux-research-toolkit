# Thematic Analyzer

> **Status: In development** — Streamlit app in progress. Run locally from this folder; hosted demo not deployed yet.

**Stage:** During synthesis  
**Philosophy:** Augmented Rigor — a parallel perspective reveals what one pass cannot.

A Streamlit web app that runs a **blind thematic analysis** on an interview transcript, then optionally compares it to your working themes and reports **only divergences**. Supports **Claude** (recommended) or **Gemini** — you provide your own API key; cost and terms depend on your provider account.

---

## What This Tool Does

Paste your inputs:

1. **Interview Transcript** — one session at a time (required)
2. **Your Working Themes** — optional theme names, codebook, or coding notes

Click **Run Thematic Analysis**. The AI co-researcher:

**Phase 1 — Blind analysis (always runs)**  
Analyzes the transcript without seeing your themes. Returns emergent themes with supporting quotes, internal contradictions, and surprises.

**Phase 2 — Divergence report (when you provide working themes)**  
Compares the blind analysis to your themes and reports only where perspectives differ:

- **Missed themes** — present in AI analysis, weak or absent in yours
- **Underweighted evidence** — quotes treated differently in importance
- **Framing differences** — same evidence, different interpretation
- **Segment or context gaps** — patterns you didn't connect

If you skip working themes, you get Phase 1 only.

---

## Try it

| Option | Best for | Link |
|--------|----------|------|
| **Run locally** | Confidential client work; data skips the demo server | [Setup instructions below](#quick-start-local) |

> **Hosted demo:** Not deployed yet — run locally with `.\run.ps1`.

---

## Privacy & confidentiality

**This tool is not air-gapped.** When you run an analysis, your transcript (and optional themes) are sent to the LLM provider you choose (Anthropic or Google). Review their data policies before pasting confidential research.

| | Hosted demo | Local run |
|---|-------------|-----------|
| **Streamlit UI** | Streamlit Community Cloud | Your machine (`localhost`) |
| **LLM processing** | Anthropic or Google (cloud) | Anthropic or Google (cloud) |
| **Who pays API costs** | You (your key in the sidebar) | You (your key) |
| **Best for** | Convenience, portfolio demos | Sensitive or client work |

> Run locally so your transcript never passes through a public demo server. API calls still go to your chosen provider — **local UI ≠ local AI**.

---

## Quick start (local)

From the repo root:

```powershell
cd tools\thematic-analyzer
.\run.ps1
```

Or manually:

```powershell
cd tools\thematic-analyzer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run thematic_analyzer.py
```

Open **http://localhost:8501** in your browser.

### API key

Set via sidebar, environment variable, or `.streamlit/secrets.toml`:

| Provider | Variable | Get a key |
|----------|----------|-----------|
| Claude (recommended) | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com/) |
| Gemini | `GEMINI_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |

> **Privacy note:** Cost and data policies depend on your API key and provider account. Free-tier Gemini keys from AI Studio may use your inputs to improve Google products. Do not paste confidential research on a free-tier Gemini key.

---

## How to use the app

1. **Interview Transcript** — paste one full transcript
2. **Your Working Themes** (optional) — paste your draft themes or codebook
3. **AI Provider** (sidebar) — choose Claude (recommended) or Gemini
4. **API key** (sidebar) — paste your key, or set via environment / secrets before launch
5. Click **Run Thematic Analysis**
6. Wait for Phase 1 (and Phase 2 if themes provided)
7. Use **Download Report (.md)** to save results

---

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Set **Main file path:** `tools/thematic-analyzer/thematic_analyzer.py`
4. Do **not** add API keys to Streamlit secrets — users bring their own (BYOK)
5. Deploy and update the demo URL in the portfolio if it differs from the placeholder above

---

## File structure

```
tools/thematic-analyzer/
├── thematic_analyzer.py   # Streamlit app
├── requirements.txt
├── run.ps1                # Windows one-step launcher
├── .streamlit/config.toml
└── README.md
```

---

## Questions or Issues

Open an issue on the main repo: [Report a bug or suggest an improvement](https://github.com/jfdarcy/ai-ux-research-toolkit/issues/new/choose)

This is a portfolio demo — issues are reviewed when I can; there is no support SLA. Please do not paste confidential research material in issues.

---

**Also live in this toolkit:** [The UX Research Interview Refiner](../interview-refiner/) — gap analysis for interview guides.
