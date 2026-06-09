# Evidence base, validation & caveats

Why the skill says "writing is universal; journals differ by scope." Full analysis: `摘要深度分析_内容层.md`; distributions: `data/codings_v2_agg.json`.

## Corpus & method
- **1,677 EP-journal abstracts** (2023–2026), topic-representative sample across the six journals (HR 253, CircAE 237, Europace 308, JACC 200, PACE 405, JICE 274).
- Every abstract **blind-coded** (coder unaware of journal) on a 13-dimension content codebook by **two independent frontier models — Claude (Sonnet) and Codex (GPT-5.4)**.

## Evidence that journals overlap on content
- **Average distributional overlap ≥86% per dimension** (avg TVD vs pooled ≤0.14 for both models on every content dimension; certainty_calibration ~0.01, voice ~0.08, study_type ~0.137 — the most journal-specific).
- **Content classifier**: predicting journal from the content codes alone scores **30% vs a 24% majority-class baseline** (chance 17%); removing study_type drops it to ~29% — non-study-type codes add little incremental journal prediction, though voice and reporting patterns still show usable tendencies. The main signal is **scope** (study type), concentrated in PACE (case reports) / Circ AE (preclinical).
- Individual *categories* can diverge up to ~30 points (PACE 30% case reports vs ~0–5% elsewhere) — these are scope, not writing style.

## Reliability (cross-model κ, Claude vs Codex)
Reliable (lean on these): study_type 0.91 · results_logic 0.76 · contribution_frame 0.72 · gap_type 0.69 ("substantial").
Lower-reliability (weak tendencies only): benchmarking 0.63 · voice 0.54 · conclusion_stance 0.49 · external_validation 0.43 · certainty_calibration 0.16 (near-constant 96–99% "matches design", a kappa-paradox).
Inter-coder (single model, 2 passes, v1 87-abstract sample): gap_type 0.78, contribution_frame 0.77, conclusion_stance 0.48.

## What the rigorous analysis corrected (vs earlier impressions)
- "Circ AE = AI venue" was a topic-filter artifact (a narrow CSP/LBBAP+AI subset showed AI 58%); in the representative corpus Circ AE AI is ~5% — its real signature is **mechanism/preclinical**.
- "Unstructured" was wrong (the early CSV had section labels stripped); original research is **structured** in all six (86–96%).
- Conclusion stance is not a strong differentiator and is low-reliability; certainty calibration is near-universal.

## Caveats (carry these when advising)
- The journal signal in content is **weak** — per-journal "dials" are tendencies, not rules.
- **JACC EP n=200** (smallest sample) → its figures (incl. the 90% impersonal-voice claim) carry the widest uncertainty.
- Conclusion_stance / voice / certainty are **low cross-model reliability** — don't over-rely.
- Corpus is **topic-representative, not exhaustive**; scope percentages are conditional on the sampled topic mix and the 2023–2026 window, not true journal output rates.
- Title-level metrics in `ep-title-advisor` come from a separate 7,267-article title analysis, not this abstract corpus.

## Provenance / reproducibility
Coding workflows: `.claude/workflows/abstract-coding-v2.js` (Claude), `run_codex_chunk.sh` + `data/codex_schema.json` (Codex). Aggregation/validation: `aggregate_codings.py`, `cross_model.py`, `p2_content_classifier.py`, `reliability.py`. Per-abstract codings: `data/codings_v2/`, `data/codings_codex/`.
