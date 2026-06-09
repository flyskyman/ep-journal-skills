# -*- coding: utf-8 -*-
"""P2 (recognition-proof): can the CODED CONTENT predict the journal?

The text-based prediction was invalid — a frontier model recognizes the real
papers (cited DOIs/exact-match). This version uses ONLY the categorical content
codes (no text => no recognition) and a transparent categorical Naive Bayes with
stratified 5-fold CV. If content barely beats baseline, journals are not
distinguishable by content => confirms 'no journal-specific writing recipe'.
Reports two conditions: with vs without study_type (the scope proxy).
"""
import json, glob, math, random
from collections import Counter, defaultdict

random.seed(0)
jmap = {int(k): v for k, v in json.load(open('data/id_journal_map_v2.json')).items()}
J = ['HR','CircAE','Europace','JACC','PACE','JICE']
ALLDIMS = ['study_type','gap_type','contribution_frame','results_logic','benchmarking',
           'conclusion_stance','certainty_calibration','voice','external_validation']

rec = {}
for f in glob.glob('data/codings_v2/coded_*.json'):
    for r in json.load(open(f, encoding='utf-8')):
        if r['id'] in jmap: rec[r['id']] = r
ids = list(rec)

def nb_cv(feature_dims, folds=5):
    # stratified folds
    byj = defaultdict(list)
    for i in ids: byj[jmap[i]].append(i)
    for j in byj: random.shuffle(byj[j])
    fold = {i: k for j in byj for k, i in enumerate([x for idx, x in enumerate(byj[j])]) }
    fold = {}
    for j in byj:
        for idx, i in enumerate(byj[j]): fold[i] = idx % folds
    correct = 0; conf = defaultdict(Counter); n = 0
    for f in range(folds):
        train = [i for i in ids if fold[i] != f]; test = [i for i in ids if fold[i] == f]
        prior = Counter(jmap[i] for i in train)
        # per-class, per-dim value counts
        cnt = {c: {d: Counter() for d in feature_dims} for c in J}
        for i in train:
            c = jmap[i]
            for d in feature_dims: cnt[c][d][rec[i].get(d)] += 1
        vocab = {d: set(rec[i].get(d) for i in ids) for d in feature_dims}
        for i in test:
            best, bestlp = None, -1e18
            for c in J:
                lp = math.log(prior[c] / len(train))
                for d in feature_dims:
                    v = rec[i].get(d)
                    num = cnt[c][d][v] + 1            # Laplace
                    den = prior[c] + len(vocab[d])
                    lp += math.log(num / den)
                if lp > bestlp: bestlp, best = lp, c
            conf[jmap[i]][best] += 1
            if best == jmap[i]: correct += 1
            n += 1
    return correct / n, conf

base = max(Counter(jmap[i] for i in ids).values()) / len(ids)
print(f"n={len(ids)}  baseline (majority class) = {round(100*base)}%   chance(1/6)=17%\n")

for label, dims in [("ALL 9 content dims", ALLDIMS),
                    ("content WITHOUT study_type (pure rhetoric)", [d for d in ALLDIMS if d != 'study_type']),
                    ("study_type ALONE (scope proxy)", ['study_type'])]:
    acc, conf = nb_cv(dims)
    print(f"== {label} ==")
    print(f"   5-fold CV accuracy = {round(100*acc)}%")
    if label.startswith("ALL"):
        print("   per-journal recall:", {j: f"{round(100*conf[j][j]/max(1,sum(conf[j].values())))}%" for j in J})
    print()

# which single dim is most predictive (1-dim NB each)
print("Single-dimension predictive power (1-feature CV accuracy):")
for d in ALLDIMS:
    acc, _ = nb_cv([d])
    print(f"   {d:<24} {round(100*acc)}%")
print(f"\nInterpretation: if accuracy stays near the ~{round(100*base)}% baseline once study_type is")
print("removed, journals are NOT distinguishable by how the abstract is written — only by what")
print("kind of study it is (scope). That confirms the skill's central claim.")
