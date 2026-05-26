# The UX Research Interview Refiner

**Stage:** Before fieldwork  
**Philosophy:** Augmented Rigor — challenge your draft before participants do.

A Streamlit web app that stress-tests your interview guide against your research objectives. Supports **Claude** (recommended) or **Gemini** (free tier).

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

## Before You Start

You will need:

| Requirement | Details |
|-------------|---------|
| **Python 3.10 or newer** | [Download Python](https://www.python.org/downloads/) — on Windows, check **"Add Python to PATH"** during install |
| **Git** (optional) | To clone the repo — [Download Git](https://git-scm.com/downloads) |
| **API key (pick one provider)** | Claude: [console.anthropic.com](https://console.anthropic.com/) · Gemini: [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (free tier) |
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
pip install -r requirements.txt
```

If you get an execution policy error when activating, run this once (then try activating again):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows (Command Prompt)

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You should see `(.venv)` at the start of your terminal prompt — that means the environment is active.

---

## Step 3: Add Your API Key

The app supports two providers. Choose one — you only need the key for the provider you plan to use. **Never share or commit your key.**

| Provider | Best for | Key variable | Get a key |
|----------|----------|--------------|-----------|
| **Claude** (recommended) | Most rigorous gap analysis | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com/) |
| **Gemini** (free tier) | Trying the tool at no cost | `GEMINI_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |

> **Privacy note:** Gemini's free tier may use your inputs to improve Google products. Do not paste confidential or client research on the free tier. Use Claude for sensitive work.

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
streamlit run interview_refiner.py
```

Your browser should open automatically to **http://localhost:8501**. If it doesn't, copy that URL into your browser manually.

To stop the app, press **Ctrl+C** in the terminal.

---

## Step 5: Run an Analysis

1. **Research Objectives** (left box) — paste your goals, key questions, and what success looks like
2. **Draft Interview Guide** (right box) — paste your planned questions and probes
3. **AI Provider** (sidebar) — choose Claude (recommended) or Gemini (free tier)
4. Click **Run Gap Analysis**
5. Wait for the report (usually 30–60 seconds)
6. Use **Download Report (.md)** to save the results

---

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| `'python' is not recognized` | Reinstall Python with **"Add to PATH"** checked, or use `py` on Windows: `py -m venv .venv` |
| `'streamlit' is not recognized` | Make sure the virtual environment is activated, then run `pip install -r requirements.txt` again |
| `No API key found` | Set the key for your selected provider (`ANTHROPIC_API_KEY` or `GEMINI_API_KEY`), or add it to `.streamlit/secrets.toml` |
| `Analysis failed: ... authentication` | Your API key may be wrong or expired — create a new one at the provider's console |
| Port 8501 already in use | Another Streamlit app may be running — close it, or run: `streamlit run interview_refiner.py --server.port 8502` |
| Browser doesn't open | Go to http://localhost:8501 manually |

---

## What's in This Folder

```
tools/interview-refiner/
├── interview_refiner.py   # The app (single file)
├── requirements.txt     # Python packages needed
└── README.md            # This file
```

---

## Questions or Issues

Open an issue on the main repo: [github.com/jfdarcy/ai-ux-research-toolkit/issues](https://github.com/jfdarcy/ai-ux-research-toolkit/issues)
