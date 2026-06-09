# -*- coding: utf-8 -*-
"""Deep quantitative analysis of 613 EP-journal abstracts.

Outputs data/abstract_deep.json and prints a console summary.
Grounds the ep-abstract-advisor skill profiles in measurable features.
"""
import csv, re, json, statistics
from collections import Counter

FILES = {
    'heart_rhythm': 'hr_abstracts.csv',
    'circ_ae':      'circ_ae_abstracts.csv',
    'europace':     'europace_abstracts.csv',
    'jacc_ep':      'jacc_ep_abstracts.csv',
    'pace':         'pace_abstracts.csv',
    'jice':         'jice_abstracts.csv',
}
NAMES = {
    'heart_rhythm':'Heart Rhythm','circ_ae':'Circ AE','europace':'Europace',
    'jacc_ep':'JACC EP','pace':'PACE','jice':'JICE',
}

# Section-header regex (structured abstracts): "Background:", "METHODS:", "Aims —"
HEADERS = ['background','aims','aim','objective','objectives','introduction',
           'methods','method','materials and methods','results','findings',
           'conclusion','conclusions','discussion','purpose']
HEADER_RE = re.compile(r'(?im)^\s*(' + '|'.join(re.escape(h) for h in HEADERS) +
                       r')\s*[:\-—–]')

P_RE   = re.compile(r'[pP]\s*[<>=≤≥]\s*\.?\d')        # p-values
CI_RE  = re.compile(r'\b(95%\s*CI|confidence interval)\b', re.I)
EFF_RE = re.compile(r'\b(HR|OR|RR|aOR|aHR|hazard ratio|odds ratio|risk ratio)\b')
AUC_RE = re.compile(r'\b(AUC|AUROC|C-statistic|c-index|area under)\b', re.I)
NUM_RE = re.compile(r'\d')

OPENERS = {
    'we_hypothesized':   re.compile(r'\bwe hypothesi[sz]ed\b', re.I),
    'we_aimed':          re.compile(r'\bwe aimed\b', re.I),
    'aim_of_study':      re.compile(r'\b(the )?(aim|purpose|objective|goal) of (this|the|our) (study|analysis|work)\b', re.I),
    'this_study_aimed':  re.compile(r'\bthis study (aimed|sought)\b', re.I),
    'sought_to':         re.compile(r'\bsought to\b', re.I),
    'we_investigated':   re.compile(r'\bwe (investigated|evaluated|assessed|examined|sought)\b', re.I),
    'however_gap':       re.compile(r'\bhowever\b', re.I),
    'remains_unclear':   re.compile(r'\b(remains?|are) (unclear|unknown|limited|elusive|poorly understood|not.{0,15}established)\b', re.I),
}
CONCL_CUES = {
    'may':        re.compile(r'\bmay\b', re.I),
    'warranted':  re.compile(r'\b(warrant|warranted|further|larger studies|future studies|needed to confirm)\b', re.I),
    'feasible':   re.compile(r'\b(feasible|feasibility|safe and effective|safe and feasible)\b', re.I),
    'superior':   re.compile(r'\b(superior|outperform|better than|improved|significantly)\b', re.I),
    'associated': re.compile(r'\b(associated with|predictor of|independent predictor)\b', re.I),
}

STOP = set('the a an of in to for and or with is are was were be been on by as at from that this these those we our study patients results methods conclusion conclusions background aims aim p ci vs versus using used between within group groups compared comparison both during after before than which who had has have not no all may also more most can than into per its their than such other each i ii'.split())

def load(path):
    rows=[]
    with open(path, encoding='utf-8-sig') as fh:
        for x in csv.DictReader(fh):
            x={k.strip().strip('"').lower():(v or '') for k,v in x.items()}
            ab=x.get('abstract','').strip()
            # exclude missing-abstract placeholders and short fragments (editorials/letters w/o real abstract)
            if ab and ab.upper()!='N/A' and len(ab.split())>=40:
                rows.append(x)
    return rows

def sentences(t):
    # split on sentence terminators not preceded by common abbreviations
    t=re.sub(r'\s+',' ',t)
    parts=re.split(r'(?<=[.!?])\s+(?=[A-Z(])', t)
    return [s for s in parts if len(s.split())>2]

def first_sentence(t):
    s=sentences(t)
    return s[0] if s else ''

def last_sentence(t):
    s=sentences(t)
    return s[-1] if s else ''

results={}
for key,fn in FILES.items():
    rows=load(fn)
    wc=[]; sc=[]; hits={'p':0,'ci':0,'eff':0,'auc':0}
    structured=0; numeric_results=0
    opener=Counter(); concl=Counter()
    words=Counter(); bigrams=Counter()
    first_words=Counter()
    for x in rows:
        ab=x['abstract'].strip()
        toks=ab.split()
        wc.append(len(toks))
        sents=sentences(ab)
        sc.append(len(sents))
        if HEADER_RE.search(ab): structured+=1
        if P_RE.search(ab): hits['p']+=1
        if CI_RE.search(ab): hits['ci']+=1
        if EFF_RE.search(ab): hits['eff']+=1
        if AUC_RE.search(ab): hits['auc']+=1
        fs=first_sentence(ab); ls=last_sentence(ab)
        for nm,rx in OPENERS.items():
            # search openers in first 2 sentences
            if rx.search(' '.join(sents[:2])): opener[nm]+=1
        for nm,rx in CONCL_CUES.items():
            if rx.search(' '.join(sents[-2:])): concl[nm]+=1
        # first word of abstract
        m=re.match(r'\s*([A-Za-z\-]+)', ab)
        if m: first_words[m.group(1).lower()]+=1
        # content word freq
        cw=[w.lower() for w in re.findall(r"[A-Za-z][A-Za-z\-]+", ab)]
        cw=[w for w in cw if w not in STOP and len(w)>2]
        words.update(cw)
        for i in range(len(cw)-1):
            bg=cw[i]+' '+cw[i+1]
            bigrams[bg]+=1
    n=len(rows)
    results[key]={
        'name':NAMES[key],'n':n,
        'words':{'mean':round(statistics.mean(wc),1),'median':int(statistics.median(wc)),
                 'p25':int(statistics.quantiles(wc,n=4)[0]) if n>3 else min(wc),
                 'p75':int(statistics.quantiles(wc,n=4)[2]) if n>3 else max(wc),
                 'min':min(wc),'max':max(wc)},
        'sentences':{'mean':round(statistics.mean(sc),1),'median':int(statistics.median(sc))},
        'structured_pct':round(100*structured/n,1),
        'stat_pct':{k:round(100*v/n,1) for k,v in hits.items()},
        'openers_pct':{k:round(100*v/n,1) for k,v in opener.most_common()},
        'conclusion_cues_pct':{k:round(100*v/n,1) for k,v in concl.most_common()},
        'top_words':[w for w,_ in words.most_common(25)],
        'top_bigrams':[b for b,c in bigrams.most_common(20) if c>=3],
        'first_word_top':[w for w,_ in first_words.most_common(8)],
    }

with open('abstract_deep.json','w',encoding='utf-8') as fh:
    json.dump(results,fh,ensure_ascii=False,indent=2)

# console summary
print(f"{'Journal':<14}{'n':>4}{'words(med/IQR)':>20}{'sent':>6}{'struct%':>9}{'p%':>6}{'CI%':>6}{'eff%':>6}{'AUC%':>6}")
for k,r in results.items():
    w=r['words']; s=r['stat_pct']
    print(f"{r['name']:<14}{r['n']:>4}{str(w['median'])+' ['+str(w['p25'])+'-'+str(w['p75'])+']':>20}"
          f"{r['sentences']['median']:>6}{r['structured_pct']:>9}{s['p']:>6}{s['ci']:>6}{s['eff']:>6}{s['auc']:>6}")
print('\n=== Openers (% of abstracts, top 4 each) ===')
for k,r in results.items():
    top=list(r['openers_pct'].items())[:4]
    print(f"{r['name']:<12}", ', '.join(f'{a}={b}%' for a,b in top))
print('\n=== Conclusion cues (top 4 each) ===')
for k,r in results.items():
    top=list(r['conclusion_cues_pct'].items())[:4]
    print(f"{r['name']:<12}", ', '.join(f'{a}={b}%' for a,b in top))
print('\n=== Top bigrams ===')
for k,r in results.items():
    print(f"{r['name']:<12}", '; '.join(r['top_bigrams'][:8]))
