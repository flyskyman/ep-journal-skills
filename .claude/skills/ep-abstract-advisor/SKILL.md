---
name: ep-abstract-advisor
description: Write, polish, or place a manuscript abstract for an EP journal (Heart Rhythm, Circ AE, Europace, JACC EP, PACE, JICE). Use when the user wants help drafting, improving, or choosing the right journal for an abstract. Trigger on "abstract", "write/polish abstract", "摘要" with EP journal names.
---

# EP Journal Abstract Advisor

**Core principle:** the *core argument structure* of a strong EP abstract is the same for all six journals. Journal-specific changes are mostly **scope** (which journal your study belongs in), plus format, voice, and limited reporting emphasis — not a different way of writing. So: write one strong abstract (Step 2), then fit it to the right journal (Step 3) and format it (Step 4). Don't write six "styles" from scratch. (Evidence + its limits: `references/evidence.md`.)

## When to use
- The user wants to draft or polish an abstract for an EP journal
- The user wants to choose / change the target journal for an abstract
- The user asks how to frame an abstract for a specific EP journal

## Step 1 — Gather
Target journal (or offer to recommend via Step 3); study type (original clinical / preclinical-basic / AI-ML / meta-analysis-review / case); the gap being closed; objective; design + population/source; key results **with numbers**; the takeaway. Optional: word limit, registry/acronym.

## Step 2 — Build the abstract (the real work; identical for every journal)
A strong abstract is a verifiable argument chain. Build it in six moves:

1. **Premise** (1 sentence) — the accepted fact / current standard.
2. **Gap** (1 sentence, highest-leverage) — pivot with *However/but/remains* to a **specific, falsifiable** unknown. Avoid "few studies exist" (weakest, highest-rejection move). Pick a gap type:
   `mechanistic_deficit` · `comparative_unknown` · `capability_gap` · `guideline_inadequacy` · `feasibility_in_niche` · `optimization_unknown` · `prevalence_or_characterization`.
3. **Aim** (1 sentence) — scoped exactly to close that gap; never broader than the methods deliver.
4. **Methods** (3–5 sentences) — design → population/source → key definitions/criteria → analysis. Credibility = specificity (name the cohort/registry, exact criteria, validation).
5. **Results** (the body, 4–6 sentences) — primary outcome first with **effect size + comparator + CI/p**, then secondary; report nulls honestly; feature a usable discriminator (ROC cutoff, non-inferiority margin, predictor) if you have one. Write results as a **comparison narrative** (before→after, or vs control — anchor every number to what it's compared against), not a dense metric dump.
6. **Conclusion** (1–2 sentences) — answer the gap; **calibrate certainty to the design** (no causal/universal claim from a retrospective single-center cohort); end with a brief **clinical-implication** clause (what it changes for practice).

**Content failure modes (these sink abstracts more than format):** gap stated as "few studies"; aim over-promises beyond methods; results give p-values with no effect size/comparator; conclusion over- or under-claims; the gap promised ≠ the result delivered; redundancy (sample characteristics or conclusions repeated across sections — state each once).

*(Step 2 is expert writing guidance informed by the corpus coding patterns — not every rule is individually proven by the data.)*

## Step 3 — Fit to the journal (scope, not style)
Match your study **type** to the journal whose scope it fits; then dial emphasis. Quick cues:
- **HR** broadest, any topic — the default. **PACE** case reports + feasibility/safety + light stats. **Circ AE** mechanism / preclinical-basic, hypothesis-driven. **JICE** technique head-to-head comparison + procedural detail. **Europace** evidence synthesis / registry / comparison. **JACC EP** clinical, quantitative (effect sizes), **impersonal voice**.

These are weak tendencies, not rules (the content signal between journals is small). The two robust levers: study-type **fit** (scope) and JACC's impersonal voice. Full per-journal scope + emphasis detail: **`references/journal-fit.md`**.

## Step 4 — Format (apply last)
Match the journal's word count and section labels. Original research is **usually structured** across all six (86–96%); exceptions are mainly article-type — case reports, images, narrative reviews, editorials. Word-count medians and the exact per-journal section-label templates (e.g., Europace's combined `AIMS / METHODS AND RESULTS / CONCLUSION`): **`references/journal-fit.md`**.

## Step 5 — Self-check
- Gap is a specific deficit of a real type — not "few studies".
- Results lead with effect size + comparator (+ discriminator if available).
- Conclusion certainty matches the design.
- Study type fits the target journal's scope (the most common real misfit).
- Voice / word count / section labels meet the journal's format (impersonal for JACC; combined Methods+Results for Europace).

## Polishing & repositioning
**Polish:** diagnose Step 2 first (gap specific? aim matches methods? results carry effect sizes? certainty fits design?), then fit (Step 3) and format (Step 4). Show edits with one-line rationales.
**Reposition for another journal:** usually NOT a rewrite — a fit check + emphasis dial + reformat (for JACC switch to impersonal voice; for Europace merge Methods+Results and add registration). Rewrite only when the study type genuinely doesn't fit the new journal's scope.

## Lint / score a draft
To diagnose a draft, run the bundled mechanical linter, then add the semantic judgments it can't make:
```
python scripts/lint.py <HR|CircAE|Europace|JACC|PACE|JICE> <draft.txt>
```
It checks the **countable** things vs the journal's targets: word count, section structure (incl. Europace's combined Methods+Results), voice (JACC impersonal), weak-gap clichés, results rigor (effect size + comparator vs p-only), overclaim words, redundancy. Treat its flags as prompts to check, not verdicts.
Then YOU judge the **semantic** items it can't: is the gap specific & of a real type (Step 2)? does the aim match the methods? does the conclusion's certainty fit the design? does the study type fit the journal's scope (Step 3)? Report flags + semantic findings with one-line fixes.

---
Supporting material (do not inline into this file): `references/journal-fit.md` (per-journal scope + format), `references/evidence.md` (data, validation, reliability, caveats), `scripts/lint.py` (mechanical draft linter), full analysis in `摘要深度分析_内容层.md`.
