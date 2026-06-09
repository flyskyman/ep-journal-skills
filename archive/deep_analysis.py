import csv
import re
import json
from collections import Counter, defaultdict
from pathlib import Path

DATA_DIR = Path(r"C:\Projects\jouranl-title\data")

JOURNALS = {
    "hr": ("hr_abstracts.csv", "Heart Rhythm"),
    "circ_ae": ("circ_ae_abstracts.csv", "Circ AE"),
    "europace": ("europace_abstracts.csv", "Europace"),
    "jacc_ep": ("jacc_ep_abstracts.csv", "JACC EP"),
    "pace": ("pace_abstracts.csv", "PACE"),
}

# Fine-grained CSP/LBBAP subtopics
CSP_SUBTOPICS = {
    "LBBAP Technique/Implantation": [r"\bLBB[AP]?\b.*(?:implant|technique|procedure|deliver|screw|penetrat|depth)", r"\bleft bundle branch.*(?:implant|technique|procedure|deliver|lead)", r"\bimplant.*left bundle", r"\bdeep septal"],
    "LBBAP vs RV Pacing": [r"\bLBB.*(?:versus|vs|compared).*(?:RV|right ventricular)", r"\b(?:RV|right ventricular).*(?:versus|vs|compared).*LBB", r"\bconduction system pacing.*(?:versus|vs|compared).*right ventricular"],
    "LBBAP for CRT": [r"\bLBB.*(?:CRT|resynchronization)", r"\bconduction system.*resynchronization", r"\bCSP.*CRT", r"\bleft bundle.*resynchronization"],
    "LBBAP Outcomes/Safety": [r"\bLBB.*(?:outcome|safety|complication|follow.up|long.term|threshold|sensing)", r"\bleft bundle.*(?:outcome|safety|threshold|sensing|complication)"],
    "LBBAP Physiology/Mechanism": [r"\bLBB.*(?:capture|electrogram|morpholog|conduction|activation|QRS)", r"\bleft bundle.*(?:capture|electrogram|morpholog|conduction|activation|QRS)", r"\bseptal.*activation"],
    "His Bundle Pacing": [r"\bHis bundle\b", r"\bHis.Purkinje\b", r"\bhisian\b", r"\bHBP\b"],
    "CSP General/Review": [r"\bconduction system pacing\b", r"\bCSP\b.*(?:review|meta|overview|update)", r"\bphysiologic pacing\b"],
    "CSP + ICD/Defibrillation": [r"\b(?:CSP|LBB|conduction system).*(?:ICD|defibrillat)", r"\b(?:ICD|defibrillat).*(?:CSP|LBB|conduction system)"],
    "CSP in Special Populations": [r"\b(?:CSP|LBB|conduction system).*(?:pediatric|child|elderly|congenital|TAVR|valv)"],
}

AI_SUBTOPICS = {
    "AI-ECG Diagnosis/Screening": [r"\b(?:AI|artificial intelligence|deep learning|machine learning|neural network).*(?:ECG|electrocardiogram|12.lead)", r"\b(?:ECG|electrocardiogram).*(?:AI|artificial intelligence|deep learning|machine learning|neural network)"],
    "AI Arrhythmia Detection": [r"\b(?:AI|machine learning|deep learning|automat).*(?:detect|classif|identif).*(?:arrhythmia|fibrillation|tachycardia|rhythm)"],
    "AI Risk Prediction": [r"\b(?:AI|machine learning|deep learning|predict).*(?:risk|predict|prognos|outcome).*(?:model|score|algorithm)", r"\bpredictive model\b"],
    "AI Mapping/Imaging": [r"\b(?:AI|machine learning|deep learning|automat).*(?:mapping|imaging|segment|image)", r"\b(?:mapping|imaging).*(?:AI|machine learning|deep learning|automat)"],
    "Digital Health/Wearables": [r"\bwearable\b", r"\bsmartwatch\b", r"\bApple Watch\b", r"\bdigital.*health\b", r"\bremote.*monitor.*(?:AI|algorithm|automat)", r"\bphotoplethysmograph\b"],
    "AI-Guided Ablation": [r"\b(?:AI|machine learning|automat).*(?:ablation|catheter)", r"\b(?:ablation|catheter).*(?:AI|machine learning).*(?:guid|assist|predict)"],
    "Natural Language/LLM": [r"\bnatural language\b", r"\blarge language\b", r"\bLLM\b", r"\bGPT\b", r"\bChatGPT\b"],
}

STUDY_TYPES = {
    "RCT": [r"\brandom\w*\s+(?:controlled\s+)?trial\b", r"\bRCT\b", r"\brandomized\b.*\bcompare\b"],
    "Meta-analysis": [r"\bmeta.analysis\b", r"\bsystematic review\b"],
    "Prospective Cohort": [r"\bprospective\b.*(?:cohort|study|observ)", r"\bprospective\b.*\bmulticenter\b"],
    "Retrospective Cohort": [r"\bretrospective\b.*(?:cohort|study|observ|analysis)"],
    "Registry Study": [r"\bregistry\b", r"\bnationwide\b.*(?:study|cohort|analysis)", r"\bpopulation.based\b"],
    "Case Report/Series": [r"\bcase report\b", r"\bcase series\b", r"\bfirst.in.human\b"],
    "Basic/Translational": [r"\bin vitro\b", r"\bin vivo\b", r"\banimal\b", r"\bpreclinical\b", r"\bporcine\b", r"\bcanine\b", r"\bcadaver\b", r"\bdonor.*heart\b"],
    "Editorial/Letter": [r"\beditorial\b", r"\bletter\b", r"\bcommentary\b", r"\bto the editor\b"],
    "Review": [r"\breview\b(?!.*systematic)", r"\boverview\b", r"\bstate.of.the.art\b", r"\bupdate\b"],
    "Validation Study": [r"\bvalidat\b", r"\bexternal validation\b"],
}

def match_any(text, patterns):
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False

def classify_subtopics(title, abstract):
    combined = f"{title} {abstract}"
    csp_cats = []
    ai_cats = []
    for cat, pats in CSP_SUBTOPICS.items():
        if match_any(combined, pats):
            csp_cats.append(cat)
    for cat, pats in AI_SUBTOPICS.items():
        if match_any(combined, pats):
            ai_cats.append(cat)
    return csp_cats, ai_cats

def classify_study_type(title, abstract):
    combined = f"{title} {abstract}"
    types = []
    for stype, pats in STUDY_TYPES.items():
        if match_any(combined, pats):
            types.append(stype)
    return types if types else ["Unclassified"]

def extract_sample_size(abstract):
    patterns = [
        r'(?:n\s*=\s*)(\d[\d,]+)',
        r'(\d[\d,]+)\s*(?:patients|participants|subjects|individuals)',
        r'(?:total of|included|enrolled|analyzed)\s*(\d[\d,]+)',
    ]
    sizes = []
    for p in patterns:
        for m in re.finditer(p, abstract, re.IGNORECASE):
            num = int(m.group(1).replace(',', ''))
            if 5 <= num <= 10000000:
                sizes.append(num)
    return max(sizes) if sizes else None

def load_abstracts(filename):
    articles = []
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pmid = row.get("PMID", "").strip().strip('"')
            year = row.get("Year", "").strip().strip('"')
            title = row.get("Title", "").strip().strip('"')
            abstract = row.get("Abstract", "").strip().strip('"')
            author = row.get("FirstAuthor", "").strip().strip('"')
            if pmid and title:
                articles.append({
                    "pmid": pmid, "year": year, "title": title,
                    "abstract": abstract if abstract != "N/A" else "",
                    "first_author": author,
                    "has_abstract": abstract != "N/A" and len(abstract) > 50,
                })
    return articles

def analyze_abstract_structure(abstract):
    if not abstract or len(abstract) < 100:
        return {}
    features = {
        "word_count": len(abstract.split()),
        "has_background": bool(re.search(r'\b(?:background|introduction|context)\b', abstract[:200], re.IGNORECASE)),
        "has_methods": bool(re.search(r'\b(?:method|we\s+(?:aimed|sought|conducted|performed|analyzed|compared|enrolled|included|studied))\b', abstract, re.IGNORECASE)),
        "has_results": bool(re.search(r'\b(?:result|found that|demonstrated|showed that|observed|mean|median|hazard ratio|odds ratio|p\s*[<=]|confidence interval|CI\b)\b', abstract, re.IGNORECASE)),
        "has_conclusion": bool(re.search(r'\b(?:conclusion|in summary|our findings|these results|this study demonstrates|we conclude)\b', abstract, re.IGNORECASE)),
        "has_stats": bool(re.search(r'\b(?:p\s*[<=]\s*0\.\d|CI\s|hazard ratio|odds ratio|AUC|sensitivity|specificity)\b', abstract, re.IGNORECASE)),
        "structured": bool(re.search(r'(?:BACKGROUND|METHODS|RESULTS|CONCLUSIONS|OBJECTIVE|AIM|PURPOSE)[\s:.]', abstract)),
    }
    return features

all_articles = {}
all_flat = []

for jkey, (fname, jname) in JOURNALS.items():
    articles = load_abstracts(fname)
    for a in articles:
        csp_cats, ai_cats = classify_subtopics(a["title"], a["abstract"])
        a["csp_subtopics"] = csp_cats
        a["ai_subtopics"] = ai_cats
        a["study_types"] = classify_study_type(a["title"], a["abstract"])
        a["sample_size"] = extract_sample_size(a["abstract"])
        a["abstract_features"] = analyze_abstract_structure(a["abstract"])
        a["journal"] = jname
    all_articles[jkey] = articles
    all_flat.extend(articles)

# === Output ===
print(f"Total articles: {len(all_flat)}")
print(f"With abstracts: {sum(1 for a in all_flat if a['has_abstract'])}")
print()

# 1. CSP subtopic distribution
print("=== CSP/LBBAP Subtopic Distribution ===")
csp_counter = Counter()
for a in all_flat:
    for c in a["csp_subtopics"]:
        csp_counter[c] += 1
for topic, count in csp_counter.most_common():
    print(f"  {topic}: {count}")

print("\n=== AI/ML Subtopic Distribution ===")
ai_counter = Counter()
for a in all_flat:
    for c in a["ai_subtopics"]:
        ai_counter[c] += 1
for topic, count in ai_counter.most_common():
    print(f"  {topic}: {count}")

print("\n=== Study Type Distribution ===")
type_counter = Counter()
for a in all_flat:
    for t in a["study_types"]:
        type_counter[t] += 1
for stype, count in type_counter.most_common():
    print(f"  {stype}: {count}")

# 2. Per-journal breakdown
print("\n=== Per-Journal CSP Subtopics ===")
for jkey, (fname, jname) in JOURNALS.items():
    articles = all_articles[jkey]
    jcsp = Counter()
    for a in articles:
        for c in a["csp_subtopics"]:
            jcsp[c] += 1
    if jcsp:
        print(f"\n  {jname}:")
        for t, c in jcsp.most_common(8):
            print(f"    {t}: {c}")

# 3. Year trends
print("\n=== CSP Year Trends ===")
csp_year = defaultdict(Counter)
for a in all_flat:
    for c in a["csp_subtopics"]:
        csp_year[a["year"]][c] += 1
for year in sorted(csp_year.keys(), reverse=True):
    top3 = csp_year[year].most_common(5)
    top_str = ", ".join(f"{t}:{c}" for t, c in top3)
    print(f"  {year}: {top_str}")

print("\n=== AI Year Trends ===")
ai_year = defaultdict(Counter)
for a in all_flat:
    for c in a["ai_subtopics"]:
        ai_year[a["year"]][c] += 1
for year in sorted(ai_year.keys(), reverse=True):
    top3 = ai_year[year].most_common(5)
    top_str = ", ".join(f"{t}:{c}" for t, c in top3)
    print(f"  {year}: {top_str}")

# 4. Abstract structure analysis
print("\n=== Abstract Structure by Journal ===")
for jkey, (fname, jname) in JOURNALS.items():
    articles = [a for a in all_articles[jkey] if a["has_abstract"]]
    if not articles:
        continue
    n = len(articles)
    avg_words = sum(a["abstract_features"].get("word_count", 0) for a in articles) / n
    structured = sum(1 for a in articles if a["abstract_features"].get("structured")) / n * 100
    has_stats = sum(1 for a in articles if a["abstract_features"].get("has_stats")) / n * 100
    has_conclusion = sum(1 for a in articles if a["abstract_features"].get("has_conclusion")) / n * 100
    print(f"\n  {jname} (n={n}):")
    print(f"    Avg abstract words: {avg_words:.0f}")
    print(f"    Structured format: {structured:.0f}%")
    print(f"    Contains statistics: {has_stats:.0f}%")
    print(f"    Explicit conclusion: {has_conclusion:.0f}%")

# 5. Sample size distribution
print("\n=== Sample Sizes ===")
for jkey, (fname, jname) in JOURNALS.items():
    sizes = [a["sample_size"] for a in all_articles[jkey] if a["sample_size"]]
    if sizes:
        sizes.sort()
        median = sizes[len(sizes)//2]
        print(f"  {jname}: n={len(sizes)} studies, median={median}, range={min(sizes)}-{max(sizes)}")

# 6. Export detailed data for further analysis
output = []
for a in all_flat:
    output.append({
        "pmid": a["pmid"],
        "journal": a["journal"],
        "year": a["year"],
        "title": a["title"],
        "first_author": a["first_author"],
        "has_abstract": a["has_abstract"],
        "csp_subtopics": a["csp_subtopics"],
        "ai_subtopics": a["ai_subtopics"],
        "study_types": a["study_types"],
        "sample_size": a["sample_size"],
        "abstract_word_count": a["abstract_features"].get("word_count", 0),
        "structured_abstract": a["abstract_features"].get("structured", False),
    })

with open(DATA_DIR / "deep_analysis.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"\nDetailed data saved to {DATA_DIR / 'deep_analysis.json'}")
