# -*- coding: utf-8 -*-
"""Mechanical linter for an EP-journal abstract draft.

Usage: python lint.py <JOURNAL> <abstract.txt>
  JOURNAL in: HR CircAE Europace JACC PACE JICE

Checks the objective, countable things (word count vs the journal's range, section
structure, voice, weak-gap clichés, results rigor markers, overclaim words,
redundancy). It does NOT judge semantic quality — gap specificity, whether the
aim matches the methods, and certainty-vs-design are LLM judgments the skill makes
on top of this. Output is a flag list; treat flags as prompts to check, not verdicts.
"""
import sys, re

# Per-journal targets (full-corpus medians; conditional on sampled topic mix — directional)
T = {
 'HR':      {'wmed':256,'lo':246,'hi':270,'struct':91,'imp':80,'labels':'BACKGROUND / OBJECTIVE / METHODS / RESULTS / CONCLUSION'},
 'CircAE':  {'wmed':281,'lo':258,'hi':303,'struct':96,'imp':62,'labels':'BACKGROUND / METHODS / RESULTS / CONCLUSIONS (+REGISTRATION for trials)'},
 'Europace':{'wmed':252,'lo':241,'hi':267,'struct':86,'imp':76,'labels':'AIMS / METHODS AND RESULTS / CONCLUSION (Methods+Results combined)'},
 'JACC':    {'wmed':266,'lo':251,'hi':280,'struct':91,'imp':90,'labels':'BACKGROUND / OBJECTIVES / METHODS / RESULTS / CONCLUSIONS'},
 'PACE':    {'wmed':230,'lo':110,'hi':252,'struct':70,'imp':71,'labels':'BACKGROUND or INTRODUCTION / METHODS / RESULTS / CONCLUSION'},
 'JICE':    {'wmed':252,'lo':239,'hi':272,'struct':93,'imp':69,'labels':'BACKGROUND or PURPOSE / METHODS / RESULTS / CONCLUSION'},
}
ALIASES = {'circ ae':'CircAE','circae':'CircAE','jacc ep':'JACC','jaccep':'JACC','heart rhythm':'HR'}

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    j = sys.argv[1]; j = ALIASES.get(j.lower(), j)
    if j not in T:
        print(f"unknown journal '{j}' — use one of {list(T)}"); sys.exit(1)
    txt = open(sys.argv[2], encoding='utf-8').read().strip()
    t = T[j]
    flags = []; ok = []
    words = len(txt.split())

    # 1. word count
    if words < t['lo']:
        flags.append(f"SHORT: {words} words; {j} runs ~{t['wmed']} [{t['lo']}–{t['hi']}]. Likely under-developed methods/results.")
    elif words > t['hi'] + 25:
        flags.append(f"LONG: {words} words; {j} runs ~{t['wmed']} [{t['lo']}–{t['hi']}]. Trim.")
    else:
        ok.append(f"word count {words} within {j} range")

    # 2. structure (section labels)
    labels = re.findall(r'(?im)^\s*(background|introduction|aims?|objectives?|methods?(?: and results)?|results|conclusions?|purpose)\s*[:\-]', txt)
    nstruct = len(set(l.lower() for l in labels))
    if t['struct'] >= 86 and nstruct < 3:
        flags.append(f"UNSTRUCTURED: {j} original research is structured ~{t['struct']}%. Use: {t['labels']}.")
    elif nstruct >= 3:
        ok.append(f"structured ({nstruct} sections)")
        if j == 'Europace' and not re.search(r'(?i)methods and results', txt):
            flags.append("EUROPACE FORMAT: combine Methods+Results into one 'METHODS AND RESULTS' section (house style).")

    # 3. voice (JACC strongly impersonal)
    we = len(re.findall(r'\b(we|our)\b', txt, re.I))
    if j == 'JACC' and we >= 2:
        flags.append(f"VOICE: {we} first-person 'we/our'; JACC is ~90% impersonal — prefer 'this study sought to…'.")
    elif we == 0:
        ok.append("impersonal voice")

    # 4. weak-gap cliché
    if re.search(r'(?i)\b(few|limited|scarce|lack of|little is known|not been (studied|investigated|reported)|remains to be (studied|determined))\b', txt[:600]):
        flags.append("WEAK GAP: opening uses a 'few/limited studies' cliché — state a specific, falsifiable deficit instead.")

    # 5. results rigor markers
    has_p = bool(re.search(r'[pP]\s*[<>=]\s*\.?\d', txt))
    has_ci = bool(re.search(r'95%\s*CI|confidence interval', txt, re.I))
    has_eff = bool(re.search(r'\b(HR|OR|RR|aOR|aHR|hazard ratio|odds ratio|risk ratio|AUC|AUROC|mean difference|MD)\b', txt))
    has_cmp = bool(re.search(r'(?i)\b(versus|vs\.?|compared (with|to)|than|relative to)\b', txt))
    if not (has_eff or has_ci):
        flags.append("RESULTS RIGOR: no effect size / 95% CI detected — report magnitude (HR/OR/AUC/mean diff + CI), not just p-values.")
    elif not has_cmp:
        flags.append("RESULTS: numbers present but no explicit comparator (vs / compared with) — anchor results to what they're compared against.")
    else:
        ok.append("results carry effect size / comparator")

    # 6. overclaim words
    over = re.findall(r'(?i)\b(prove[ds]?|proven|causes?|caused|establishes?|definitively|for the first time ever|guarantee[ds]?)\b', txt)
    if over:
        flags.append(f"OVERCLAIM: {sorted(set(w.lower() for w in over))} — calibrate certainty to the design (esp. observational/single-center).")

    # 7. redundancy (repeated sample-size phrasing)
    n_sample = len(re.findall(r'\b\d{2,4}\s+(patients|participants|subjects)\b', txt, re.I))
    if n_sample >= 3:
        flags.append(f"REDUNDANCY: sample size stated {n_sample}× — state population/n once.")

    # report
    print(f"=== Lint: {j} | {words} words ===")
    print(f"\n[OK] {len(ok)}:")
    for o in ok: print(f"  ✓ {o}")
    print(f"\n[FLAGS] {len(flags)}:")
    for f in flags: print(f"  ⚠ {f}")
    if not flags: print("  (no mechanical flags — now check the semantic items: gap specificity, aim↔methods match, certainty↔design)")
    print(f"\nMechanical score: {len(ok)}/{len(ok)+len(flags)} checks clean. Semantic review still required (skill §1).")

if __name__ == '__main__':
    main()
