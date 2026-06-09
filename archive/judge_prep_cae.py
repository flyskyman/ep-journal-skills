# -*- coding: utf-8 -*-
"""Phase 2 prep: build blind, order-randomized judge tasks from round-1 generations.
For each hid: comparison 'AvB' (skill vs no-skill) and 'AvO' (skill vs original).
Randomizes which arm is X vs Y, records the mapping, writes a prompt file per task.
"""
import json, os, random, re
random.seed(11)
D = 'data'; L = D + '/loop_cae'
heldout = {x['hid']: x for x in json.load(open(D + '/heldout_cae.json', encoding='utf-8'))}
os.makedirs(L + '/judge_tasks', exist_ok=True)
os.makedirs(L + '/judge_out', exist_ok=True)

def norm(t):
    # light surface-anonymisation so the 'real' one isn't obvious by tells
    t = re.sub(r'\b(NCT\d+|CRD\d+|PROSPERO\s*\S+)\b', '[registration]', t, flags=re.I)
    t = re.sub(r'https?://\S+', '', t)
    t = re.sub(r'\b(Clinical ?Trial(s)? ?Registration|URL|Unique identifier)\b.*', '', t, flags=re.I)
    return t.strip()

RUBRIC = ("Score EACH abstract 1-5 on: gap_specificity (is the knowledge gap specific & falsifiable, not 'few studies'), "
          "results_rigor (primary result with effect size + comparator + CI/p, not vague), "
          "certainty_calibration (does the conclusion's strength fit the design), "
          "journal_fit (fits the target journal's typical scope/format), clarity. "
          "Then pick the better overall abstract. Judge QUALITY ONLY — do NOT try to guess which is 'the real published one'.")

mapping = {}
tasks = []
for hid, h in heldout.items():
    j = h['journal']
    pa = f'{L}/A_{hid}.txt'; pb = f'{L}/B_{hid}.txt'
    if not (os.path.exists(pa) and os.path.exists(pb)):
        print(f'skip hid {hid}: missing A/B'); continue
    A = norm(open(pa, encoding='utf-8').read())
    B = norm(open(pb, encoding='utf-8').read())
    O = norm(h['abstract'])
    for comp, second_text, second_arm in [('AvB', B, 'B'), ('AvO', O, 'O')]:
        flip = random.random() < 0.5
        if flip: x_txt, x_arm, y_txt, y_arm = second_text, second_arm, A, 'A'
        else:    x_txt, x_arm, y_txt, y_arm = A, 'A', second_text, second_arm
        tid = f'{hid}_{comp}'
        mapping[tid] = {'hid': hid, 'journal': j, 'comp': comp, 'X': x_arm, 'Y': y_arm}
        prompt = (f"You are an expert EP journal editor blindly comparing two abstracts written for the journal '{j}'. "
                  f"{RUBRIC}\n\n=== Abstract X ===\n{x_txt}\n\n=== Abstract Y ===\n{y_txt}\n\n"
                  f"Return the structured object (x_scores, y_scores, winner X/Y/tie, rationale, loser_weakness=what the weaker abstract most lacked).")
        open(f'{L}/judge_tasks/{tid}.txt', 'w', encoding='utf-8').write(prompt)
        tasks.append(tid)
json.dump(mapping, open(f'{L}/judge_mapping.json', 'w'), ensure_ascii=False, indent=1)
open(f'{L}/judge_tasklist.txt', 'w').write('\n'.join(tasks))
print(f'prepared {len(tasks)} judge tasks ({len(heldout)} hids x 2 comparisons); mapping saved')
