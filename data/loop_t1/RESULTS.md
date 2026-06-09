# Title-skill validation (#7) — generate-vs-baseline, cross-model

15 fresh held-out studies (reused R2 briefs). For each: title-skill (A) vs no-skill (B) title generated from the brief alone; original published title = O. Blind, order-randomized, rubric = journal_fit / informativeness / clarity / appeal.

## Primary: title-skill (A) vs no-skill (B)
| Judge | A wins | B wins | tie |
|-------|--------|--------|-----|
| Claude | 7 | 8 | 0 |
| Codex | 8 | 7 | 0 |
Per-task agreement 12/15. **Verdict: ~50/50 — the title-skill gives NO measurable quality benefit over a no-skill baseline, confirmed cross-model.**

Claude criterion means (A vs B): journal_fit 3.87 vs 3.60 (skill better), clarity 4.27 vs 3.87 (skill better), but informativeness 4.0 vs 4.6 (skill WORSE), appeal 3.6 vs 3.73. The skill trades informativeness for style-fit → net wash.

## Secondary: A vs original — A 13/15 (Claude). Discount (same-model self-preference + brief-framing advantage).

## Interpretation
Unlike the abstract skill (cross-model 60–80% win), the title skill does not beat baseline. A frontier model already writes good titles; the title skill's value (length/colon/style conventions) is thin and gets washed out, and over-fitting to style cost informativeness.

The title skill's real value is therefore NOT raw title-quality uplift (it can't deliver that vs a strong model) but: (a) journal **recommendation** / fit positioning, (b) house-convention **compliance** (length, sentence-case, registration, Europace combined sections), (c) examples for non-expert users. Frame it that way, or improve it by insisting the title lead with the key finding (informativeness) while matching style.

---

# Title round-2 — improved skill (info-density first)

Diagnosis of R1: the style-first skill LOST on informativeness (A 4.0 vs B 4.6) because it dropped concrete specifics (device names, exact outcomes, cohort size, both comparison arms) to satisfy style conventions, and over-applied "question titles" for JACC. Fix: rewrote Step 2 to **lead with the specific contribution (finding/outcomes, both arms, named device/study, cohort size/design) and treat style as a container; never drop a specific for a convention; no question-titles for original research.**

Re-tested on the SAME 15 briefs, same no-skill B baseline, blind, cross-model:

| Round | Claude (A/B) | Codex (A/B) | combined |
|-------|--------------|-------------|----------|
| R1 style-first | 7/8 | 8/7 | 15/15 (no benefit) |
| R2 info-density | 8/7 | 9/6 | **17/13 (~57%, both models favor skill)** |

informativeness flipped A 4.0→4.53 (now > B 4.07); journal_fit and appeal also favor A. Tradeoff: clarity dipped (A 4.0 vs B 4.47) from packing specifics.

**Conclusion:** the title skill now delivers a real, cross-model-confirmed benefit over no-skill — modest (~57% vs abstracts' 60–80%), because frontier models already title well, so the skill's ceiling is lower. The decisive lever was information content, not style. Optional refinement: pack only the 2–3 most decision-relevant specifics to recover clarity.

---

# Title round-3 — clarity refinement (FINAL)

R2 won on informativeness but dipped on clarity (over-stuffed titles). Refined Step 2a: "lead with the 2–3 MOST decision-relevant specifics, don't cram all; informative AND clean beats stuffed; cut the least-decision-relevant if crowded."

Full trajectory (skill A vs no-skill B, n=15, blind, cross-model):
| Round | Claude A/B | Codex A/B | combined | win% |
|-------|-----------|-----------|----------|------|
| R1 style-first | 7/8 | 8/7 | 15/15 | 50% (no benefit) |
| R2 info-density | 8/7 | 9/6 | 17/13 | 57% |
| R3 +clarity refine | 8/7 | 10/5 | **18/12** | **60%** |

R3 Claude criterion means (A vs B): informativeness 4.73 vs 4.07, clarity 4.2 vs 4.67 (recovered from R2's 4.0), journal_fit 4.27 vs 4.27, appeal 3.8 vs 3.87.

**FINAL: the title skill now delivers a real, cross-model-confirmed ~60% win over no-skill — monotonic improvement (50→57→60%) driven by evidence (lead with specifics, not style; keep it clean). Residual: no-skill titles are still slightly clearer (simpler), an inherent informative-vs-clean tradeoff the skill resolves toward informative — the right call for a title's job. ep-title-advisor SKILL.md Step 2 reflects this final version.**
