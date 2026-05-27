# The UX Research Interview Refiner

> **Status: Live** — Streamlit app with local and hosted demo options.

**Stage:** Before fieldwork  
**Philosophy:** Augmented Rigor — challenge your draft before participants do.

A Streamlit web app that stress-tests your interview guide against your research objectives. Supports **Claude** (recommended) or **Gemini** — you provide your own API key; cost and terms depend on your provider account.

---

## What This Tool Does

Paste two things into the app:

1. **Research Objectives** — what you're trying to learn
2. **Draft Interview Guide** — the questions you plan to ask

Click **Run Gap Analysis**. The AI acts as a rigorous UX research methodologist and returns a Markdown report with:

- **Blind Spots** — objectives your draft doesn't cover
- **Framing Bias** — leading questions or hidden assumptions
- **Missed Angles** — creative questions and edge cases you overlooked

It also generates an **independent parallel guide** built only from your objectives, so you can compare two perspectives side by side.

---

## Try it

| Option | Best for | Link |
|--------|----------|------|
| **Hosted demo** | Quick try in the browser — paste your own API key | [interview-refiner-jfdarcy.streamlit.app](https://interview-refiner-jfdarcy.streamlit.app) |
| **Run locally** | Confidential client work; data skips the demo server | [Setup instructions below](#step-1-get-the-code) |

---

## Privacy & confidentiality

**This tool is not air-gapped.** When you run an analysis, your objectives and draft interview guide are sent to the LLM provider you choose (Anthropic or Google). Review their data policies before pasting confidential research.

| | Hosted demo | Local run |
|---|-------------|-----------|
| **Streamlit UI** | Streamlit Community Cloud | Your machine (`localhost`) |
| **LLM processing** | Anthropic or Google (cloud) | Anthropic or Google (cloud) |
| **Who pays API costs** | You (your key in the sidebar) | You (your key) |
| **Best for** | Convenience, portfolio demos | Sensitive or client work |

> Run locally so your draft never passes through a public demo server. API calls still go to your chosen provider — **local UI ≠ local AI**.

---

## Before You Start

You will need:

| Requirement | Details |
|-------------|---------|
| **Python 3.10 or newer** | [Download Python](https://www.python.org/downloads/) — on Windows, check **"Add Python to PATH"** during install |
| **Git** (optional) | To clone the repo — [Download Git](https://git-scm.com/downloads) |
| **API key (pick one provider)** | Claude: [console.anthropic.com](https://console.anthropic.com/) · Gemini: [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (free keys available) |
| **Internet connection** | The app calls your chosen provider when you run an analysis |

To check Python is installed, open a terminal and run:

```bash
python --version
```

On some systems the command is `python3` instead of `python`. Use whichever works on your machine.

---

## Step 1: Get the Code

### Option A — Clone with Git (recommended)

Open a terminal and run:

```bash
git clone https://github.com/jfdarcy/ai-ux-research-toolkit.git
cd ai-ux-research-toolkit/tools/interview-refiner
```

### Option B — Download without Git

1. Go to [github.com/jfdarcy/ai-ux-research-toolkit](https://github.com/jfdarcy/ai-ux-research-toolkit)
2. Click the green **Code** button → **Download ZIP**
3. Unzip the file
4. Open a terminal and navigate into the tool folder:

```bash
# Replace the path below with wherever you saved the ZIP
cd path/to/ai-ux-research-toolkit-main/tools/interview-refiner
```

**Windows tip:** In File Explorer, shift-right-click the `interview-refiner` folder and choose **"Open in Terminal"** to start in the right place.

---

## Step 2: Set Up a Virtual Environment

A virtual environment keeps this tool's dependencies isolated from other Python projects on your machine.

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If you get an execution policy error when activating, run this once (then try activating again):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows (Command Prompt)

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

You should see `(.venv)` at the start of your terminal prompt — that means the environment is active.

> **Windows + Anaconda users:** If you have Anaconda and another Python installed, plain `pip install` and `streamlit run` may use different environments. Always use `python -m pip` and `python -m streamlit` after activating `.venv` so install and launch use the same Python.

---

## Step 3: Add Your API Key

The app supports two providers. Choose one — you only need the key for the provider you plan to use. **Never share or commit your key.**

| Provider | Best for | Key variable | Get a key |
|----------|----------|--------------|-----------|
| **Claude** (recommended) | Most rigorous gap analysis | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com/) |
| **Gemini** | Lower-cost option; free keys available via AI Studio, paid keys also work | `GEMINI_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |

> **Privacy note:** Cost and data policies depend on your API key and provider account. Free-tier Gemini keys from AI Studio may use your inputs to improve Google products. Do not paste confidential research on a free-tier Gemini key. Review your provider's terms before use.

### Set the key (pick one method)

**Method A — Environment variable (recommended)**

Set the variable for your chosen provider in the same terminal session where you'll launch the app:

```powershell
# Windows (PowerShell) — Claude
$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"

# Windows (PowerShell) — Gemini
$env:GEMINI_API_KEY = "your-key-here"
```

```cmd
# Windows (Command Prompt) — Claude
set ANTHROPIC_API_KEY=sk-ant-your-key-here

# Windows (Command Prompt) — Gemini
set GEMINI_API_KEY=your-key-here
```

```bash
# macOS / Linux — Claude
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# macOS / Linux — Gemini
export GEMINI_API_KEY="your-key-here"
```

**Method B — Streamlit secrets file**

Create a file at `tools/interview-refiner/.streamlit/secrets.toml`:

```toml
# Include one or both — the app uses whichever matches your sidebar selection
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
GEMINI_API_KEY = "your-key-here"
```

This file is already listed in the repo's `.gitignore` — it won't be committed if you push changes.

---

## Step 4: Launch the App

Make sure you're still inside `tools/interview-refiner` with your virtual environment active (`(.venv)` visible in the prompt).

```bash
python -m streamlit run interview_refiner.py
```

Your browser should open automatically to **http://localhost:8501**. If it doesn't, copy that URL into your browser manually.

To stop the app, press **Ctrl+C** in the terminal.

---

## Step 5: Run an Analysis

1. **Research Objectives** (left box) — paste your goals, key questions, and what success looks like
2. **Draft Interview Guide** (right box) — paste your planned questions and probes
3. **AI Provider** (sidebar) — choose Claude (recommended) or Gemini
4. **API key** (sidebar) — paste your key, *or* set it via environment variable / `secrets.toml` before launching (local only)
5. Click **Run Gap Analysis**
6. Wait for the report (usually 30–60 seconds)
7. Use **Download Report (.md)** to save the results

---

## Deploy to Streamlit Community Cloud (repo maintainers)

To publish the hosted demo (BYOK — **do not** add API keys to Cloud secrets):

1. Sign in at [share.streamlit.io](https://share.streamlit.io/) with GitHub
2. Click **Create app** → select `jfdarcy/ai-ux-research-toolkit`
3. Set **Main file path** to `tools/interview-refiner/interview_refiner.py`
4. Leave **Secrets** empty — users paste their own keys in the sidebar
5. Deploy; update the demo URL in `index.html` and this README if your app URL differs

Expected URL format: `https://interview-refiner-jfdarcy.streamlit.app` (you choose the subdomain at deploy time).

---

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| `'python' is not recognized` | Reinstall Python with **"Add to PATH"** checked, or use `py` on Windows: `py -m venv .venv` |
| `ModuleNotFoundError: No module named 'anthropic'` | Activate `.venv`, run `python -m pip install -r requirements.txt`, then launch with `python -m streamlit run interview_refiner.py` |
| `'streamlit' is not recognized` | Make sure the virtual environment is activated, then run `python -m pip install -r requirements.txt` again |
| `No API key found` | Set the key for your selected provider (`ANTHROPIC_API_KEY` or `GEMINI_API_KEY`), or add it to `.streamlit/secrets.toml` |
| `Analysis failed: ... authentication` | Your API key may be wrong or expired — create a new one at the provider's console |
| Port 8501 already in use | Another Streamlit app may be running — close it, or run: `streamlit run interview_refiner.py --server.port 8502` |
| Browser doesn't open | Go to http://localhost:8501 manually |

---

## What's in This Folder

```
tools/interview-refiner/
├── interview_refiner.py   # The app (single file)
├── requirements.txt       # Python packages needed
├── .streamlit/config.toml # Streamlit Cloud theme/config
└── README.md
```

---

## Questions or Issues

Open an issue on the main repo: [Report a bug or suggest an improvement](https://github.com/jfdarcy/ai-ux-research-toolkit/issues/new/choose)

This is a portfolio demo — issues are reviewed when I can; there is no support SLA. Please do not paste confidential research material in issues.
