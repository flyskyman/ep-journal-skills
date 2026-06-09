# -*- coding: utf-8 -*-
"""Stage A: build a balanced, topic-representative abstract corpus.

Circ AE: all PMIDs. Other 5 journals: deterministic random sample of 450 PMIDs.
Fetch abstracts from NCBI efetch (XML), preserving structured-section labels.
Output: data/corpus_v2.json  (list of {id, journal, year, title, abstract, structured})
"""
import csv, json, time, random, urllib.request, urllib.parse, os
import xml.etree.ElementTree as ET
from collections import Counter

FILES = {'HR':'data/heart_rhythm.csv','CircAE':'data/circ_ae.csv','Europace':'data/europace.csv',
         'JACC':'data/jacc_ep.csv','PACE':'data/pace.csv','JICE':'data/jice.csv'}
SAMPLE_PER = 450          # PMIDs sampled per non-CircAE journal (CircAE = all)
random.seed(42)           # reproducible

# ---- 1. select PMIDs ----
pmid_journal = {}
for j, f in FILES.items():
    with open(f, encoding='utf-8-sig') as fh:
        rows = [r for r in csv.DictReader(fh)]
    pmids = [ (r.get('PMID') or r.get('﻿PMID') or '').strip() for r in rows ]
    pmids = [p for p in pmids if p.isdigit()]
    if j != 'CircAE' and len(pmids) > SAMPLE_PER:
        pmids = random.sample(pmids, SAMPLE_PER)
    for p in pmids:
        pmid_journal[p] = j
allpmids = list(pmid_journal)
print(f"selected {len(allpmids)} PMIDs:", Counter(pmid_journal.values()))

# ---- 2. fetch in batches (XML) ----
def efetch(batch):
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    data = urllib.parse.urlencode({'db':'pubmed','id':','.join(batch),'retmode':'xml'}).encode()
    req = urllib.request.Request(url, data=data, headers={'User-Agent':'ep-journal-analysis/1.0'})
    for attempt in range(4):
        try:
            return urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:
            if attempt == 3: raise
            time.sleep(2*(attempt+1))

def parse(xmlbytes):
    out = {}
    root = ET.fromstring(xmlbytes)
    for art in root.iter('PubmedArticle'):
        pmid = art.findtext('.//PMID')
        title = ''.join(art.find('.//ArticleTitle').itertext()) if art.find('.//ArticleTitle') is not None else ''
        year = art.findtext('.//PubDate/Year') or art.findtext('.//ArticleDate/Year') or ''
        segs = []; labels = []
        for ab in art.findall('.//Abstract/AbstractText'):
            lbl = ab.get('Label')
            txt = ''.join(ab.itertext()).strip()
            if txt:
                segs.append(txt);
                if lbl: labels.append(lbl)
        abstract = ' '.join(segs)
        out[pmid] = {'title':title.strip(),'year':year,'abstract':abstract,'structured':len(labels)>=2}
    return out

records = {}
B = 150
batches = [allpmids[i:i+B] for i in range(0, len(allpmids), B)]
for bi, batch in enumerate(batches, 1):
    try:
        records.update(parse(efetch(batch)))
    except Exception as e:
        print(f"batch {bi} FAILED: {repr(e)[:120]}")
    print(f"  batch {bi}/{len(batches)} done, cumulative parsed={len(records)}")
    time.sleep(0.4)

# ---- 3. assemble + filter real abstracts ----
corpus = []
i = 0
for p, j in pmid_journal.items():
    r = records.get(p)
    if not r: continue
    ab = r['abstract'].strip()
    if ab and ab.upper() != 'N/A' and len(ab.split()) >= 40:
        i += 1
        corpus.append({'id':i,'pmid':p,'journal':j,'year':r['year'],
                       'title':r['title'],'abstract':ab,'structured':r['structured']})
json.dump(corpus, open('data/corpus_v2.json','w',encoding='utf-8'), ensure_ascii=False)
print(f"\nREAL abstracts: {len(corpus)}")
print("per journal:", Counter(c['journal'] for c in corpus))
print("structured %:", {j: round(100*sum(1 for c in corpus if c['journal']==j and c['structured'])/max(1,sum(1 for c in corpus if c['journal']==j))) for j in FILES})
