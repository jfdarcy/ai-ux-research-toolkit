# AI UX Research Toolkit

> **🧠 My Philosophy: Augmented Rigor & The Co-Researcher Model**

To enhance the depth and objectivity of my work, I treat Artificial Intelligence (AI) as a tireless **"co-researcher"** rather than a simple automation tool. My goal is not to work faster, but to leverage AI to challenge my own assumptions and ensure the highest quality of insights.

This repository is a living portfolio of that philosophy in practice—each tool addresses a specific moment in the research lifecycle where human judgment is most vulnerable to bias, blind spots, or premature certainty. **One tool is live today;** the others are documented as in-development concepts with draft co-researcher prompts.

---

## Tools

| Status | Tool | UX Problem | Link |
|--------|------|------------|------|
| **Live** | [The UX Research Interview Refiner](./tools/interview-refiner/) | Interview guides hide leading questions and coverage gaps until fieldwork | [Try demo →](https://interview-refiner-jfdarcy.streamlit.app) · [Code →](./tools/interview-refiner/) |
| *In development* | [Research Plan Challenger](./tools/research-plan-challenger/) | Untested assumptions hide in research plans until it's too late | [Concept →](./tools/research-plan-challenger/) |
| *In development* | [Transcript Dual-Lens Analyzer](./tools/transcript-dual-lens/) | Single-researcher synthesis is vulnerable to confirmation bias | [Concept →](./tools/transcript-dual-lens/) |
| *In development* | [Insight Rigidity Checker](./tools/insight-rigidity-checker/) | Teams fall in love with insights before validating them against evidence | [Concept →](./tools/insight-rigidity-checker/) |

---

## Portfolio Site

The portfolio is published as a static site — no build step, no install required to view it.

### View it online

**https://jfdarcy.github.io/ai-ux-research-toolkit/**

The site presents the Augmented Rigor philosophy, a section for each tool explaining the UX problem it addresses, and links to the code in this repo.

### Preview locally

If you've cloned or downloaded this repo and want to preview changes before pushing, you'll need [Node.js](https://nodejs.org/) installed (which includes `npx`). To check:

```bash
node --version
```

From the root of this repo — the folder that contains `index.html` — run:

```bash
npx serve .
```

Then open **http://localhost:3000** in your browser. (The terminal will show the exact URL and port.)

To stop the server, press **Ctrl+C**.

**Don't have Node.js?** You can also open `index.html` directly in your browser (double-click the file in File Explorer or Finder). Most of the site will render correctly; some fonts load from the internet, so an offline preview may look slightly different.

---

## License

MIT
