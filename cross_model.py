# -*- coding: utf-8 -*-
"""Cross-model validation: Claude (codings_v2) vs Codex (codings_codex).
Per-dimension agreement + Cohen's kappa over all both-coded abstracts, and a
check that the 'journals overlap >=86%' content finding reproduces under Codex.

Hardened: detects duplicate ids, out-of-enum labels, None values, unmatched ids,
skewed-marginal kappa instability; no silent fallbacks.
"""
import json, glob, sys
from collections import Counter

D = 'data'
with open(D+'/id_journal_map_v2.json') as fh:
    jmap = {int(k): v for k, v in json.load(fh).items()}
J = ['HR','CircAE','Europace','JACC','PACE','JICE']
DIMS = ['study_type','gap_type','contribution_frame','results_logic','benchmarking',
        'conclusion_stance','certainty_calibration','voice','external_validation']
ALLOWED = {
 'study_type':{'original_clinical','original_preclinical_basic','ai_ml','meta_analysis_review','case_report_series','other'},
 'gap_type':{'mechanistic_deficit','comparative_unknown','capability_gap','guideline_inadequacy','feasibility_in_niche','optimization_unknown','prevalence_or_characterization','literature_void_weak','no_clear_gap'},
 'contribution_frame':{'mechanism_insight','realworld_scale_evidence','validated_ai_capability','clinical_decision_change','comparative_effectiveness','procedural_refinement','evidence_synthesis_meta','feasibility_safety_demo','prognostic_predictor'},
 'results_logic':{'effectsize_comparator_ci','p_value_only','discriminator_threshold_roc','noninferiority','meta_pooled_effect','descriptive_only'},
 'benchmarking':{'vs_guideline_standard','vs_alternative_technique','vs_baseline_prepost','vs_existing_model','none'},
 'conclusion_stance':{'decisive_clinical','mechanistic_elevation','translational_honest','practical_modest','exploratory_hypothesis_generating','null_finding_neutral'},
 'certainty_calibration':{'matches_design','overclaims','underclaims'},
 'voice':{'first_person_we','impersonal'},
 'external_validation':{'external','internal_only','not_applicable'},
}

def load(globpat, src):
    rec = {}; dup = 0; rows = 0; bad = Counter()
    files = glob.glob(globpat)
    for f in files:
        try:
            with open(f, encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception as e:
            print(f"  [{src}] PARSE FAIL {f}: {str(e)[:70]}"); continue
        arr = data['codings'] if isinstance(data, dict) and 'codings' in data else data
        for r in arr:
            rid = r.get('id')
            if rid is None:
                print(f"  [{src}] row without id in {f}"); continue
            rows += 1
            if rid in rec: dup += 1
            rec[rid] = r
            for dim in DIMS:
                v = r.get(dim)
                if v is not None and v not in ALLOWED[dim]:
                    bad[(dim, v)] += 1
    print(f"[{src}] files={len(files)} rows={rows} unique_ids={len(rec)} duplicate_ids={dup}")
    if dup: print(f"  WARNING [{src}] {dup} duplicate ids (silent overwrite) — join may be invalid")
    for (dim, v), n in bad.most_common(10):
        print(f"  WARNING [{src}] out-of-enum {dim}={v!r} x{n}")
    return rec

print("=== LOAD + INTEGRITY ===")
claude = load(D+'/codings_v2/coded_*.json', 'claude')
codex  = load(D+'/codings_codex/codex_*.json', 'codex')
ids = sorted(set(claude) & set(codex))
only_c = set(claude) - set(codex); only_x = set(codex) - set(claude)
print(f"\nboth-coded={len(ids)}  claude-only={len(only_c)}  codex-only={len(only_x)}")
print(f"codex completeness: {len(codex)} / {len(claude)} claude ids "
      f"({round(100*len(ids)/max(1,len(claude)))}% of claude both-coded)")
if not ids:
    print("no overlap yet — run again after Codex produces output."); sys.exit(0)

def kappa(pairs):
    pairs = [(a,b) for a,b in pairs if a is not None and b is not None]
    n = len(pairs)
    if n == 0: return 0.0, 0.0, 0, 0.0
    cats = set(a for a,_ in pairs) | set(b for _,b in pairs)
    po = sum(1 for a,b in pairs if a==b)/n
    ca = Counter(a for a,_ in pairs); cb = Counter(b for _,b in pairs)
    pe = sum((ca[c]/n)*(cb[c]/n) for c in cats)
    k = (po-pe)/(1-pe) if pe < 1 else 1.0
    # skew: modal-category share of the union (kappa unstable if very high)
    skew = max(max(ca.values()), max(cb.values()))/n
    return po, k, n, skew
def interp(k): return 'almost perfect' if k>=.81 else 'substantial' if k>=.61 else 'moderate' if k>=.41 else 'fair' if k>=.21 else 'poor'

print(f"\n=== PER-DIMENSION AGREEMENT (n both-coded, None-filtered) ===")
print(f"{'dimension':<24}{'n':>6}{'agree%':>8}{'kappa':>8}  interpretation")
ksum=0; kn=0
for dim in DIMS:
    pairs=[(claude[i].get(dim), codex[i].get(dim)) for i in ids]
    po,k,n,skew=kappa(pairs); ksum+=k; kn+=1
    flag='  (skewed marginals -> read agree%, kappa unstable)' if skew>0.9 else ''
    nflag='' if n==len(ids) else f'  [{len(ids)-n} None dropped]'
    print(f"{dim:<24}{n:>6}{round(100*po):>7}%{k:>8.2f}  {interp(k)}{flag}{nflag}")
print(f"\nmean kappa: {ksum/kn:.2f}")

# reproduce the journal-specificity (avg TVD vs pooled) under BOTH models
def dist(rec, idset, dim):
    vals=[rec[i].get(dim) for i in idset if rec[i].get(dim) is not None]
    c=Counter(vals); n=len(vals)
    return {k:v/n for k,v in c.items()} if n else {}
def tvd(p,q):
    keys=set(p)|set(q); return 0.5*sum(abs(p.get(k,0)-q.get(k,0)) for k in keys)
MIN_N = 20  # journals with fewer both-coded abstracts are excluded (empty/tiny dist => meaningless TVD)
jn = Counter(jmap.get(i) for i in ids)
present = [j for j in J if jn.get(j,0) >= MIN_N]
skipped = [(j, jn.get(j,0)) for j in J if jn.get(j,0) < MIN_N]
print(f"\n=== journal-specificity (avg TVD vs pooled over journals with n>={MIN_N}) ===")
if skipped:
    print(f"  EXCLUDED (insufficient n): {skipped}  -> TVD computed over {present}")
    print(f"  NOTE: partial Codex run; rerun after 140/140 for the full 6-journal result.")
print(f"{'dimension':<24}{'Claude':>9}{'Codex':>9}")
for dim in DIMS:
    o={}
    for src,rec in [('Claude',claude),('Codex',codex)]:
        pooled=dist(rec,[i for i in ids if jmap.get(i) in present],dim)
        tv=[tvd(dist(rec,[i for i in ids if jmap.get(i)==j],dim),pooled) for j in present]
        o[src]=sum(tv)/len(present) if present else float('nan')
    print(f"{dim:<24}{o['Claude']:>9.3f}{o['Codex']:>9.3f}")
print("\nTVD ~0.1 => ~90% distributional overlap. If both models stay <~0.15 on every dim,")
print("the 'no journal-specific writing recipe' conclusion is model-robust.")
