# EP journal title profiles

Per-journal title detail for Step 2 of the skill. **Metrics computed over all 7,267 article titles (2023–2026, six journals)** — deterministic regex counts shown as rounded percentages (source: `data/title_metrics.json`; word/char length + colon/question/versus/novelty/review/case rates). Mechanical superlatives are verified across all six; **semantic categories (case/versus/review) are regex lower bounds** (see cross-validation below).

## Verified metrics (all 7,267 titles)

| Journal | n | words (med) | chars | colon% | question% | versus% | novel% | review/meta% | case% |
|---------|---|-------------|-------|--------|-----------|---------|--------|--------------|-------|
| HR | 2166 | 14.3 (14) | 113 | 42.5 | 4.8 | 3.5 | 4.2 | 3.1 | 0.6 |
| Circ AE | 396 | 14.9 (14) | 118 | 48.2 | 3.3 | 3.8 | 6.1 | 1.5 | 0.0 |
| Europace | 1277 | 16.4 (16) | 130 | **57.2** | 4.9 | 6.4 | 3.1 | 3.6 | 0.5 |
| JACC EP | 1443 | **12.5 (13)** | 99 | 47.3 | **9.5** | 3.9 | 3.1 | 0.6 | 0.7 |
| PACE | 888 | 14.2 (14) | 110 | 41.9 | 6.4 | 5.5 | 2.4 | 6.5 | **6.6** |
| JICE | 1097 | 15.7 (15) | 124 | 47.0 | 5.1 | **7.0** | 3.6 | 7.0 | 1.5 |

**Cross-validation (Codex, independent classification of 90 titles, 15/journal):** mechanical metrics are reliable — `colon` 90/90 agreement, `question` 89/90. But the **regex undercounts the semantic categories**: `versus` (misses "compared with / A or B" phrasings), `review/meta` (misses variants like "meta-analytical"), and especially `case` — Codex found unlabeled case reports the regex scored as 0 (case titles often don't contain "case report"). So **treat case% / versus% / review% as lower bounds** (true rates higher). Mechanical rankings are verified (Europace longest + most colons; JACC shortest + most questions); semantic-category rankings (PACE highest case, JICE highest versus/review) are **provisional** — directionally supported but not independently re-counted per journal.

**What genuinely differs across journals** (real title-style signals; the companion abstract analysis separately found abstract *content* barely separates journals): title length (JACC shortest 12.5 → Europace longest 16.4), colon use (PACE 42% → Europace 57%), question titles (Circ AE 3.3% → JACC 9.5%, editorial culture), and case-report rate (lowest Circ AE 0% → highest PACE 6.6%). versus / novelty / review rates differ only mildly. (novel% = strict novelty phrases; named-study/acronym presence is method-dependent — directional only.)

## Heart Rhythm (HR)
- **Positioning**: HRS flagship; broadest scope; highest volume (~700/year)
- **Style**: 14 words / 113 chars; colon ~43% (moderate); question ~5%; named studies common; rarely case reports (0.6%). Broad topics (AF, ablation, pacing, channelopathy, devices); favors "outcomes/predictors/association/risk"; for CSP/LBBP include "left bundle branch" explicitly.
- **Patterns**: `{Topic}: {Subtitle with design/source}` · `{Finding} in {Population}: {Study Name}` (trials) · `{Descriptive key finding}` · `{Topic} — A {Study Name} Analysis`
- **Examples**:
  - "Impact of Linear Ablation in Persistent Atrial Fibrillation Using a Dual-Energy, Wide-Footprint Catheter: Analysis from the SPHERE Per-AF Randomized Trial."
  - "Trends in Ventricular Arrhythmia-Related Mortality in the United States from 1979 to 2024: A CDC WONDER Analysis."

## Circulation: Arrhythmia and Electrophysiology (Circ AE)
- **Positioning**: high-impact, selective (~130/year); technology-forward
- **Style**: 14–15 words / 118 chars; colon 48%; **fewest question titles (3.3%)**; **highest strict-novelty phrasing (6.1%)**; essentially no case reports (0%); precise, technical, mechanism-focused; favors "pulsed field/catheter/lesion/substrate".
- **Patterns**: `{Technical innovation/finding}: {Evidence source}` · `{Precise mechanistic finding} in {Context}` · `{Outcome} of {Intervention}: {Study Name}` · Title-Case, formal
- **Examples**:
  - "Variability in Tissue Interface Temperature During Pulse Field Atrial Ablation: Implications for Real-Time Contact Assessment."
  - "Epicardial-to-Endocardial Activation Gradients and Conduction Block During Atrial Fibrillation in the Human Left Atrial Posterior Wall."

## Europace
- **Positioning**: European EP flagship; long, descriptive, design-forward titles
- **Style**: **longest (16.4 words / 130 chars)** and **highest colon use (57%, near-mandatory)**; design usually in the title; European multicenter registries featured; meta-analysis/SR welcomed; comparison studies common (include both arms); favors "a systematic review/a nationwide study/a European multicenter"; sentence-case common (lowercase after colon).
- **Patterns**: `{Detailed description}: {Subtitle — method/registry/design}` · `{A} versus {B} for {Condition}: {Source}` · `{Outcome} after {Intervention} in {Population}: a {design} study` · `{Topic}: a systematic review and meta-analysis`
- **Examples**:
  - "Pulsed Field Ablation versus Thermal Ablation for Pulmonary Vein Isolation: A Network Meta-Analysis of Randomized Controlled Trials."
  - "Incidence and predictors of major arrhythmic events after myocarditis: a systematic review and meta-analysis."

## JACC: Clinical Electrophysiology (JACC EP)
- **Positioning**: JACC sub-journal; broad article types; strong editorial voice
- **Style**: **shortest (12.5 words / 99 chars)** and **highest question rate (9.5%, editorial/commentary culture)**; very few case-report titles (0.7%); short and punchy; colon subtitles use qualitative descriptors ("A Dangerous Scenario", "Lessons Learned"); Title-Case; action verbs / clinical-relevance framing.
- **Patterns**: `{Concise finding}: {Punchy subtitle}` · `{Provocative question}?` (editorials) · `{Descriptive case/image}: {Brief characterization}` · `{Short clinical message}`
- **Examples**:
  - "How Many CPVT Patients Need an ICD?: The Impact of Left Cardiac Sympathetic Denervation."
  - "J-Wave Syndromes: Reconciling the Complexity."
  - "AF Ablation and Autonomic Provocation: A New Type of Holiday Heart?"

## PACE (Pacing and Clinical Electrophysiology)
- **Positioning**: CIED/pacing specialist; practical; **the leading case-report venue (and a high review/meta venue)**
- **Style**: 14 words / 110 chars; lowest colon use (42%, more direct titles); **highest case-report rate (6.6%) and high review/meta rate (6.5%)**; straightforward clinical titles; least strict-novelty language (2.4%); favors "pacemaker/implantable/lead/cardiac resynchronization".
- **Patterns**: `{Clinical question/technique}: {Study type}` · `{Direct descriptive statement}` (no colon) · `{Device/pacing topic}: A Systematic Review and Meta-Analysis` · `{Unusual case}: A Case Report/Series`
- **Examples**:
  - "Conduction System Pacing Versus Right Ventricular Pacing in Atrioventricular Block: A Systematic Review and Meta-Analysis of Randomized Controlled Trials."
  - "Dual-Chamber Leadless Pacemaker Implants in the Young."

## JICE (Journal of Interventional Cardiac Electrophysiology)
- **Positioning**: interventional EP specialist; comparison-study hub (~250/year)
- **Style**: 15.7 words / 124 chars (second longest); **highest versus rate (7.0%)** and high review/meta rate (7.0%); comparison studies dominate (include both arms); technical/descriptive with full design; less editorial voice than JACC, more technical detail than PACE; favors "versus/compared/feasibility/safety/multicenter".
- **Patterns**: `{A} versus {B} for/in {Condition}: {Study design}` · `{Technical finding}: a {multicenter/prospective/retrospective} study` · `{Detailed intervention + outcome}` · `{Topic}: a systematic review and meta-analysis`
- **Examples**:
  - "A prospective multicenter study of left bundle branch area pacing using stylet-driven lead: insights into capture types, delivery curve selection, and procedural failure."
  - "Improved outcomes of left bundle branch pacing compared to left ventricular septal pacing in patients with heart failure: a systematic review and meta-analysis."

---
**Provenance & caveats:** metrics are deterministic regex counts over the 7,267-title corpus (`data/title_metrics.json`), shown rounded; semantic categories (case/versus/review) are lower bounds (regex misses unlabeled cases / "compared with"). Example titles are real published titles from the corpus (illustrative, not validation data). The Step-2 "information-density first" guidance rests on **internal pilot testing** (n=15 held-out, blind, cross-model: skill 18 / no-skill 12) — a heuristic supported by limited testing, not a powered trial; see `data/loop_t1/RESULTS.md`.
