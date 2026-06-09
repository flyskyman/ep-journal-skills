# EP Journal Title Analysis Project

This project contains PubMed article data and analysis for 6 major EP journals (2023-2026):
- Heart Rhythm, Circ AE, Europace, JACC EP, PACE, JICE

## Directory layout
- `.claude/skills/` — the two finished skills (deliverables); each is lean `SKILL.md` + `references/` (+ `scripts/` for abstract).
- `.claude/workflows/` — provenance records of how the corpus was built/validated (coding, reliability, generate/judge loops), not active tooling.
- `data/` — canonical artifacts referenced by the skills: `corpus_v2.json` (1,677-abstract corpus), `codings_v2/` + `codings_codex/` (dual-model blind codings), `codings_v2_agg.json`, `title_metrics.json`, `*_xval/redteam_*.json` (cross-model validation), `loop_*/RESULTS.md` (generate-vs-baseline eval records), `corpus_csv/` (raw PubMed pulls), `*_schema.json`.
- `data/_intermediate/` — scratch (coding chunks, per-loop judge tasks/outputs, superseded v1 products). Safe to ignore.
- Root analysis docs: `摘要深度分析_内容层.md` (abstract content findings, referenced by the skill), `skills迭代方法论与经验.md` (methodology + lessons).
- Root scripts (referenced by skill evidence): `cross_model.py`, `p2_content_classifier.py`, `reliability.py`, `aggregate_codings.py`.
- `reports/` — earlier topic-analysis reports (AI-ECG, LBBAP, CSP, journal-volume — unrelated to the skills).
- `archive/` — one-off scripts and prompt dumps from the build process.

## Skills
- `/ep-title-advisor` — Generate manuscript titles tailored to specific EP journals based on 7267-article analysis (6 journals)
- `/ep-abstract-advisor` — Write/polish/place abstracts using a universal content engine + journal-fit layer, based on a dual-model (Claude+Codex) blind-coded analysis of 1,677 abstracts (6 journals). Key finding: no journal-specific writing recipe (content overlaps ≥86% per dimension, dual-model); journals differ by scope, not style. Analysis: `摘要深度分析_内容层.md`.
