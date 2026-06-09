# -*- coding: utf-8 -*-
"""Inter-coder reliability: coder1 (coded_*.json) vs coder2 (rel_coded_*.json)
on the 87-abstract stratified sample. Reports raw agreement and Cohen's kappa
per dimension, plus the main disagreements for the subjective dimensions.
"""
import json, os, glob
from collections import Counter, defaultdict

D = 'data'
sample = set(json.load(open(os.path.join(D, 'rel_sample_ids.json'))))
jmap = {int(k): v for k, v in json.load(open(os.path.join(D, 'id_journal_map.json'))).items()}

def load(globpat):
    rec = {}
    for f in glob.glob(os.path.join(D, globpat)):
        try:
            for r in json.load(open(f, encoding='utf-8')):
                rec[r['id']] = r
        except Exception as e:
            print('PARSE FAIL', os.path.basename(f), str(e)[:60])
    return rec

c1 = load('codings/coded_*.json')
c2 = load('rel_codings/rel_coded_*.json')

DIMS = ['study_type','gap_type','opening_move','contribution_frame','results_logic',
        'benchmarking','conclusion_stance','certainty_calibration','voice','external_validation']
SUBJECTIVE = {'gap_type','contribution_frame','conclusion_stance','certainty_calibration'}

ids = sorted(i for i in sample if i in c1 and i in c2)
print(f"=== RELIABILITY: {len(ids)} abstracts both-coded (sample={len(sample)}) ===")
missing = sorted(i for i in sample if i not in c2)
if missing: print(f"coder2 missing {len(missing)}: {missing}")

def kappa(pairs):
    # Cohen's kappa
    cats = set(a for a,b in pairs) | set(b for a,b in pairs)
    n = len(pairs)
    po = sum(1 for a,b in pairs if a==b)/n
    pe = 0.0
    ca = Counter(a for a,b in pairs); cb = Counter(b for a,b in pairs)
    for c in cats:
        pe += (ca[c]/n)*(cb[c]/n)
    return po, (po-pe)/(1-pe) if pe<1 else 1.0

def interp(k):
    return ('almost perfect' if k>=.81 else 'substantial' if k>=.61 else
            'moderate' if k>=.41 else 'fair' if k>=.21 else 'slight/poor')

print(f"\n{'dimension':<24}{'agree%':>8}{'kappa':>8}  interpretation   {'[subjective]'}")
results={}
for dim in DIMS:
    pairs=[(c1[i].get(dim), c2[i].get(dim)) for i in ids]
    po,k=kappa(pairs)
    results[dim]=(po,k)
    tag='  <-- subjective' if dim in SUBJECTIVE else ''
    print(f"{dim:<24}{round(100*po):>7}%{k:>8.2f}  {interp(k):<16}{tag}")

# overall subjective vs objective
subj=[results[d][1] for d in DIMS if d in SUBJECTIVE]
obj=[results[d][1] for d in DIMS if d not in SUBJECTIVE]
print(f"\nmean kappa  subjective={sum(subj)/len(subj):.2f}   objective={sum(obj)/len(obj):.2f}")

# disagreement detail for subjective dims
print("\n=== DISAGREEMENTS on subjective dimensions ===")
for dim in sorted(SUBJECTIVE):
    dis=[(i,jmap.get(i),c1[i].get(dim),c2[i].get(dim)) for i in ids if c1[i].get(dim)!=c2[i].get(dim)]
    print(f"\n{dim}: {len(dis)}/{len(ids)} disagree")
    conf=Counter((a,b) for i,j,a,b in dis)
    for (a,b),n in conf.most_common(6):
        print(f"   {a}  ->  {b}   (x{n})")
