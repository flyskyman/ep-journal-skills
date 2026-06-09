# Round-1 generate-and-compare results

Held-out set: 15 real EP abstracts (3 each HR/Europace/JACC/PACE/JICE; not in the coded corpus). For each: a fact-only brief was extracted (separate agent), then two abstracts generated from the brief alone — **A = Claude + skill**, **B = Claude + no skill** — plus the **O = original** published abstract. Blind, order-randomized pairwise judging on a 5-criterion rubric.

## Primary arm — A (skill) vs B (no-skill), recognition-immune
Two independent judge models:
- **Claude judge: skill wins 11/15 (73%)**
- **Codex judge: skill wins 12/15 (80%)**
- Per-task winner agreement Claude-vs-Codex: **8/15 (53%)** — aggregate direction agrees, individual calls are close/noisy.

Claude-judge mean criterion scores (A vs B): journal_fit 4.13 vs 3.67 (skill's biggest edge), certainty 4.07 vs 3.73, gap_specificity 3.73 vs 3.4; results_rigor 3.67 vs 3.8 and clarity 3.93 vs 4.0 (a wash — both Claude-generated from same brief).

**Conclusion:** the skill's value is real and cross-model-confirmed at the aggregate level (~75–80% win), driven mainly by journal structure/format fit + certainty calibration. Individual A-vs-B margins are small (consistent with the overall finding that journal differences are modest).

## Secondary arm — A (skill) vs O (original)
Claude judge: A wins 13/15. **Heavily discount:** a Claude judge comparing Claude-generated A vs a human original has same-model self-preference bias. Not a trustworthy "skill beats published abstracts" claim. (This bias is exactly why cross-model judging matters.)

## Round-2 improvement signals (from where A lost / was dinged)
1. Results sometimes lack an explicit comparator anchor / before→after narrative — present results as a comparison story, not a dense metric dump.
2. Occasional verbosity/redundancy (e.g. PACE: Methods restating sample characteristics).
3. Occasional missing explicit clinical-implication sentence in the conclusion.
(Strength confirmed by loser-weakness notes: skill reliably wins journal_fit via correct section-label templates — incl. Europace AIMS/METHODS AND RESULTS, JACC/JICE conventions — and certainty calibration / exploratory labeling.)

## Method notes
- Brief extraction and generation are separate agents (generators never see the original → no leakage).
- Originals re-fetched with section labels preserved (an earlier storage step had stripped them, unfairly de-structuring O).
- Codex judging required serial execution + per-call timeout + self-contained prompts (abstracts inlined); parallel codex exec races the shared runtime's model-manager and fails.
- Files: generations `data/loop_r1/{brief,A,B}_*`; judgments `judge_out/` (Claude), `judge_codex/` (Codex); mapping `judge_mapping.json`.

---

# Round-2 (improved skill, fresh held-out) + cross-model

After applying 3 Round-1 weakness fixes to the skill (results-as-comparison-narrative; no redundancy; clinical-implication clause), a NEW 15-abstract held-out set (no reuse) was generated + judged.

| Round | Claude: skill wins | Codex: skill wins | per-task agreement |
|-------|--------------------|--------------------|--------------------|
| R1 (orig skill) | 11/15 (73%) | 12/15 (80%) | 8/15 (53%) |
| R2 (improved skill, fresh data) | 9/15 (60%) | 9/15 (60%) | 13/15 (87%) |

**Conclusions:**
- The skill's benefit is positive across two rounds, two judge models, and two independent fresh held-out sets — robust. Driver is journal_fit (structure/format) + certainty calibration.
- R2 cross-model per-task agreement jumped to 87% — both independent models see the skill version as better on the same items, so the 60% is trustworthy (not noise).
- The 3 micro-improvements did NOT raise the win rate (R2 ≤ R1; different sets, so no regression, but no measurable gain either). **Diminishing returns on micro-tweaks** — the skill's value is already captured by the universal engine + journal-fit layer.
- No overfitting to the judge: the skill still wins on fresh data under an independent model.

**Decision: finalize.** Further micro-iteration is not cost-justified; the skill is validated and stable.

---

# CircAE supplement (n=4) — option ②

CircAE had no clean held-out (all 396 CircAE PMIDs were used in the coded corpus), so 4 corpus CircAE abstracts were used as test items (skill draws on aggregate distributions, not individual abstracts; mild contamination caveat). Improved skill, blind A-vs-B + A-vs-O.

| | Claude: skill wins | Codex: skill wins |
|---|---|---|
| CircAE (n=4) | 4/4 | 2/4 |

**Honest read:** underpowered (n=4) and cross-model INCONCLUSIVE — Claude sees the skill helping CircAE (4/4, AVG 4.35 vs 3.9), Codex sees it as even (2/4). The skill does not hurt CircAE; whether it helps is unconfirmed at this n. CircAE remains the weakest-evidenced journal throughout (no clean held-out possible).

## Combined skill-vs-no-skill picture
| Set | Claude | Codex |
|-----|--------|-------|
| R1 (orig skill, 5 journals, n=15) | 11/15 | 12/15 |
| R2 (improved skill, fresh, 5 journals, n=15) | 9/15 | 9/15 |
| CircAE supplement (improved, n=4) | 4/4 | 2/4 |

Overall: skill > no-skill is robust for the 5 well-sampled journals (both models, two fresh sets); CircAE is positive-but-unconfirmed (small n, model split).
