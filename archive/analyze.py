import csv
import re
import json
from collections import Counter, defaultdict
from pathlib import Path

DATA_DIR = Path(r"C:\Projects\jouranl-title\data")

JOURNALS = {
    "heart_rhythm": "Heart Rhythm",
    "circ_ae": "Circulation: Arrhythmia and Electrophysiology",
    "europace": "Europace",
    "jacc_ep": "JACC: Clinical Electrophysiology",
    "pace": "PACE",
}

TOPIC_KEYWORDS = {
    "Atrial Fibrillation": [r"\batrial fibrillation\b", r"\bAF\b", r"\bAfib\b", r"\bpulmonary vein isolation\b", r"\bPVI\b"],
    "Catheter Ablation": [r"\bcatheter ablation\b", r"\bablation\b", r"\bradiofrequency\b", r"\bRF ablation\b"],
    "Pulsed Field Ablation": [r"\bpulsed field ablation\b", r"\bPFA\b", r"\bpulsed.field\b"],
    "Ventricular Arrhythmia": [r"\bventricular tachycardia\b", r"\bventricular fibrillation\b", r"\bVT\b(?!A)", r"\bVF\b", r"\bventricular arrhythmia\b", r"\bPVC\b", r"\bpremature ventricular\b"],
    "Cardiac Pacing/CRT": [r"\bpacemaker\b", r"\bpacing\b", r"\bCRT\b", r"\bcardiac resynchronization\b", r"\bleadless\b", r"\blead\b"],
    "ICD/Defibrillator": [r"\bICD\b", r"\bdefibrillat\b", r"\bimplantable cardioverter\b", r"\bsubcutaneous.*ICD\b", r"\bS-ICD\b"],
    "Sudden Cardiac Death": [r"\bsudden cardiac death\b", r"\bsudden death\b", r"\bSCD\b", r"\bcardiac arrest\b"],
    "Conduction System Pacing": [r"\bleft bundle branch\b", r"\bLBBP\b", r"\bLBBA\b", r"\bconduction system pacing\b", r"\bHis bundle\b", r"\bHis-Purkinje\b"],
    "Atrial Flutter/SVT": [r"\batrial flutter\b", r"\bSVT\b", r"\bsupraventricular\b", r"\bAVNRT\b", r"\bAVRT\b", r"\btachycardia\b"],
    "Channelopathy/Genetics": [r"\bBrugada\b", r"\blong QT\b", r"\bLQTS\b", r"\bchannelopathy\b", r"\bgenetic\b", r"\bvariant\b", r"\bmutation\b", r"\bSCN5A\b", r"\bKCN\b", r"\bgene\b"],
    "Cardiomyopathy": [r"\bcardiomyopathy\b", r"\bHCM\b", r"\bDCM\b", r"\barrhythmogenic\b", r"\bACM\b"],
    "Heart Failure": [r"\bheart failure\b", r"\bHF\b(?!A)", r"\bHFrEF\b", r"\bHFpEF\b"],
    "Stroke/Anticoagulation": [r"\bstroke\b", r"\banticoagulat\b", r"\bOAC\b", r"\bthromboembol\b", r"\bbleeding\b", r"\bCHA2DS2\b"],
    "LAA Closure": [r"\bleft atrial appendage\b", r"\bLAA\b", r"\bWatchman\b", r"\bappendage closure\b", r"\bappendage occlusion\b"],
    "AI/Machine Learning": [r"\bartificial intelligence\b", r"\bmachine learning\b", r"\bdeep learning\b", r"\bAI\b", r"\bneural network\b", r"\bautomated\b"],
    "Mapping/Imaging": [r"\bmapping\b", r"\belectroanatomic\b", r"\bMRI\b", r"\bCT\b", r"\bechocardiograph\b", r"\bimaging\b"],
    "Syncope": [r"\bsyncope\b", r"\bvasovagal\b"],
    "Cardiac Monitoring": [r"\bwearable\b", r"\bmonitor\b", r"\bApple Watch\b", r"\bsmartwat\b", r"\bimplantable.*monitor\b", r"\bloop recorder\b", r"\bremote monitoring\b"],
}

TITLE_PATTERNS = {
    "Colon Structure (X: Y)": r"^[^:]+:\s+.+",
    "Question Title": r"\?[\"']?\s*$",
    "Descriptive (A/An/The start)": r"^\"?(?:A|An|The)\s",
    "Outcome/Association": r"\b(?:outcome|association|impact|effect|predictor|prognos)\b",
    "Comparison (vs/versus/compared)": r"\b(?:versus|vs\.?|compared)\b",
    "Meta-analysis/Review": r"\b(?:meta-analysis|systematic review|review|meta.analysis)\b",
    "Case Report/Series": r"\b(?:case report|case series|a case of|first.in.human)\b",
    "Trial/Study Name (ACRONYM)": r"\b[A-Z]{3,}\b.*(?:trial|study|registry)",
    "Trends/Epidemiology": r"\b(?:trend|incidence|prevalence|epidemiolog|nationwide|population.based)\b",
    "Guidelines/Consensus": r"\b(?:guideline|consensus|statement|recommendation|expert)\b",
    "Novel/New": r"\b(?:novel|new|first|emerging)\b",
}

def load_journal(fname):
    articles = []
    path = DATA_DIR / f"{fname}.csv"
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pmid = row.get("PMID", "").strip()
            year = row.get("Year", "").strip()
            title = row.get("Title", "").strip().strip('"')
            if pmid and title:
                articles.append({"pmid": pmid, "year": year, "title": title})
    return articles

def classify_topic(title):
    topics = []
    for topic, patterns in TOPIC_KEYWORDS.items():
        for pat in patterns:
            if re.search(pat, title, re.IGNORECASE):
                topics.append(topic)
                break
    return topics if topics else ["Other"]

def analyze_title_structure(title):
    features = []
    for name, pat in TITLE_PATTERNS.items():
        if re.search(pat, title, re.IGNORECASE):
            features.append(name)
    return features

def main():
    all_data = {}
    results = {}

    for fname, jname in JOURNALS.items():
        articles = load_journal(fname)
        all_data[fname] = articles

        year_counts = Counter()
        topic_counts = Counter()
        year_topic = defaultdict(Counter)
        title_lengths = []
        word_counts = []
        structure_counts = Counter()
        all_words = Counter()

        for a in articles:
            year = a["year"]
            title = a["title"]
            year_counts[year] += 1

            topics = classify_topic(title)
            for t in topics:
                topic_counts[t] += 1
                year_topic[year][t] += 1

            title_lengths.append(len(title))
            words = title.split()
            word_counts.append(len(words))

            structures = analyze_title_structure(title)
            for s in structures:
                structure_counts[s] += 1

            for w in words:
                clean = re.sub(r'[^\w-]', '', w.lower())
                if len(clean) > 3:
                    all_words[clean] += 1

        results[fname] = {
            "journal": jname,
            "total": len(articles),
            "year_counts": dict(sorted(year_counts.items(), reverse=True)),
            "top_topics": topic_counts.most_common(15),
            "year_topic": {y: dict(sorted(c.items(), key=lambda x: -x[1])[:5]) for y, c in sorted(year_topic.items(), reverse=True)},
            "avg_title_length": round(sum(title_lengths) / len(title_lengths), 1) if title_lengths else 0,
            "avg_word_count": round(sum(word_counts) / len(word_counts), 1) if word_counts else 0,
            "title_structures": structure_counts.most_common(15),
            "top_words": all_words.most_common(30),
            "colon_pct": round(structure_counts.get("Colon Structure (X: Y)", 0) / len(articles) * 100, 1),
            "question_pct": round(structure_counts.get("Question Title", 0) / len(articles) * 100, 1),
        }

    output = json.dumps(results, ensure_ascii=False, indent=2)
    out_path = DATA_DIR / "analysis.json"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Analysis saved to {out_path}")

    # Also generate a PFA trend analysis
    print("\n=== PFA Trend (Pulsed Field Ablation) ===")
    for fname, jname in JOURNALS.items():
        pfa_by_year = Counter()
        for a in all_data[fname]:
            if any(re.search(p, a["title"], re.IGNORECASE) for p in TOPIC_KEYWORDS["Pulsed Field Ablation"]):
                pfa_by_year[a["year"]] += 1
        total = sum(pfa_by_year.values())
        years_str = ", ".join(f"{y}:{c}" for y, c in sorted(pfa_by_year.items()))
        print(f"  {jname}: {total} total ({years_str})")

    # Print summary
    print("\n=== Summary per Journal ===")
    for fname in JOURNALS:
        r = results[fname]
        print(f"\n--- {r['journal']} ({r['total']} articles) ---")
        print(f"  Year distribution: {r['year_counts']}")
        print(f"  Avg title length: {r['avg_title_length']} chars, {r['avg_word_count']} words")
        print(f"  Colon structure: {r['colon_pct']}%, Question: {r['question_pct']}%")
        print(f"  Top topics: {', '.join(f'{t[0]}({t[1]})' for t in r['top_topics'][:8])}")
        print(f"  Top structures: {', '.join(f'{s[0]}({s[1]})' for s in r['title_structures'][:6])}")

if __name__ == "__main__":
    main()
