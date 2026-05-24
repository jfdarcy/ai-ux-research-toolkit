# Transcript Dual-Lens Analyzer

**Stage:** During synthesis  
**Philosophy:** Augmented Rigor — two perspectives reveal what one cannot.

## The UX Problem

Single-researcher transcript coding is vulnerable to confirmation bias. We notice what we expect, deprioritize contradictions, and build narratives that feel coherent but may not be complete.

## What This Tool Does

Runs an independent AI thematic analysis alongside your human coding, then surfaces divergences:

- Themes present in AI analysis but absent from yours
- Quotes you tagged as minor that the AI flagged as significant
- Contradictory patterns across participant segments

## Usage

```bash
# Coming soon — dual-lens comparison workflow
python dual_lens.py --transcript interview.txt --your-themes themes.json
```

## Co-Researcher Prompt (Draft)

```
Analyze this interview transcript independently. Do not assume any prior themes.
Extract:
1. Top 5 emergent themes with supporting quotes
2. Contradictions or tensions within the participant's responses
3. Anything surprising or counter to common UX assumptions

After analysis, compare your output to the researcher's themes and highlight divergences only.
```
