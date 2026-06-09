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
    "jice": ("jice_abstracts.csv", "JICE"),
}

AI_BROAD = [
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

PFA_PATTERNS = [r"\bpulsed field ablation\b", r"\bPFA\b", r"\bpulsed.field\b"]

# Fine AI-ECG categories
AI_FINE = {
    # === Input modality ===
    "Input-12导联标准ECG": [r"\b12.lead\b", r"\bstandard.*ECG\b", r"\b12\b.*\bECG\b", r"\bsurface ECG\b"],
    "Input-单导联/可穿戴ECG": [r"\bsingle.lead\b", r"\bambulatory\b.*ECG", r"\bHolter\b", r"\bwearable\b.*ECG", r"\bpatch\b.*ECG", r"\b1.lead\b"],
    "Input-心内电图(EGM/ICE)": [r"\bintracardiac\b.*(?:electrogram|EGM|echo)", r"\bbipolar\b.*electrogram\b", r"\bICE\b.*(?:image|echo)"],
    "Input-PPG/光电": [r"\bphotoplethysmograph\b", r"\bPPG\b", r"\bsmartwat\b", r"\bApple Watch\b"],
    "Input-CMR/CT影像": [r"\bCMR\b.*(?:AI|learning|model|automat)", r"\bLGE\b.*(?:AI|learning|model)", r"\b(?:AI|learning|model).*(?:CMR|MRI|CT)\b"],
    "Input-多模态": [r"\bmultimodal\b", r"\bmulti.modal\b", r"\bcombined.*(?:ECG|clinical|imaging)\b.*model\b"],

    # === Target disease/condition ===
    "Target-AF检测/预测": [r"\batrial fibrillation\b.*(?:detect|predict|screen|diagnos|classif)", r"\bAF\b.*(?:detect|predict|screen|risk)\b", r"\b(?:detect|predict|screen).*\batrial fibrillation\b"],
    "Target-AF复发预测": [r"\brecurrence\b.*(?:AF|atrial fibrillation|ablation)", r"\breturn\b.*(?:AF|atrial fibrillation)", r"\b(?:AF|atrial fibrillation).*recur\b"],
    "Target-VT/VF/SCA检测": [r"\bventricular tachycardia\b.*(?:detect|predict|classif)", r"\bVT\b.*(?:detect|predict|classif)", r"\bcardiac arrest\b.*(?:detect|predict)", r"\bsudden cardiac\b.*(?:death|arrest).*(?:predict|risk)"],
    "Target-心肌病筛查": [r"\bcardiomyopathy\b.*(?:detect|screen|diagnos)", r"\bATTR\b.*(?:detect|screen)", r"\bamyloid\b.*(?:detect|screen)", r"\bHCM\b.*(?:detect|screen)"],
    "Target-传导异常/缓慢心律失常": [r"\bbradyarrhythmia\b", r"\bconduction\b.*(?:disease|delay|abnormal).*(?:detect|predict)", r"\bAV block\b.*(?:predict|detect)", r"\bLBBB\b.*(?:detect|predict|identif)"],
    "Target-PVC/室早定位": [r"\bPVC\b.*(?:locali|origin|site)", r"\bpremature ventricular\b.*(?:locali|origin)", r"\bectop\b.*(?:locali|origin)"],
    "Target-心衰/心功能预测": [r"\bheart failure\b.*(?:predict|detect|screen|prognos)", r"\bLVEF\b.*(?:predict|estimat)", r"\bcardiac function\b.*(?:predict|estimat)"],
    "Target-CRT反应预测": [r"\bCRT\b.*(?:response|respond|predict)", r"\bresynchronization\b.*(?:response|predict)", r"\b(?:response|respond).*\bCRT\b"],
    "Target-消融靶点/引导": [r"\bablation\b.*(?:target|guide|assist|predict).*(?:AI|model|automat)", r"\bmapping\b.*(?:AI|automat|algorithm)", r"\b(?:AI|automat).*(?:ablation|mapping)\b"],
    "Target-Brugada综合征": [r"\bBrugada\b.*(?:AI|model|diagnos|detect|classif)"],
    "Target-生物年龄/整体风险": [r"\bbiolog.*age\b", r"\bAI.*age\b", r"\bvascular age\b", r"\bECG.*age\b"],
    "Target-房颤消融后食管损伤": [r"\besophag\b.*(?:predict|injury|thermal)"],

    # === ML method ===
    "Method-CNN/卷积网络": [r"\bCNN\b", r"\bconvolutional\b", r"\bResNet\b", r"\bInception\b", r"\bDenseNet\b"],
    "Method-RNN/LSTM/时序": [r"\bRNN\b", r"\bLSTM\b", r"\brecurrent\b", r"\btemporal\b.*network\b", r"\btime.series\b.*(?:model|network)"],
    "Method-Transformer/Attention": [r"\btransformer\b", r"\battention\b.*(?:mechanism|model|network)", r"\bself.attention\b"],
    "Method-传统ML(RF/SVM/XGB)": [r"\brandom forest\b", r"\bsupport vector\b", r"\bSVM\b", r"\bXGBoost\b", r"\bgradient boost\b", r"\blogistic regression\b.*(?:model|predict)"],
    "Method-集成/多模型比较": [r"\bensemble\b", r"\bcompare.*model\b", r"\bmodel comparison\b", r"\bmultiple.*algorithm\b"],
    "Method-可解释性/SHAP": [r"\bexplainab\b", r"\binterpretab\b", r"\bSHAP\b", r"\bGrad.?CAM\b", r"\battention.*map\b", r"\bsaliency\b"],
    "Method-联邦学习/隐私": [r"\bfederat\b", r"\bprivacy\b.*(?:preserv|protect)", r"\bdifferential privacy\b"],
    "Method-NLP/LLM": [r"\bnatural language\b", r"\bLLM\b", r"\bGPT\b", r"\bChatGPT\b", r"\blarge language\b"],

    # === Validation ===
    "Validation-外部验证": [r"\bexternal.*valid\b", r"\bmulti.?center.*valid\b", r"\bexternally\b.*valid\b", r"\bindependent.*(?:cohort|dataset|valid)\b"],
    "Validation-多中心/多国": [r"\bmulti.?center\b", r"\bmulti.?national\b", r"\bmulti.?site\b", r"\bmulti.?institution\b"],
    "Validation-大规模数据(>10000)": [r"\b\d{5,}\b.*(?:patient|ECG|record|subject)"],
    "Validation-前瞻性验证": [r"\bprospective.*valid\b", r"\breal.world.*valid\b", r"\breal.time\b.*(?:valid|test|deploy)"],

    # === Clinical translation ===
    "Translation-FDA/CE认证相关": [r"\bFDA\b", r"\bCE.?mark\b", r"\bregulatory\b", r"\bcertif\b"],
    "Translation-临床决策支持": [r"\bclinical decision\b", r"\bdecision support\b", r"\bclinical.*workflow\b", r"\btriage\b"],
    "Translation-筛查项目/人群健康": [r"\bscreening\b.*(?:program|population|communit)", r"\bpopulation.*screen\b", r"\bmass screen\b"],
    "Translation-远程监测/CIED": [r"\bremote monitor\b.*(?:AI|automat|algorithm)", r"\bCIED\b.*(?:AI|automat)", r"\bdevice.*transmis\b.*(?:AI|automat)"],
}

# Performance metrics extraction
PERF_PATTERNS = {
    "AUC/AUROC": r'\bAU(?:RO)?C\b.*?(?:of\s+)?(\d+\.?\d*)',
    "Sensitivity": r'\bsensitivit\w*\b.*?(\d+\.?\d*)\s*%',
    "Specificity": r'\bspecificit\w*\b.*?(\d+\.?\d*)\s*%',
    "Accuracy": r'\baccuracy\b.*?(\d+\.?\d*)\s*%',
    "NPV": r'\bnegative predictive\b.*?(\d+\.?\d*)\s*%',
    "PPV": r'\bpositive predictive\b.*?(\d+\.?\d*)\s*%',
}

def match_any(text, patterns):
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False

def extract_perf(abstract):
    metrics = {}
    for name, pat in PERF_PATTERNS.items():
        matches = re.findall(pat, abstract, re.IGNORECASE)
        if matches:
            vals = [float(v) for v in matches if 0 < float(v) <= 100]
            if vals:
                metrics[name] = max(vals)
    return metrics

def extract_n(abstract):
    patterns = [r'(?:n\s*=\s*)(\d[\d,]+)', r'(\d[\d,]+)\s*(?:patients|ECGs?|records|subjects|participants)']
    sizes = []
    for p in patterns:
        for m in re.finditer(p, abstract, re.IGNORECASE):
            num = int(m.group(1).replace(',', ''))
            if 10 <= num <= 50000000:
                sizes.append(num)
    return max(sizes) if sizes else None

def extract_cohort_names(abstract):
    known = ["Framingham", "UK Biobank", "ELSA-Brasil", "MIMIC", "PhysioNet", "Medicare",
             "TriNetX", "Mayo Clinic", "Cleveland Clinic", "Cedars-Sinai", "Mass General"]
    found = []
    for name in known:
        if re.search(name, abstract, re.IGNORECASE):
            found.append(name)
    return found

all_ai = []
for jkey, (fname, jname) in JOURNALS.items():
    path = DATA_DIR / fname
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pmid = row.get("PMID", row.get("pmid", "")).strip().strip('"')
            year = row.get("Year", row.get("year", "")).strip().strip('"')
            title = row.get("Title", row.get("title", "")).strip().strip('"')
            abstract = row.get("Abstract", row.get("abstract", "")).strip().strip('"')
            author = row.get("FirstAuthor", row.get("first_author", "")).strip().strip('"')
            if abstract == "N/A":
                abstract = ""
            combined = f"{title} {abstract}"
            if not match_any(combined, AI_BROAD):
                continue
            if match_any(combined, PFA_PATTERNS):
                continue

            fine_cats = []
            for cat, pats in AI_FINE.items():
                if match_any(combined, pats):
                    fine_cats.append(cat)

            perf = extract_perf(abstract) if abstract else {}
            n = extract_n(abstract) if abstract else None
            cohorts = extract_cohort_names(abstract) if abstract else []

            all_ai.append({
                "pmid": pmid, "year": year, "title": title,
                "abstract": abstract, "author": author, "journal": jname,
                "fine_cats": fine_cats, "perf_metrics": perf,
                "sample_size": n, "cohort_names": cohorts,
                "has_abstract": len(abstract) > 50,
            })

print(f"Total AI/ML articles (excl PFA): {len(all_ai)}")
print(f"With abstracts: {sum(1 for a in all_ai if a['has_abstract'])}")

# Fine categories
print("\n=== Fine Categories ===")
fine_counter = Counter()
for a in all_ai:
    for c in a["fine_cats"]:
        fine_counter[c] += 1
for cat, cnt in fine_counter.most_common():
    print(f"  {cat}: {cnt}")

# Per journal
print("\n=== Per-Journal ===")
for jkey, (fname, jname) in JOURNALS.items():
    jarticles = [a for a in all_ai if a["journal"] == jname]
    if not jarticles:
        continue
    jfine = Counter()
    for a in jarticles:
        for c in a["fine_cats"]:
            jfine[c] += 1
    print(f"\n  {jname} ({len(jarticles)} articles):")
    for cat, cnt in jfine.most_common(12):
        print(f"    {cat}: {cnt}")

# Year trends
print("\n=== Year Trends (Key) ===")
for cat in ["Target-AF检测/预测", "Target-心肌病筛查", "Target-CRT反应预测",
            "Target-VT/VF/SCA检测", "Target-消融靶点/引导", "Target-传导异常/缓慢心律失常",
            "Method-CNN/卷积网络", "Method-传统ML(RF/SVM/XGB)", "Method-Transformer/Attention",
            "Validation-外部验证", "Validation-多中心/多国", "Input-多模态"]:
    year_cnt = Counter()
    for a in all_ai:
        if cat in a["fine_cats"]:
            year_cnt[a["year"]] += 1
    total = sum(year_cnt.values())
    if total > 0:
        years_str = ", ".join(f"{y}:{c}" for y, c in sorted(year_cnt.items()))
        print(f"  {cat}: {total} ({years_str})")

# Performance metrics
print("\n=== Performance Metrics (AUC > 0.7) ===")
for a in all_ai:
    if "AUC/AUROC" in a["perf_metrics"] and a["perf_metrics"]["AUC/AUROC"] >= 0.7:
        auc = a["perf_metrics"]["AUC/AUROC"]
        sens = a["perf_metrics"].get("Sensitivity", "—")
        spec = a["perf_metrics"].get("Specificity", "—")
        targets = [c for c in a["fine_cats"] if c.startswith("Target-")]
        methods = [c for c in a["fine_cats"] if c.startswith("Method-")]
        target_str = ", ".join(targets) if targets else "—"
        method_str = ", ".join(methods) if methods else "—"
        print(f"  [{a['journal']}] [{a['year']}] AUC={auc} Sens={sens} Spec={spec}")
        print(f"    Target: {target_str} | Method: {method_str}")
        print(f"    N={a['sample_size']} | {a['title'][:90]}")

# Sample size distribution
print("\n=== Sample Sizes ===")
sizes_with = [(a["sample_size"], a["journal"]) for a in all_ai if a["sample_size"]]
if sizes_with:
    sizes_only = [s[0] for s in sizes_with]
    sizes_only.sort()
    print(f"  Total with N: {len(sizes_only)}")
    print(f"  Median: {sizes_only[len(sizes_only)//2]}, Range: {min(sizes_only)}-{max(sizes_only)}")
    print(f"  >10000: {sum(1 for s in sizes_only if s > 10000)}")
    print(f"  >100000: {sum(1 for s in sizes_only if s > 100000)}")

# Cohort usage
print("\n=== Named Cohorts ===")
cohort_counter = Counter()
for a in all_ai:
    for c in a["cohort_names"]:
        cohort_counter[c] += 1
for c, cnt in cohort_counter.most_common():
    print(f"  {c}: {cnt}")

# Export
output = []
for a in all_ai:
    output.append({
        "pmid": a["pmid"], "journal": a["journal"], "year": a["year"],
        "title": a["title"], "author": a["author"],
        "fine_cats": a["fine_cats"], "perf_metrics": a["perf_metrics"],
        "sample_size": a["sample_size"], "cohort_names": a["cohort_names"],
        "has_abstract": a["has_abstract"],
    })
with open(DATA_DIR / "ai_ecg_deep.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"\nExported to {DATA_DIR / 'ai_ecg_deep.json'}")
