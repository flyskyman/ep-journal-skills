# -*- coding: utf-8 -*-
"""Aggregate round-1 blind judge results into win rates + per-criterion means,
recovering each X/Y verdict back to its arm (A=skill, B=no-skill, O=original)."""
import json, glob, os
from collections import Counter, defaultdict

D = 'data/loop_r2'
mp = json.load(open(D + '/judge_mapping.json'))
CRIT = ['gap_specificity', 'results_rigor', 'certainty_calibration', 'journal_fit', 'clarity']

wins = defaultdict(Counter)
scores = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))  # comp -> arm -> crit -> [vals]
weaknesses = defaultdict(list)
n = Counter()
by_journal = defaultdict(lambda: Counter())

for f in glob.glob(D + '/judge_out/*.json'):
    tid = os.path.basename(f)[:-5]
    if tid not in mp:
        continue
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        print('parse fail', tid, str(e)[:50]); continue
    m = mp[tid]; comp = m['comp']; n[comp] += 1
    win_arm = m['X'] if d['winner'] == 'X' else m['Y'] if d['winner'] == 'Y' else 'tie'
    wins[comp][win_arm] += 1
    if comp == 'AvB':
        by_journal[m['journal']][win_arm] += 1
    for slot, arm in [('x_scores', m['X']), ('y_scores', m['Y'])]:
        for c in CRIT:
            scores[comp][arm][c].append(d[slot][c])
    weaknesses[comp].append((win_arm, d.get('loser_weakness', '')))

def mean(xs): return round(sum(xs) / len(xs), 2) if xs else 0

print('=== ROUND 1 JUDGE RESULTS (Codex, blind, order-randomized) ===')
for comp, label in [('AvB', 'A=skill vs B=no-skill  [PRIMARY - recognition-immune]'),
                    ('AvO', 'A=skill vs O=original  [secondary - absolute bar]')]:
    print(f'\n## {label}   n={n[comp]}')
    print('   wins:', dict(wins[comp]))
    arms = sorted(scores[comp])
    print('   mean criterion scores (1-5):')
    print('     arm  ' + ''.join(f'{c[:10]:>12}' for c in CRIT) + f'{"AVG":>8}')
    for a in arms:
        ms = [mean(scores[comp][a][c]) for c in CRIT]
        avg = round(sum(ms) / len(ms), 2) if ms else 0
        print(f'     {a:<4} ' + ''.join(f'{v:>12}' for v in ms) + f'{avg:>8}')

print('\n=== A-vs-B wins by journal ===')
for j, c in by_journal.items():
    print(f'   {j:<9} {dict(c)}')

print('\n=== loser weaknesses (skill-improvement signal, A-vs-B) ===')
for win_arm, wk in weaknesses['AvB']:
    if wk: print(f'   [winner={win_arm}] {wk}')
