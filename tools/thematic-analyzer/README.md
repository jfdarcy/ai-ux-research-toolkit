# Thematic Analyzer

> **Status: In development** — not yet implemented. This folder documents the UX problem and a draft co-researcher prompt for a future tool.

**Stage:** During synthesis  
**Philosophy:** Augmented Rigor — a parallel perspective reveals what one pass cannot.

## The UX Problem

Single-researcher transcript coding is vulnerable to confirmation bias. We notice what we expect, underweight contradictions, and polish narratives that feel coherent but may be incomplete.

## How It Will Work

The tool applies the same **co-researcher** pattern as the Interview Refiner: the AI does not replace your synthesis — it runs a **parallel, blind analysis** and then reports only where the two perspectives diverge.

### Planned workflow

1. **Paste the transcript** — one interview at a time to start (multi-transcript batch is a later enhancement).
2. **Optionally paste your working themes** — a short list of theme names, a rough codebook, or notes from your own first pass. If omitted, the tool still runs blind analysis and returns the AI's independent themes only.
3. **Run analysis** — BYOK model (Claude recommended, Gemini supported), same provider pattern as Interview Refiner.
4. **Receive a structured Markdown report** with two parts:

**Part A — Independent thematic analysis (AI-only, no anchoring)**

- 5–8 emergent themes with definition and 2–3 supporting quotes each
- Internal contradictions or tensions within the participant's responses
- Surprises or counter-intuitive patterns relative to common UX assumptions

**Part B — Divergence report (only where perspectives differ)**

- **Missed themes** — present in AI analysis, absent or weak in yours
- **Underweighted evidence** — quotes you tagged as minor that the AI flagged as central (or vice versa)
- **Framing differences** — same quote interpreted differently
- **Segment or context gaps** — patterns the AI surfaced that your coding didn't connect

5. **Download report** — save as `.md` for synthesis notes or team review.

### Design principles

- **Blind first, compare second** — the AI must not see your themes until after its independent pass (two-step prompt or two API calls).
- **Divergence-only comparison** — the output highlights disagreement, not agreement; reduces rubber-stamping.
- **Quote-grounded** — every theme and divergence cites transcript evidence.
- **Privacy honest** — same BYOK + not-air-gapped positioning as Interview Refiner; no confidential client data on hosted demo.

## Usage

```bash
# Coming soon — independent thematic analysis + divergence report
python thematic_analyzer.py --transcript interview.txt --themes your-themes.md
```

## Co-Researcher Prompt (Draft)

```
You are a rigorous UX research synthesizer acting as a tireless co-researcher.

PHASE 1 — Independent analysis (do this first; do not read the researcher's themes yet):
Analyze this interview transcript. Extract emergent themes from the data only.
For each theme: name it, define it in one sentence, and cite 2–3 supporting quotes.
Also note internal contradictions and anything surprising relative to typical UX assumptions.

PHASE 2 — Divergence check (only after Phase 1):
Compare your themes to the researcher's working themes below.
Report ONLY divergences:
- Themes you found that they missed or underdeveloped
- Quotes they may have underweighted
- Same evidence framed differently
Do not restate agreements.
```

---

**Live in this toolkit:** [The UX Research Interview Refiner](../interview-refiner/) — gap analysis for interview guides.
