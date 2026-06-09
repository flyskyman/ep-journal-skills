---
name: ep-title-advisor
description: Generate and recommend manuscript titles tailored to specific EP (electrophysiology) journals. Use when user wants to craft a title for Heart Rhythm, Circulation Arrhythmia and Electrophysiology, Europace, JACC Clinical Electrophysiology, PACE, or JICE. Trigger when user mentions writing a paper title, choosing a journal, or asking for title suggestions for EP manuscripts.
---

# EP Journal Title Advisor

Generate manuscript titles matched to a target EP journal's style, and recommend the best-fit journal. Per-journal title profiles (length, structure, patterns, examples) live in **`references/journal-profiles.md`** — read it for the target journal before generating.

## When to use
- The user wants a manuscript title for an EP journal, or to compare title styles
- The user asks "what title would work for [journal]?" or which journal to target

## Step 1 — Gather
Target journal (or offer to recommend, see table below); research topic; study type (RCT / observational / meta-analysis / case report / editorial / basic science); key finding (one sentence); study acronym (if any); sample size / data source (if relevant).

## Step 2 — Generate titles

**The title's job is to convey the specific contribution. A strong model already nails journal style, so style is NOT where titles are won or lost — information content is. Lead with substance; treat style as the container.** (Internal pilot, n=15 cross-model: a style-first version *tied* a no-skill baseline; leading with specifics won (18/12). Treat as a heuristic, not a powered result — see `references/journal-profiles.md`.)

### 2a. Lead with the high-value specifics (this is the decisive step)
A title beats its rivals by naming the things readers scan for. Pick the **2–3 MOST decision-relevant** of these and lead with them — do NOT cram in all of them (an over-stuffed title loses clarity):
- **The key finding or the exact outcomes measured** — not just the topic. "Acute success and AV-block risk" beats "a registry analysis"; "bleeding *and mortality*" beats "bleeding".
- **The intervention and its comparator — name both arms** ("A versus B").
- **The device / technique / study by name** ("LAmbre device", "pentaspline", "BEAT PAROX-AF").
- **Population**, and where notable, **cohort size / design** (RCT, registry, n).
- **Priority rule:** keep a concrete specific over a style convention — but choose the few specifics that most distinguish *this* study, and if the title gets crowded or hard to read, cut the least-decision-relevant one. **Informative AND clean beats stuffed.**

### 2b. Then fit the journal (constraint, not goal) — see `references/journal-profiles.md`
- Length (JACC ~12 words → Europace ~16), colon subtitle, sentence-case for Europace, named-study format, impersonal phrasing, journal vocabulary.
- **Question-format titles are rare — only for genuine editorials/commentaries. Do NOT use a question for original research** (even at JACC; a declarative title that states the finding wins).
- **Scope/fit**: signal the study *belongs* in this journal (Circ AE → mechanism/preclinical; JICE → technique head-to-head/procedural; Europace → comparison/synthesis/registry; JACC → quantitative clinical; PACE → feasibility/device/case/meta; HR → broad actionable finding).

### 2c. Produce 5–8 candidates, then recommend
Vary which specifics lead. **Recommend the most *informative* candidate that still fits the journal's length/style** — not the most stylish one. Self-check each: does it name the finding/outcomes, both arms, the named entity, and the design? If a rival no-skill title would be more specific, yours isn't done.

## Step 3 — Output
Group by journal; for each title add one line: structure type | why it fits. If no journal was specified, generate for all six and flag the best-fit (use the table below).

## Step 4 — Refine
Ask which the user likes; offer to combine elements; adjust length/tone/structure; if useful, search PubMed for recent example titles from the target journal.

## Cross-journal recommendation (if unsure where to submit)
| Study type | Best fit |
|-----------|----------|
| PFA clinical trial | Circ AE > HR |
| AF ablation observational | HR > Europace |
| Ablation technique comparison | JICE > Europace |
| VT/VA study | JACC EP > HR |
| Pacing/CIED | PACE > HR |
| CSP/LBBP | HR > PACE > JICE |
| CSP comparison study | JICE > Europace |
| Meta-analysis | PACE > JICE > Europace |
| Case report | PACE > JACC EP |
| AI/ML in EP | Circ AE > Europace |
| Mapping/catheter technology | JICE > HR |
| European registry | Europace |
| Channelopathy/genetics | HR > JACC EP |
| Guidelines/consensus | HR |

---
Supporting material (not inlined here): `references/journal-profiles.md` (per-journal title detail). Title metrics derive from a 7,267-article title analysis (2023–2026); treat percentages as directional.
