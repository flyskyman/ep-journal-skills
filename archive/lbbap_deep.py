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

CSP_PATTERNS = [
    r"\bleft bundle branch\b", r"\bLBBP\b", r"\bLBBA\b", r"\bLBB pacing\b",
    r"\bconduction system pacing\b", r"\bCSP\b",
    r"\bHis bundle\b", r"\bHis-Purkinje\b", r"\bHis pacing\b",
    r"\bhisian pacing\b", r"\bphysiologic pacing\b",
    r"\bcardiac resynchronization.*pacing\b", r"\bCRT.*pacing\b",
    r"\bbundle branch\b.*pacing", r"\bpacing.*bundle branch\b",
    r"\bseptal pacing\b", r"\bdeep septal\b",
]

PFA_PATTERNS = [r"\bpulsed field ablation\b", r"\bPFA\b", r"\bpulsed.field\b", r"\belectroporation\b"]
AI_PATTERNS = [r"\bartificial intelligence\b", r"\bmachine learning\b", r"\bdeep learning\b", r"\bneural network\b", r"\bAI\b(?!DS|CD|V\b)"]

# Very fine-grained LBBAP subtopics
LBBAP_FINE = {
    # === Technique ===
    "植入技术-鞘管/导线选择": [r"\bsheath\b", r"\bdelivery.*system\b", r"\bguiding catheter\b", r"\bcurve\b.*\b(?:select|choice)\b"],
    "植入技术-SDL vs LLL": [r"\bstylet.driven\b", r"\blumenless\b", r"\bSDL\b", r"\bLLL\b", r"\b3830\b"],
    "植入技术-RF辅助/困难植入": [r"\bradiofrequency.*(?:facilitat|current|assist)\b", r"\bfibrosis.*septum\b", r"\bdifficult.*implant\b", r"\bbailout\b"],
    "植入技术-Zero/低透视": [r"\bzero.fluoroscop\b", r"\blow.fluoroscop\b", r"\bminimal fluoroscop\b", r"\belectroanatomic mapping.*pacing\b"],
    "植入技术-简化方法": [r"\bsimplif\b", r"\bmodified.*lead\b", r"\bwithout.*sheath\b", r"\bpoor man\b", r"\bmodified chest lead\b"],
    "植入技术-植入成功率/失败分析": [r"\bsuccess rate\b", r"\bprocedural.*(?:success|failure|outcome)\b", r"\blearning curve\b", r"\bimplant.*success\b"],

    # === Capture/Physiology ===
    "夺获标准-LBB夺获确认": [r"\bcapture.*(?:criter|confirm|identif|verif)\b", r"\bcapture type\b", r"\bselective.*capture\b", r"\bnon.selective\b", r"\btransition\b.*output"],
    "夺获标准-QRS形态分析": [r"\bQRS.*(?:morpholog|duration|pattern|axis)\b", r"\bpaced QRS\b", r"\bR.wave peak time\b", r"\bRWPT\b", r"\bV[16].*morpholog\b"],
    "夺获标准-LVAT/电激动": [r"\bLVAT\b", r"\bleft ventricular activation time\b", r"\bactivation.*(?:pattern|sequence|map)\b", r"\bventricular.*synchron\b.*(?:electr|paced)"],
    "夺获标准-LBBP vs LVSP区分": [r"\bLBBP\b.*\bLVSP\b", r"\bLVSP\b.*\bLBBP\b", r"\bleft bundle branch pacing\b.*\bleft ventricular septal\b", r"\bseptal pacing\b.*\bbundle\b"],
    "电生理参数-阈值/感知/阻抗": [r"\bthreshold\b", r"\bsensing\b", r"\bimpedance\b", r"\blead.*(?:performance|parameter|stability)\b", r"\bcurrent of injury\b"],
    "电生理参数-心内电图": [r"\belectrogram\b", r"\bEGM\b", r"\bintracardiac\b.*\brecord\b", r"\bLBB potential\b", r"\bunipolar\b"],

    # === CRT/Heart Failure ===
    "CRT-LBBAP vs BiVP": [r"\bLBB.*\b(?:versus|vs|compared)\b.*\b(?:biventricular|BiV|BVP)\b", r"\b(?:biventricular|BiV)\b.*\b(?:versus|vs|compared)\b.*\bLBB\b"],
    "CRT-LVEF改善/逆重构": [r"\bLVEF\b.*\b(?:improv|increas|change)\b", r"\breverse remodel\b", r"\bsuper.?respond\b", r"\bCRT.*response\b", r"\brespond\b.*\bCRT\b"],
    "CRT-非反应者预测": [r"\bnon.?respond\b", r"\bpredict.*(?:response|responder)\b", r"\brisk.*stratif\b.*\bCRT\b"],
    "CRT-心衰住院/死亡": [r"\bheart failure.*(?:hospitali|death|mortalit)\b", r"\ball.cause mortality\b", r"\bcomposite.*endpoint\b", r"\bsurvival\b"],
    "CRT-LBBAP作为升级/挽救": [r"\bupgrade\b", r"\brescue\b", r"\breplacement\b.*\bCRT\b", r"\bpacing.induced cardiomyopathy\b", r"\bPICM\b"],

    # === LBBAP vs RVP ===
    "vs RVP-血流动力学/LVEF": [r"\b(?:RV|right ventricular).*(?:pacing|pace)\b.*(?:LVEF|ejection|function|remodel)\b", r"\bLBB.*(?:versus|vs).*(?:RV|right ventricular)\b.*(?:LVEF|function)"],
    "vs RVP-房颤发生": [r"\bnew.onset.*(?:AF|atrial fibrillation)\b.*(?:RV|CSP|LBB)\b", r"\batrial.*arrhythmia.*(?:burden|incidence)\b.*(?:RV|CSP)"],
    "vs RVP-三尖瓣反流": [r"\btricuspid.*regurgitation\b", r"\bTR\b.*(?:worsen|grade|change)\b"],

    # === Safety/Complications ===
    "安全-间隔穿孔/导线脱位": [r"\bperforation\b", r"\bdislodge\b", r"\bdisplacement\b", r"\bprotrusion\b", r"\bventricular septal defect\b"],
    "安全-导线提取": [r"\bextraction\b", r"\blead.*remov\b"],
    "安全-长期参数稳定性": [r"\blong.term\b.*(?:threshold|parameter|performance|stability|follow)\b", r"\b(?:threshold|parameter).*(?:stable|stability|long.term)\b"],
    "安全-T波过感知/误感知": [r"\bT.wave.*oversens\b", r"\boversens\b", r"\binappropriate.*detect\b"],
    "安全-MRI兼容性": [r"\bMRI\b.*\bsafe\b", r"\bmagnetic resonance\b.*\bsafe\b", r"\bcardiac magnetic resonance\b.*\bpacing\b"],

    # === Special Populations ===
    "特殊人群-高龄(≥75/80/90)": [r"\b(?:elderly|octogenarian|nonagenarian|aged|older)\b", r"\b(?:≥|>)\s*(?:75|80|90)\b.*\byear\b"],
    "特殊人群-儿科": [r"\bpediatric\b", r"\bchild\b", r"\binfant\b", r"\byoung\b.*\bpatient\b"],
    "特殊人群-先心病/术后": [r"\bcongenital\b", r"\bEbstein\b", r"\bTGA\b", r"\bGlenn\b", r"\bsurgical.*VSD\b", r"\bprosthetic.*valve\b"],
    "特殊人群-TAVR后": [r"\bTAVR\b", r"\bTAVI\b", r"\btranscatheter aortic\b"],
    "特殊人群-心肌病(DCM/HCM/ICM)": [r"\bcardiomyopathy\b", r"\bDCM\b", r"\bHCM\b", r"\bischemic\b.*\bcardiomyopathy\b", r"\bsarcoidosis\b", r"\bamyloidosis\b"],
    "特殊人群-房颤(AV结消融)": [r"\bAV.*node.*ablation\b", r"\batrioventricular.*node.*ablation\b", r"\bpace.and.ablate\b"],

    # === His Bundle Pacing ===
    "His束-HBP技术/参数": [r"\bHis bundle.*(?:pacing|lead|threshold|parameter)\b", r"\bHBP\b.*(?:lead|threshold|implant)"],
    "His束-HBP vs LBBAP": [r"\bHis.*(?:versus|vs|compared).*(?:LBB|left bundle)\b", r"\b(?:LBB|left bundle).*(?:versus|vs|compared).*His\b"],
    "His束-HBP for CRT": [r"\bHis.*(?:CRT|resynchroniz)\b", r"\bHis.Alternative\b"],

    # === Imaging/Assessment ===
    "影像-CMR/瘢痕评估": [r"\bCMR\b", r"\bcardiac magnetic resonance\b", r"\blate gadolinium\b", r"\bLGE\b", r"\bscar\b.*\b(?:assess|burden|predict)\b"],
    "影像-CT定位": [r"\b(?:CT|computed tomography)\b.*(?:lead|position|location)\b", r"\bphoton.counting\b"],
    "影像-超声评估(STE/TTE)": [r"\bspeckle tracking\b", r"\bstrain\b", r"\bmyocardial work\b", r"\bechocardiograph\b.*(?:assess|evaluat|synchron)\b"],
    "影像-ECGi/UHF-ECG": [r"\bECGi\b", r"\bultra.high.frequency\b", r"\bUHF.ECG\b", r"\bbody surface\b.*\bmapping\b"],

    # === ICD/Defibrillation ===
    "ICD-CSP+ICD联合": [r"\bICD\b.*\b(?:CSP|LBB|conduction system)\b", r"\b(?:CSP|LBB).*\bICD\b", r"\bdefibrillat.*lead\b.*\b(?:LBB|bundle)\b"],
    "ICD-ATP via LBBA": [r"\bantitachycardia.*pacing\b.*\b(?:LBB|bundle)\b", r"\bATP\b.*\b(?:LBB|LBBA)\b"],

    # === Emerging ===
    "新兴-抗心律失常效应": [r"\barrhythm\b.*\b(?:suppress|prevent|reduce|vulnerab)\b.*\b(?:LBB|CSP|conduction system)\b", r"\bventricular arrhythmia\b.*\b(?:LBB|CSP)\b"],
    "新兴-EMW/QT/复极化": [r"\belectromechanical window\b", r"\bEMW\b", r"\bQT\b.*\b(?:correct|interval|dispers)\b.*\bpacing\b", r"\brepolariz\b"],
    "新兴-经肝静脉/非常规路径": [r"\btranshepatic\b", r"\bunconventional.*access\b", r"\bpersistent left SVC\b"],
}

STUDY_DESIGNS = {
    "RCT": [r"\brandomized\b", r"\bRCT\b"],
    "前瞻性队列": [r"\bprospective\b"],
    "回顾性队列": [r"\bretrospective\b"],
    "注册研究/真实世界": [r"\bregistry\b", r"\breal.world\b", r"\bnationwide\b", r"\bMedicare\b", r"\bpopulation.based\b"],
    "Meta-analysis": [r"\bmeta.analysis\b", r"\bsystematic review\b"],
    "计算模型/基础": [r"\bin.silico\b", r"\bcomputational\b", r"\bpreclinical\b", r"\banimal\b", r"\bcadaver\b", r"\bdonor.*heart\b", r"\bporcine\b", r"\bcanine\b"],
    "Case report/series": [r"\bcase report\b", r"\bcase series\b", r"\bcase present\b"],
    "Editorial/Letter": [r"\beditorial\b", r"\bletter\b", r"\bcomment\b", r"\bto the editor\b"],
    "综述": [r"\breview\b(?!.*systematic)", r"\bstate.of.the.art\b", r"\boverview\b"],
}

def match_any(text, patterns):
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False

def is_csp(title, abstract=""):
    combined = f"{title} {abstract}"
    return match_any(combined, CSP_PATTERNS) and not match_any(combined, PFA_PATTERNS)

def classify_fine(title, abstract):
    combined = f"{title} {abstract}"
    cats = []
    for cat, pats in LBBAP_FINE.items():
        if match_any(combined, pats):
            cats.append(cat)
    return cats

def classify_design(title, abstract):
    combined = f"{title} {abstract}"
    designs = []
    for d, pats in STUDY_DESIGNS.items():
        if match_any(combined, pats):
            designs.append(d)
    return designs if designs else ["未分类"]

def extract_n(abstract):
    patterns = [r'(?:n\s*=\s*)(\d[\d,]+)', r'(\d[\d,]+)\s*(?:patients|participants|subjects)']
    sizes = []
    for p in patterns:
        for m in re.finditer(p, abstract, re.IGNORECASE):
            num = int(m.group(1).replace(',', ''))
            if 5 <= num <= 10000000:
                sizes.append(num)
    return max(sizes) if sizes else None

def extract_lvef_change(abstract):
    m = re.search(r'LVEF.*?(?:improv|increas|chang).*?(\d+\.?\d*)%?\s*(?:to|→)\s*(\d+\.?\d*)%', abstract, re.IGNORECASE)
    if m:
        return f"{m.group(1)}% → {m.group(2)}%"
    m = re.search(r'LVEF.*?(?:improv|increas).*?(\d+\.?\d*)\s*%', abstract, re.IGNORECASE)
    if m:
        return f"+{m.group(1)}%"
    return None

# Load and filter
all_csp = []
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
            if pmid and title and is_csp(title, abstract):
                if match_any(title, AI_PATTERNS) or match_any(abstract, AI_PATTERNS):
                    continue  # exclude pure AI
                fine_cats = classify_fine(title, abstract)
                designs = classify_design(title, abstract)
                n = extract_n(abstract) if abstract else None
                lvef = extract_lvef_change(abstract) if abstract else None
                all_csp.append({
                    "pmid": pmid, "year": year, "title": title,
                    "abstract": abstract, "author": author, "journal": jname,
                    "fine_cats": fine_cats, "designs": designs,
                    "sample_size": n, "lvef_change": lvef,
                    "has_abstract": len(abstract) > 50,
                })

print(f"Total LBBAP/CSP articles (excl AI): {len(all_csp)}")
print(f"With abstracts: {sum(1 for a in all_csp if a['has_abstract'])}")

# Fine category counts
print("\n=== Fine-grained Categories ===")
fine_counter = Counter()
for a in all_csp:
    for c in a["fine_cats"]:
        fine_counter[c] += 1
for cat, cnt in fine_counter.most_common():
    print(f"  {cat}: {cnt}")

# By journal
print("\n=== Per-Journal Top Fine Categories ===")
for jkey, (fname, jname) in JOURNALS.items():
    jarticles = [a for a in all_csp if a["journal"] == jname]
    if not jarticles:
        continue
    jfine = Counter()
    for a in jarticles:
        for c in a["fine_cats"]:
            jfine[c] += 1
    print(f"\n  {jname} ({len(jarticles)} articles):")
    for cat, cnt in jfine.most_common(10):
        print(f"    {cat}: {cnt}")

# Year trends for key categories
KEY_CATS = ["植入技术-SDL vs LLL", "CRT-LBBAP vs BiVP", "夺获标准-LBBP vs LVSP区分",
            "特殊人群-TAVR后", "安全-间隔穿孔/导线脱位", "His束-HBP vs LBBAP",
            "新兴-抗心律失常效应", "CRT-LVEF改善/逆重构", "影像-CMR/瘢痕评估"]
print("\n=== Key Category Year Trends ===")
for cat in KEY_CATS:
    year_cnt = Counter()
    for a in all_csp:
        if cat in a["fine_cats"]:
            year_cnt[a["year"]] += 1
    if sum(year_cnt.values()) > 0:
        years_str = ", ".join(f"{y}:{c}" for y, c in sorted(year_cnt.items()))
        print(f"  {cat}: total={sum(year_cnt.values())} ({years_str})")

# Study design distribution
print("\n=== Study Design Distribution ===")
design_counter = Counter()
for a in all_csp:
    for d in a["designs"]:
        design_counter[d] += 1
for d, cnt in design_counter.most_common():
    print(f"  {d}: {cnt}")

# Sample sizes
print("\n=== Sample Sizes by Design ===")
for design in ["RCT", "前瞻性队列", "回顾性队列", "注册研究/真实世界", "Meta-analysis"]:
    sizes = [a["sample_size"] for a in all_csp if design in a["designs"] and a["sample_size"]]
    if sizes:
        sizes.sort()
        med = sizes[len(sizes)//2]
        print(f"  {design}: n={len(sizes)}, median={med}, range={min(sizes)}-{max(sizes)}")

# LVEF changes reported
print("\n=== LVEF Changes Reported ===")
for a in all_csp:
    if a["lvef_change"]:
        print(f"  [{a['journal']}] [{a['year']}] {a['author']}: {a['lvef_change']} | {a['title'][:80]}")

# Export
output = []
for a in all_csp:
    output.append({
        "pmid": a["pmid"], "journal": a["journal"], "year": a["year"],
        "title": a["title"], "author": a["author"],
        "fine_cats": a["fine_cats"], "designs": a["designs"],
        "sample_size": a["sample_size"], "lvef_change": a["lvef_change"],
        "has_abstract": a["has_abstract"],
    })
with open(DATA_DIR / "lbbap_deep.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"\nExported to {DATA_DIR / 'lbbap_deep.json'}")
