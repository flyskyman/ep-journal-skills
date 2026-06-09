import csv
import re
import json
from pathlib import Path

DATA_DIR = Path(r"C:\Projects\jouranl-title\data")

JOURNALS = {
    "heart_rhythm": "Heart Rhythm",
    "circ_ae": "Circulation: Arrhythmia and Electrophysiology",
    "europace": "Europace",
    "jacc_ep": "JACC: Clinical Electrophysiology",
    "pace": "PACE",
}

CSP_PATTERNS = [
    r"\bleft bundle branch\b", r"\bLBBP\b", r"\bLBBA\b", r"\bLBB pacing\b",
    r"\bconduction system pacing\b", r"\bCSP\b",
    r"\bHis bundle\b", r"\bHis-Purkinje\b", r"\bHis pacing\b",
    r"\bhisian pacing\b", r"\bphysiologic pacing\b",
    r"\bcardiac resynchronization.*pacing\b", r"\bCRT.*pacing\b",
    r"\bbundle branch\b.*pacing", r"\bpacing.*bundle branch\b",
    r"\bseptal pacing\b", r"\bdeep septal\b",
]

AI_PATTERNS = [
    r"\bartificial intelligence\b", r"\bmachine learning\b", r"\bdeep learning\b",
    r"\bneural network\b", r"\bAI\b(?!DS|CD|V\b)", r"\bML\b",
    r"\bnatural language\b", r"\blarge language model\b", r"\bLLM\b",
    r"\bautomated.*detect\b", r"\bautomated.*classif\b", r"\bautomated.*predict\b",
    r"\bcomputer.aided\b", r"\balgorithm.*learn\b",
    r"\bconvolutional\b", r"\brandom forest\b", r"\bsupport vector\b",
    r"\bpredictive model\b", r"\brisk.*model\b.*\b(?:predict|classif)\b",
    r"\bdigital\b.*\b(?:health|twin|biomarker)\b",
    r"\bwearable\b.*\b(?:detect|monitor|algorithm)\b",
]

PFA_PATTERNS = [
    r"\bpulsed field ablation\b", r"\bPFA\b", r"\bpulsed.field\b",
    r"\bpulse field\b", r"\belectroporation\b",
]

def matches_any(title, patterns):
    for p in patterns:
        if re.search(p, title, re.IGNORECASE):
            return True
    return False

def classify(title):
    cats = []
    if matches_any(title, CSP_PATTERNS):
        cats.append("CSP/LBBAP")
    if matches_any(title, AI_PATTERNS):
        cats.append("AI/ML")
    return cats

results = {}
all_pmids = []

for fname, jname in JOURNALS.items():
    path = DATA_DIR / f"{fname}.csv"
    matched = []
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pmid = row.get("PMID", "").strip()
            year = row.get("Year", "").strip()
            title = row.get("Title", "").strip().strip('"')
            if not pmid or not title:
                continue
            if matches_any(title, PFA_PATTERNS):
                continue
            cats = classify(title)
            if cats:
                matched.append({"pmid": pmid, "year": year, "title": title, "categories": cats})
                all_pmids.append(pmid)
    results[fname] = {"journal": jname, "articles": matched, "count": len(matched)}

print("=== Filtered Articles (CSP/LBBAP + AI, excluding PFA) ===\n")
total = 0
for fname, jname in JOURNALS.items():
    r = results[fname]
    csp_count = sum(1 for a in r["articles"] if "CSP/LBBAP" in a["categories"])
    ai_count = sum(1 for a in r["articles"] if "AI/ML" in a["categories"])
    both = sum(1 for a in r["articles"] if len(a["categories"]) > 1)
    print(f"{jname}: {r['count']} articles (CSP/LBBAP: {csp_count}, AI/ML: {ai_count}, both: {both})")
    total += r["count"]
    for a in r["articles"]:
        cats = "+".join(a["categories"])
        print(f"  [{a['year']}] [{cats}] {a['title'][:100]}")
    print()

print(f"\nTotal: {total} articles")
print(f"Total PMIDs: {len(all_pmids)}")

with open(DATA_DIR / "filtered_pmids.json", "w") as f:
    json.dump({"pmids": all_pmids, "by_journal": {k: [a["pmid"] for a in v["articles"]] for k, v in results.items()}}, f)
