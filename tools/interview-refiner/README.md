# The UX Research Interview Refiner

**Stage:** Before fieldwork  
**Philosophy:** Augmented Rigor — challenge your draft before participants do.

## The UX Problem

Interview guides often carry hidden assumptions, leading questions, and gaps that only surface after sessions are underway. By then, revision is costly and bias has already shaped what you hear.

## What This Tool Does

Given your **Research Objectives** and **Draft Interview Guide**, an AI co-researcher (Claude Sonnet):

1. Generates an **independent parallel guide** from objectives alone
2. Compares it against your draft
3. Outputs a structured Markdown report covering:
   - **Blind Spots** — objectives not covered in your draft
   - **Framing Bias** — leading questions or unstated assumptions
   - **Missed Angles** — creative questions and edge cases you overlooked

## Run Locally

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

### Setup

```bash
cd tools/interview-refiner

# Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure API Key

**Option A — environment variable (recommended)**

```bash
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY = "your-key-here"

# macOS / Linux
export ANTHROPIC_API_KEY="your-key-here"
```

**Option B — Streamlit secrets file**

Create `.streamlit/secrets.toml` in this directory:

```toml
ANTHROPIC_API_KEY = "your-key-here"
```

> Never commit your API key. Add `.streamlit/secrets.toml` to `.gitignore`.

### Launch

```bash
streamlit run interview_refiner.py
```

Streamlit opens the app at **http://localhost:8501**.

### Usage

1. Paste your **Research Objectives** in the left panel
2. Paste your **Draft Interview Guide** in the right panel
3. Click **Run Gap Analysis**
4. Review the Markdown report; download it with the button at the bottom

## File Structure

```
tools/interview-refiner/
├── interview_refiner.py   # Single-file Streamlit app
├── requirements.txt
└── README.md
```
