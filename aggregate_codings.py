# -*- coding: utf-8 -*-
"""Aggregate the 60 coded_NN.json files into per-journal distributions.

Joins blind codings with the id->journal map, validates integrity (no silent
fallback: reports missing chunks / unparseable files / unknown enum values),
prints per-journal distribution tables per dimension, and clusters novel_pattern
flags for codebook refinement (Phase 3 recursion).
"""
import json, os, glob, re
from collections import Counter, defaultdict

D = 'data'
jmap = {int(k): v for k, v in json.load(open(os.path.join(D, 'id_journal_map.json'))).items()}
JOURNALS = ['HR', 'CircAE', 'Europace', 'JACC', 'PACE', 'JICE']

DIMS = ['study_type','gap_type','opening_move','contribution_frame','results_logic',
        'benchmarking','conclusion_stance','certainty_calibration','voice','external_validation']
ALLOWED = {
 'study_type':{'original_clinical','original_preclinical_basic','ai_ml','meta_analysis_review','case_report_series','other'},
 'gap_type':{'mechanistic_deficit','comparative_unknown','capability_gap','guideline_inadequacy','feasibility_in_niche','optimization_unknown','prevalence_or_characterization','literature_void_weak','no_clear_gap'},
 'opening_move':{'premise_then_however','aim_first','hypothesis_first','trial_or_cohort_name_first','entity_definition','clinical_problem_first'},
 'contribution_frame':{'mechanism_insight','realworld_scale_evidence','validated_ai_capability','clinical_decision_change','comparative_effectiveness','procedural_refinement','evidence_synthesis_meta','feasibility_safety_demo','prognostic_predictor'},
 'results_logic':{'effectsize_comparator_ci','p_value_only','discriminator_threshold_roc','noninferiority','meta_pooled_effect','descriptive_only'},
 'benchmarking':{'vs_guideline_standard','vs_alternative_technique','vs_baseline_prepost','vs_existing_model','none'},
 'conclusion_stance':{'decisive_clinical','mechanistic_elevation','translational_honest','practical_modest','exploratory_hypothesis_generating','null_finding_neutral'},
 'certainty_calibration':{'matches_design','overclaims','underclaims'},
 'voice':{'first_person_we','impersonal'},
 'external_validation':{'external','internal_only','not_applicable'},
}

# ---- load + validate ----
records = {}          # id -> coding dict
bad_enum = defaultdict(list)
parse_fail = []
files = sorted(glob.glob(os.path.join(D, 'codings', 'coded_*.json')))
for f in files:
    try:
        arr = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        parse_fail.append((os.path.basename(f), str(e)[:80])); continue
    for r in arr:
        rid = r.get('id')
        records[rid] = r
        for dim in DIMS:
            v = r.get(dim)
            if v not in ALLOWED[dim]:
                bad_enum[dim].append((rid, v))

missing = [i for i in jmap if i not in records]
print(f"=== INTEGRITY ===")
print(f"chunk files found: {len(files)}/60")
print(f"abstracts coded: {len(records)}/414")
if parse_fail: print(f"PARSE FAILURES: {parse_fail}")
if missing: print(f"MISSING IDS ({len(missing)}): {missing[:40]}")
for dim, errs in bad_enum.items():
    if errs: print(f"INVALID {dim} ({len(errs)}): {errs[:8]}")
if not parse_fail and not missing and not any(bad_enum.values()):
    print("clean: all 414 coded, all enums valid")

# ---- per-journal distributions ----
def pct_table(dim):
    by = {j: Counter() for j in JOURNALS}
    nj = Counter()
    for rid, r in records.items():
        j = jmap.get(rid)
        if j: by[j][r.get(dim)] += 1; nj[j] += 1
    vals = sorted(ALLOWED[dim], key=lambda v: -sum(by[j][v] for j in JOURNALS))
    print(f"\n### {dim}")
    hdr = f"{'value':<34}" + ''.join(f"{j:>9}" for j in JOURNALS)
    print(hdr)
    for v in vals:
        if sum(by[j][v] for j in JOURNALS) == 0: continue
        row = f"{v:<34}"
        for j in JOURNALS:
            p = round(100*by[j][v]/nj[j]) if nj[j] else 0
            row += f"{str(p)+'%':>9}"
        print(row)

print("\n=== PER-JOURNAL DISTRIBUTIONS (% within journal) ===")
print('n per journal:', {j: sum(1 for i,r in records.items() if jmap.get(i)==j) for j in JOURNALS})
for dim in DIMS:
    pct_table(dim)

# ---- novel patterns (Phase 3 recursion input) ----
print("\n=== NOVEL PATTERNS (fits_codebook=false) ===")
novels = [(rid, jmap.get(rid), r.get('novel_pattern','')) for rid, r in records.items()
          if r.get('fits_codebook') is False and r.get('novel_pattern','').strip()]
print(f"total flagged: {len(novels)}")
# crude clustering by keyword
kw = Counter()
for rid, j, np_ in novels:
    for w in re.findall(r'[a-z]{4,}', np_.lower()):
        kw[w] += 1
print("top keywords in novel flags:", kw.most_common(20))
print("\nall novel flags:")
for rid, j, np_ in sorted(novels, key=lambda x: x[1] or ''):
    print(f"  [{j}] #{rid}: {np_}")

# ---- save aggregate ----
agg = {'n_total': len(records), 'by_journal': {}}
for j in JOURNALS:
    ids = [i for i in records if jmap.get(i)==j]
    agg['by_journal'][j] = {'n': len(ids)}
    for dim in DIMS:
        c = Counter(records[i].get(dim) for i in ids)
        agg['by_journal'][j][dim] = {k: round(100*v/len(ids)) for k,v in c.most_common()} if ids else {}
json.dump(agg, open(os.path.join(D,'abstract_codings_agg.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=2)
print("\nsaved data/abstract_codings_agg.json")
