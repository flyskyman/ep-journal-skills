import csv
import re
from collections import Counter
from pathlib import Path

DATA_DIR = Path(r"C:\Projects\jouranl-title\data")

TOPIC_KEYWORDS = {
    "Atrial Fibrillation": [r"\batrial fibrillation\b", r"\bAF\b", r"\bAfib\b", r"\bpulmonary vein isolation\b", r"\bPVI\b"],
    "Catheter Ablation": [r"\bcatheter ablation\b", r"\bablation\b", r"\bradiofrequency\b", r"\bRF ablation\b"],
    "Pulsed Field Ablation": [r"\bpulsed field ablation\b", r"\bPFA\b", r"\bpulsed.field\b"],
    "Ventricular Arrhythmia": [r"\bventricular tachycardia\b", r"\bventricular fibrillation\b", r"\bVT\b(?!A)", r"\bVF\b", r"\bventricular arrhythmia\b", r"\bPVC\b", r"\bpremature ventricular\b"],
    "Cardiac Pacing/CRT": [r"\bpacemaker\b", r"\bpacing\b", r"\bCRT\b", r"\bcardiac resynchronization\b", r"\bleadless\b", r"\blead\b"],
    "ICD/Defibrillator": [r"\bICD\b", r"\bdefibrillat\b", r"\bimplantable cardioverter\b", r"\bsubcutaneous.*ICD\b", r"\bS-ICD\b"],
    "Conduction System Pacing": [r"\bleft bundle branch\b", r"\bLBBP\b", r"\bLBBA\b", r"\bconduction system pacing\b", r"\bHis bundle\b", r"\bHis-Purkinje\b"],
    "Mapping/Imaging": [r"\bmapping\b", r"\belectroanatomic\b", r"\bMRI\b", r"\bCT\b", r"\bechocardiograph\b", r"\bimaging\b"],
    "AI/Machine Learning": [r"\bartificial intelligence\b", r"\bmachine learning\b", r"\bdeep learning\b", r"\bAI\b", r"\bneural network\b"],
}

TITLE_PATTERNS = {
    "Colon Structure": r"^[^:]+:\s+.+",
    "Question Title": r"\?[\"']?\s*$",
    "Comparison (vs/versus)": r"\b(?:versus|vs\.?|compared)\b",
    "Meta-analysis/Review": r"\b(?:meta-analysis|systematic review|review|meta.analysis)\b",
    "Case Report/Series": r"\b(?:case report|case series|a case of|first.in.human)\b",
    "Novel/New": r"\b(?:novel|new|first|emerging)\b",
    "Outcome/Association": r"\b(?:outcome|association|impact|effect|predictor|prognos)\b",
}

articles = []
path = DATA_DIR / "jice.csv"
with open(path, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        title = row.get("Title", "").strip().strip('"')
        year = row.get("Year", "").strip().strip('"')
        if title:
            articles.append({"title": title, "year": year})

year_counts = Counter(a["year"] for a in articles)
topic_counts = Counter()
structure_counts = Counter()
title_lengths = [len(a["title"]) for a in articles]
word_counts = [len(a["title"].split()) for a in articles]

for a in articles:
    for topic, pats in TOPIC_KEYWORDS.items():
        for p in pats:
            if re.search(p, a["title"], re.IGNORECASE):
                topic_counts[topic] += 1
                break
    for name, pat in TITLE_PATTERNS.items():
        if re.search(pat, a["title"], re.IGNORECASE):
            structure_counts[name] += 1

n = len(articles)
print(f"=== JICE Analysis ({n} articles) ===")
print(f"\nYear distribution: {dict(sorted(year_counts.items(), reverse=True))}")
print(f"Avg title length: {sum(title_lengths)/n:.1f} chars, {sum(word_counts)/n:.1f} words")
print(f"Colon structure: {structure_counts.get('Colon Structure',0)/n*100:.1f}%")
print(f"Question title: {structure_counts.get('Question Title',0)/n*100:.1f}%")

print(f"\nTop topics:")
for t, c in topic_counts.most_common(10):
    print(f"  {t}: {c} ({c/n*100:.1f}%)")

print(f"\nTitle structures:")
for s, c in structure_counts.most_common():
    print(f"  {s}: {c} ({c/n*100:.1f}%)")
