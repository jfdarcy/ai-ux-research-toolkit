# Insight Rigidity Checker

> **Status: In development** — not yet implemented. This folder documents the UX problem and a draft co-researcher prompt for a future tool.

**Stage:** Before sharing findings  
**Philosophy:** Augmented Rigor — love the question, not the answer.

## The UX Problem

Research teams often polish insights into compelling narratives before fully validating them against evidence. Stakeholders then act on fragile conclusions with unwarranted confidence.

## What This Tool Will Do

For each insight you draft, the co-researcher:

- Maps the insight back to specific supporting quotes
- Flags overgeneralizations and unsupported leaps
- Assigns a confidence score based on evidence density
- Asks: *What evidence would disprove this insight?*

## Usage

```bash
# Coming soon — insight validation workflow
python rigidity_checker.py --insight insight.md --transcripts ./data/
```

## Co-Researcher Prompt (Draft)

```
You are a skeptical co-researcher reviewing findings before they go to stakeholders.

For each insight provided:
1. List the exact quotes that support it (minimum 3)
2. Identify quotes that contradict or complicate it
3. Rate confidence: High / Medium / Low with justification
4. State what would disprove this insight
5. Rewrite the insight to be more precise if overgeneralized
```

---

**Live in this toolkit:** [The UX Research Interview Refiner](../interview-refiner/) — gap analysis for interview guides.
