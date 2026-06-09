# -*- coding: utf-8 -*-
import json,os,random
random.seed(11)
D='data'; L=D+'/loop_t1'
heldout={x['hid']:x for x in json.load(open(D+'/heldout_r2.json',encoding='utf-8'))}
os.makedirs(L+'/judge_tasks',exist_ok=True); os.makedirs(L+'/judge_out',exist_ok=True)
RUBRIC=("Score EACH title 1-5 on: journal_fit (length/structure/style match for the target journal — see how that journal titles papers), "
        "informativeness (conveys the key topic+finding), clarity (clean, readable, unambiguous), appeal (precise and compelling). "
        "Pick the better title overall. Judge QUALITY ONLY — do NOT guess which is the real published one.")
mapping={}; tasks=[]
for hid,h in heldout.items():
    j=h['journal']; pa=f'{L}/A_{hid}.txt'; pb=f'{L}/B_{hid}.txt'
    if not (os.path.exists(pa) and os.path.exists(pb)): print('skip',hid,'missing'); continue
    A=open(pa,encoding='utf-8').read().strip(); B=open(pb,encoding='utf-8').read().strip(); O=h['title'].strip()
    for comp,second,arm2 in [('AvB',B,'B'),('AvO',O,'O')]:
        flip=random.random()<0.5
        if flip: x,xa,y,ya=second,arm2,A,'A'
        else: x,xa,y,ya=A,'A',second,arm2
        tid=f'{hid}_{comp}'; mapping[tid]={'hid':hid,'journal':j,'comp':comp,'X':xa,'Y':ya}
        p=(f"You are an expert {j} editor blindly comparing two candidate manuscript titles for the SAME study, both intended for {j}. {RUBRIC}\n\n"
           f"=== Title X ===\n{x}\n\n=== Title Y ===\n{y}\n\nReturn the structured object.")
        open(f'{L}/judge_tasks/{tid}.txt','w',encoding='utf-8').write(p); tasks.append(tid)
json.dump(mapping,open(f'{L}/judge_mapping.json','w'),ensure_ascii=False,indent=1)
open(f'{L}/judge_tasklist.txt','w').write('\n'.join(tasks))
print('prepared',len(tasks),'title judge tasks')
