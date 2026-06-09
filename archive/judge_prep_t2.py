# -*- coding: utf-8 -*-
import json,os,random
random.seed(11)
D='data'; L=D+'/loop_t2'
heldout={x['hid']:x for x in json.load(open(D+'/heldout_r2.json',encoding='utf-8'))}
RUBRIC=("Score EACH title 1-5 on: journal_fit, informativeness (conveys key topic+finding+specifics), clarity, appeal. "
        "Pick the better title overall. Judge QUALITY ONLY.")
mapping={}; tasks=[]
for hid,h in heldout.items():
    j=h['journal']; pa=f'{L}/A_{hid}.txt'; pb=f'{L}/B_{hid}.txt'
    if not (os.path.exists(pa) and os.path.exists(pb)): continue
    A=open(pa,encoding='utf-8').read().strip(); B=open(pb,encoding='utf-8').read().strip()
    flip=random.random()<0.5
    x,xa,y,ya=(B,'B',A,'A') if flip else (A,'A',B,'B')
    tid=f'{hid}_AvB'; mapping[tid]={'hid':hid,'journal':j,'comp':'AvB','X':xa,'Y':ya}
    p=(f"You are an expert {j} editor blindly comparing two candidate manuscript titles for the SAME study, both for {j}. {RUBRIC}\n\n=== Title X ===\n{x}\n\n=== Title Y ===\n{y}\n\nReturn the structured object.")
    open(f'{L}/judge_tasks/{tid}.txt','w',encoding='utf-8').write(p); tasks.append(tid)
json.dump(mapping,open(f'{L}/judge_mapping.json','w'),ensure_ascii=False,indent=1)
open(f'{L}/judge_tasklist.txt','w').write('\n'.join(tasks))
print('t2 judge tasks:',len(tasks))
