# EP Journal Title & Abstract Advisor

Two [Claude Code](https://claude.com/claude-code) **skills** that help draft and place manuscript titles and abstracts for six major electrophysiology (EP) journals — **Heart Rhythm, Circ AE, Europace, JACC: Clinical EP, PACE, JICE** — together with the empirical analysis they are built on.

All source data is **public PubMed metadata** (PMID, year, title, abstract). No patient data, no private information.

## Key finding

> There is **no journal-specific *way to write*** an EP abstract.

A dual-model blind content analysis found the six journals' abstract *content* overlaps **≥86% per dimension**; a recognition-proof content classifier predicts the journal at only **30%** (vs a 24% base rate). Journals differ by **scope** (what each publishes) plus thin formatting and JACC's impersonal voice — **not** by a distinct writing recipe. So a good skill is a *universal content engine + a journal-fit layer*, not six separate styles.

Titles differ more mechanically (length: JACC ~12.5 words → Europace ~16.4; colon use 42%→57%; question rate 3%→9.5%), but in head-to-head testing titles are won on **information content**, not style.

## The two skills

| Skill | What it does |
|-------|--------------|
| [`ep-title-advisor`](.claude/skills/ep-title-advisor/) | Generates manuscript titles for a target EP journal (info-density first, then journal fit) and recommends where to submit. |
| [`ep-abstract-advisor`](.claude/skills/ep-abstract-advisor/) | Writes / polishes / places an abstract via a 6-move content engine + journal-fit layer; ships a mechanical linter (`scripts/lint.py`). |

Each skill is lean `SKILL.md` + `references/` (per the skill-creator convention); analysis and evidence live in references, not in the operational file.

## How it was validated

1. **Corpus** — 7,267 titles + a topic-representative **1,677-abstract** corpus (2023–2026).
2. **Blind content coding** — a 13-dimension codebook, coder blind to the journal, by **two independent models** (Claude Sonnet + Codex / GPT-5.4); cross-model agreement (Cohen's κ).
3. **Recognition-proof check** — classify on coded *features*, not raw text, because frontier models memorize real published abstracts.
4. **Generate-vs-baseline** — for fresh held-out studies, generate *skill* vs *no-skill* output from a fact-only brief, then blind-judge (both models, randomized order). Abstract skill wins ~60–80% on well-sampled journals; the title skill improved 50%→60% across iterations.
5. **Cross-model red-team** — a second model audits each skill's claims against the evidence.

These are internal pilots, not powered trials — claims are calibrated to the evidence (see the docs below).

## Repository layout

```
.claude/skills/      the two finished skills (deliverables)
.claude/workflows/   fan-out workflows (coding, reliability, generate/judge loops)
data/                canonical corpus, dual-model codings, metrics, validation records, eval RESULTS.md
  corpus_csv/        raw PubMed pulls
  _intermediate/     scratch + audit trails (safe to ignore)
reports/             earlier topic-analysis reports (AI-ECG, LBBAP, CSP, journal volume)
archive/             one-off build scripts and prompt dumps
摘要深度分析_内容层.md          abstract content findings (referenced by the skill)
skills迭代方法论与经验.md       methodology + engineering lessons
```

Detailed analysis docs are in Chinese; the skills, code, and this README are in English.

## Using the skills

Place the `.claude/skills/` folders in your project (or `~/.claude/skills/`) and invoke from Claude Code:

```
/ep-title-advisor      craft a title / pick a journal
/ep-abstract-advisor   draft, polish, or place an abstract
```

---
*Built with Claude Code. Source data: public PubMed. Treat reported percentages as directional.*
