# Research Plan Challenger

> **Status: In development** — not yet implemented. This folder documents the UX problem and a draft co-researcher prompt for a future tool.

**Stage:** Before fieldwork  
**Philosophy:** Augmented Rigor — challenge assumptions before they become sunk costs.

## The UX Problem

Research plans often carry hidden assumptions about user behavior, scope, and success criteria. These rarely surface until after weeks of fieldwork, when revision becomes psychologically and politically costly.

## What This Tool Will Do

An AI co-researcher adversarially reviews your research plan:

- Surfaces untested hypotheses embedded in objectives
- Flags leading or biased interview questions
- Proposes counter-scenarios and edge cases
- Suggests alternative methods when the plan has blind spots

## Usage

```bash
# Coming soon — scaffold for co-researcher prompt workflow
python challenger.py --plan your-research-plan.md
```

## Co-Researcher Prompt (Draft)

```
You are a senior UX researcher reviewing a colleague's research plan.
Your job is NOT to approve it — your job is to find what they haven't considered.

For each section of the plan:
1. Identify assumptions stated as facts
2. List 3 counter-hypotheses
3. Flag questions that could lead the participant
4. Suggest one alternative method that would stress-test the same objective
```

---

**Live in this toolkit:** [The UX Research Interview Refiner](../interview-refiner/) — gap analysis for interview guides.
