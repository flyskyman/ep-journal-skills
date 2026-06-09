#!/usr/bin/env python3
"""Parse PubMed JSON results and generate jacc_ep_abstracts.csv"""

import json
import csv
import html
import re
import os

# Result files from PubMed batch queries
RESULT_DIR = r"C:\Users\flysk\.claude\projects\C--Projects-jouranl-title\fd224ed8-9840-4ab2-8361-9c6e6533c2a0\tool-results"

FILE_RESULTS = [
    os.path.join(RESULT_DIR, "toolu_01Y9v3fAidrWCceLH6CMpUHm.txt"),  # batch 1 (20)
    os.path.join(RESULT_DIR, "toolu_01WaxWL91sFJqv1kDxnC8o6T.txt"),  # batch 2 (20)
    os.path.join(RESULT_DIR, "toolu_011iBfcvr1MkkTNAtELLLQto.txt"),  # batch 3 (20)
    os.path.join(RESULT_DIR, "toolu_017PpzZM6ZZV66pgyP3UF8Uf.txt"),  # batch 5 (13)
]

# Inline batch 4 (14 articles) and batch 6 (10 articles) returned directly in the conversation
# We need to reconstruct these from the tool output

def decode_html_entities(text):
    """Decode HTML entities like &#x2265; and &#xa0;"""
    if not text:
        return text
    # First pass: html.unescape handles named and numeric entities
    text = html.unescape(text)
    # Remove any remaining XML-style entities
    text = re.sub(r'&#x[0-9a-fA-F]+;', '', text)
    return text

def clean_abstract(abstract):
    """Clean abstract text"""
    if not abstract or abstract == "[Abstract not available]":
        return "N/A"
    abstract = decode_html_entities(abstract)
    # Replace newlines with spaces
    abstract = abstract.replace('\n', ' ').replace('\r', ' ')
    # Collapse multiple spaces
    abstract = re.sub(r'\s+', ' ', abstract).strip()
    return abstract

def get_first_author(authors):
    """Extract first author last name"""
    if not authors or len(authors) == 0:
        return "N/A"
    return decode_html_entities(authors[0].get('last_name', 'N/A'))

def get_year(pub_date):
    """Extract publication year"""
    if not pub_date:
        return "N/A"
    return pub_date.get('year', 'N/A')

def parse_articles(data):
    """Parse articles from a JSON structure"""
    articles = []
    for art in data.get('articles', []):
        pmid = art['identifiers']['pmid']
        title = decode_html_entities(art.get('title', 'N/A'))
        year = get_year(art.get('publication_date', {}))
        abstract = clean_abstract(art.get('abstract', ''))
        first_author = get_first_author(art.get('authors', []))
        articles.append({
            'PMID': pmid,
            'Year': year,
            'Title': title,
            'Abstract': abstract,
            'FirstAuthor': first_author,
        })
    return articles

def main():
    all_articles = {}  # keyed by PMID to deduplicate

    # Parse file results
    for fpath in FILE_RESULTS:
        if not os.path.exists(fpath):
            print(f"WARNING: File not found: {fpath}")
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for art in parse_articles(data):
            all_articles[art['PMID']] = art
        print(f"Parsed {len(data.get('articles', []))} articles from {os.path.basename(fpath)}")

    # Required PMIDs
    required_pmids = [
        "42047422","42029372","41995655","41973899","41954553","41860505","41817497",
        "41790087","41790086","41134245","41134241","41498721","41441802","41416973",
        "41348081","41288542","41288540","41263722","40938228","40866024","40866023",
        "40838921","40772890","40767798","40738599","40738598","40569238","40569236",
        "40569235","40504057","40471767","40439650","40439644","40439643","40372330",
        "40338779","40208157","40117417","40100197","40100196","40099772","39945715",
        "39846924","39808087","39570266","39480392","39603761","39520430","39477681",
        "39425726","39387744","39387739","39387738","39387737","39340506","39297841",
        "39243257","39243255","39177552","38970598","38934972","38878013","38842977",
        "38842969","38829298","38597855","38551549","38363277","38340117","38267169",
        "38267165","38127008","38069976","37943191","37758375","37758374","37715742",
        "37611994","37589646","37558292","37498245","37498242","37480862","37438043",
        "37354171","37227341","37225308","37212761","36939662","36858703","36858692",
        "36858691","36858690","36752453","36752449","36697195","36697194"
    ]

    # Inline data for batch 4 (returned directly, not saved to file)
    batch4_inline = [
        {"PMID": "40866023", "Year": "2025", "Title": "Septal Perforation During Left Bundle Branch Pacing: Into the Abyss of the Unknown.", "Abstract": "N/A", "FirstAuthor": "Ponnusamy"},
        {"PMID": "40838921", "Year": "2025", "Title": "Rethinking Risk in Mitral Valve Prolapse: The Promise of Machine Learning and Multimodal Phenotyping.", "Abstract": "N/A", "FirstAuthor": "Deharo"},
        {"PMID": "40772890", "Year": "2025", "Title": "Seeing the Forest for the Trees: A Novel Marker for the His-Purkinje System.", "Abstract": "N/A", "FirstAuthor": "Hanna"},
        {"PMID": "40767798", "Year": "2025", "Title": "Fully Automated Anatomy Labeling for Intracardiac Echocardiography Using Deep Learning.", "Abstract": "Intracardiac echocardiography (ICE) is increasingly being used to guide electrophysiologic (EP) procedures but requires a considerable learning curve. ICE images collected from 2 separate institutions (605 EP procedures, 196,768 images) were used to develop an automated deep learning-based algorithm to detect anatomic structures from the right atrium. Fifteen of 21 anatomic structures were correctly identified with >70% precision and recall. Mislabeling of one anatomic structure for another was rare. This fully automated anatomy labeling algorithm can serve as an education tool or can be used as a navigation tool to guide ICE operators in EP procedures.", "FirstAuthor": "Gol Gungor"},
        {"PMID": "40738599", "Year": "2025", "Title": "Reply: QS Morphology in a Nonfiltered Unipolar Electrogram From a Left Bundle Branch Pacing Lead.", "Abstract": "N/A", "FirstAuthor": "Kato"},
        {"PMID": "40738598", "Year": "2025", "Title": "QS Morphology in a Nonfiltered Unipolar Electrogram From a Left Bundle Branch Pacing Lead.", "Abstract": "N/A", "FirstAuthor": "Iida"},
        {"PMID": "40569238", "Year": "2025", "Title": "New ECG Morphologic Criteria for the Identification of Left Bundle Branch Capture.", "Abstract": "Identification of left bundle branch capture (LBBc) during left bundle branch area pacing remains challenging. This study sought to validate the utility of new simple morphologic criteria for the identification of LBBc. Patients with proven LBBc based on the presence of QRS transition during decremental output pacing were included. The paced VQRS upstroke/downstroke was quantitatively and qualitatively evaluated, and classified as fast or slow, with fast upstroke patterns associated with LBBc and slow upstroke patterns with left ventricular septal capture (LVSc). Additionally, the appearance of a paced QRS downstroke slurring/notching in any lead not previously present during lead penetration and/or an M QRS pattern in inferior leads was also considered suggestive of LBBc. Accuracy of these criteria was tested by independent evaluators using exclusively qualitative electrocardiogram morphologic features. 115 patients with proven LBBc were included. Mean VQRS upstroke duration during LBBc was significantly shorter than during LVSc (34.6 +/- 10.1 ms vs 63.2 +/- 12.1 ms; P < 0.001). A paced Vupstroke/downstroke ratio <1 had a sensitivity and specificity of 0.97 and 0.95 for the identification of LBBc. A slurred/notched QRS downstroke or M pattern in inferior leads was present in 91.1% during LBBc in baseline narrow QRS patients with inferior paced QRS axis, with sensitivity and specificity being 0.91 and 0.87, respectively. Using exclusively qualitative criteria, independent evaluators were able to identify the correct capture pattern in 87% of LBBc and 89% of LVSc cases, with diagnostic accuracy being significantly lower among dilated cardiomyopathy patients: 70.4% vs 93%; P = 0.004. Simple electrocardiogram morphologic criteria can accurately identify LBBc during left bundle branch area pacing in patients with baseline narrow QRS and/or without cardiomyopathy.", "FirstAuthor": "Cano"},
        {"PMID": "40569236", "Year": "2025", "Title": "Left Ventricular Mechanics During Left Ventricular Septal Pacing are Similar to Those During Left Bundle Branch Pacing.", "Abstract": "N/A", "FirstAuthor": "Prinzen"},
        {"PMID": "40569235", "Year": "2025", "Title": "Demystifying the Electrocardiogram of Left Bundle Branch Area Pacing.", "Abstract": "N/A", "FirstAuthor": "Burri"},
        {"PMID": "40504057", "Year": "2025", "Title": "Conduction System Pacing for Resynchronization Therapy: CONSYSTent and Beyond.", "Abstract": "N/A", "FirstAuthor": "Chelu"},
        {"PMID": "40471767", "Year": "2025", "Title": "Detecting Arrhythmogenic Right Ventricular Cardiomyopathy From the Electrocardiogram Using Deep Learning.", "Abstract": "N/A", "FirstAuthor": "Sigfstead"},
        {"PMID": "40439650", "Year": "2025", "Title": "Left Ventricular Mechanical Insights Into Left Bundle Branch Pacing and Left Ventricular Septal Pacing.", "Abstract": "The relationship between left ventricular (LV) mechanical efficiency and various modalities of left bundle branch area pacing (LBBAP) is not well understood. The goal of this study was to evaluate the correlation between 2 different modalities of LBBAP, including left bundle branch pacing (LBBP) and LV septal pacing (LVSP) and myocardial work (MW), during spontaneous rhythm and LBBAP in patients with normal or moderately reduced LV ejection fraction. Patients were retrieved from the TREEBEARD prospective study and categorized into 2 groups based on whether they received LBBP or LVSP. MW was assessed using metrics such as global work index, global constructive work, global wasted work, and global work efficiency. Overall, 155 patients were included in the study (mean age 73.3 +/- 14.3 years; 74.8% male), with 102 in the LBBP group and 53 in the LVSP group. In the LBBP group, all MW indices displayed a strong correlation between values recorded during spontaneous rhythm and LBBP. Conversely, the LVSP group exhibited moderate correlations for global work index (r = 0.535; P = 0.004), global constructive work (r = 0.587; P = 0.009), and global work efficiency (r = 0.503; P = 0.01). Global wasted work did not show a statistically significant correlation (r = 0.641; P = 0.13). In patients with preserved or moderately reduced LV ejection fraction, LBBP exhibited LV mechanical efficiency comparable to that of spontaneous LV activation. Conversely, LVSP is a valuable option, but LV mechanics is impaired, showing a reduced GWE of the left ventricle.", "FirstAuthor": "Bertini"},
        {"PMID": "40439644", "Year": "2025", "Title": "Septal Intramyocardial Purkinje Network: A Potential New Mechanism Explaining Left Bundle Branch Area Pacing Physiology.", "Abstract": "Despite the growing use of left bundle branch area pacing (LBBAP) to deliver conduction system pacing, the mechanism underlying the narrow QRS interval conferred by this pacing modality remains unclear. This study aimed to evaluate the mechanism that provides a most plausible explanation of LBBAP physiology. A cohort of 13 patients who had surface electrocardiographic (ECG) or intracardiac recording features not explainable by either selective or nonselective LBBAP were evaluated. Unique ECG patterns and intracardiac recordings over the right interventricular septum were analyzed, as well as septal Purkinje fiber staining patterns in human cardiac tissue, to assess whether such findings can be attributed to the capture of the recently discovered intramyocardial Purkinje network. The following unexpected ECG and intracardiac recording patterns were observed during LBBAP: 1) alternating incomplete right bundle branch block and left bundle branch block in an output-independent and output-dependent fashion; 2) variable, instead of all-or-none, recruitment of both left and right bundle systems; 3) correction of baseline right bundle branch block at low outputs; 4) paced QRS axis and duration closely matching the baseline narrow QRS interval in patients who underwent atrioventricular node ablation; and 5) intracardiac recordings demonstrating rapid, apparently nonphysiological activation of the right ventricular septum. Additionally, extensive Purkinje tissue was identified deep inside the septal myocardium in the human heart near the usual location of the LBBAP lead. These data suggest a potential physiological role of the intramyocardial Purkinje system. Direct capture of Purkinje fibers connected to both bundle branches to rapidly activate both ventricles could provide a unifying explanation for these counterintuitive findings.", "FirstAuthor": "Liu"},
        {"PMID": "40439643", "Year": "2025", "Title": "Simultaneous Right and Left Bundle Pacing: Rationale and Feasibility in Lieu of His Bundle Pacing.", "Abstract": "N/A", "FirstAuthor": "Trivedi"},
    ]

    # Inline data for batch 6 (10 articles)
    batch6_inline = [
        {"PMID": "37212761", "Year": "2023", "Title": "Left Bundle Branch Area Pacing Versus Biventricular Pacing as Initial Strategy for Cardiac Resynchronization.", "Abstract": "Left bundle branch area pacing (LBBAP) for cardiac resynchronization therapy (CRT) is an alternative to biventricular pacing (BiVp). The purpose of this study was to compare the outcomes between LBBAP and BiVp as an initial implant strategy for CRT. In this prospective multicenter, observational, nonrandomized study, first-time CRT implant recipients with LBBAP or BiVp were included. The primary efficacy outcome was a composite of heart failure (HF)-related hospitalization and all-cause mortality. The primary safety outcomes were acute and long-term complications. Secondary outcomes included postprocedural New York Heart Association functional class and electrocardiographic and echocardiographic parameters. A total of 371 patients (median follow-up of 340 days [IQR: 206-477 days]) were included. The primary efficacy outcome occurred in 24.2% in the LBBAP vs 42.4% in the BiVp (HR: 0.621 [95% CI: 0.415-0.93]; P = 0.021) group, driven by a reduction in HF-related hospitalizations (22.6% vs 39.5%; HR: 0.607 [95% CI: 0.397-0.927]; P = 0.021) without significant difference in all-cause mortality (5.5% vs 11.9%; P = 0.19) or differences in long-term complications (LBBAP: 9.4% vs BiVp: 15.2%; P = 0.146). LBBAP resulted in shorter procedural (95 minutes [IQR: 65-120 minutes] vs 129 minutes [IQR: 103-162 minutes]; P < 0.001) and fluoroscopy times (12 minutes [IQR: 7.4-21.1 minutes] vs 21.7 minutes [IQR: 14.3-30 minutes]; P < 0.001), shorter QRS duration (123.7 +/- 18 milliseconds vs 149.3 +/- 29.1 milliseconds; P < 0.001), and higher postprocedural left ventricular ejection fraction (34.1% +/- 12.5% vs 31.4% +/- 10.8%; P = 0.041). LBBAP as an initial CRT strategy resulted in a lower risk of HF-related hospitalizations compared to BiVp. A reduction in procedural and fluoroscopy times, shorter paced QRS duration, and improvements in left ventricular ejection fraction compared with BiVp were observed.", "FirstAuthor": "Diaz"},
        {"PMID": "36939662", "Year": "2023", "Title": "JACC Journals' Pathway Forward With AI Tools: The Future Is Now.", "Abstract": "N/A", "FirstAuthor": "Fuster"},
        {"PMID": "36858703", "Year": "2022", "Title": "Response to Para-Hisian Pacing in the Setting of Presence of a Concealed Nodoventricular/Nodofascicular Pathway.", "Abstract": "N/A", "FirstAuthor": "Nagashima"},
        {"PMID": "36858692", "Year": "2022", "Title": "Development of an AI-Driven QT Correction Algorithm for Patients in Atrial Fibrillation.", "Abstract": "Prolongation of the QTc interval is associated with the risk of torsades de pointes. Determination of the QTc interval is therefore of critical importance. There is no reliable method for measuring or correcting the QT interval in atrial fibrillation (AF). The authors sought to evaluate the use of a convolutional neural network (CNN) applied to AF electrocardiograms (ECGs) for accurately estimating the QTc interval and ruling out prolongation of the QTc interval. The authors identified patients with a 12-lead ECG in AF within 10 days of a sinus ECG, with similar (+/-10 ms) QRS durations, between October 23, 2001, and November 5, 2021. A multilayered deep CNN was implemented in TensorFlow 2.5 (Google) to predict the MUSE (GE Healthcare) software-generated sinus QTc value from an AF ECG waveform, demographic characteristics, and software-generated features. The study identified 6,432 patients (44% female) with an average age of 71 years. The CNN predicted sinus QTc values with a mean absolute error of 22.2 ms and root mean squared error of 30.6 ms, similar to the intrinsic variability of the sinus QTc interval. Approximately 84% and 97% of the model's predictions were contained within 1 SD (+/-30.6 ms) and 2 SD (+/-61.2 ms) from the sinus QTc interval. The model outperformed the AFQTc method, exhibiting narrower error ranges (mean absolute error comparison P < 0.0001). The model performed best for ruling out QTc prolongation (negative predictive value 0.82 male, 0.92 female; specificity 0.92 male, 0.97 female). A CNN model applied to AF ECGs accurately predicted the sinus QTc interval, outperforming current alternatives and exhibiting a high negative predictive value.", "FirstAuthor": "Tarabanis"},
        {"PMID": "36858691", "Year": "2023", "Title": "Smart Devices in Detecting AF: Excellent Signal Quality, But AI Can Still Learn From Clinicians.", "Abstract": "N/A", "FirstAuthor": "Teh"},
        {"PMID": "36858690", "Year": "2023", "Title": "Clinical Validation of 5 Direct-to-Consumer Wearable Smart Devices to Detect Atrial Fibrillation: BASEL Wearable Study.", "Abstract": "Multiple smart devices capable to detect atrial fibrillation (AF) are presently available. Sensitivity and specificity for the detection of AF may differ between available smart devices, and this has not yet been adequately investigated. The aim was to assess the accuracy of 5 smart devices in identifying AF compared with a physician-interpreted 12-lead electrocardiogram as the reference standard in a real-world cohort of patients. We consecutively enrolled patients presenting to a cardiology service at a tertiary referral center in a prospective, diagnostic study. We prospectively analyzed 201 patients (31% women, median age 66.7 years). AF was present in 62 (31%) patients. Sensitivity and specificity for the detection of AF were comparable between devices: 85% and 75% for the Apple Watch 6, 85% and 75% for the Samsung Galaxy Watch 3, 58% and 75% for the Withings Scanwatch, 66% and 79% for the Fitbit Sense, and 79% and 69% for the AliveCor KardiaMobile, respectively. The rate of inconclusive tracings was 18%, 17%, 24%, 21%, and 26% for the Apple Watch 6, Samsung Galaxy Watch 3, Withings Scan Watch, Fitbit Sense, and AliveCor KardiaMobile (P < 0.01 for pairwise comparison), respectively. By manual review of inconclusive tracings, the rhythm could be determined in 955 (99%) of 969 single-lead electrocardiograms. Regarding patient acceptance, the Apple Watch was ranked first (39% of participants). In this clinical validation of 5 direct-to-consumer smart devices, we found differences in the amount of inconclusive tracings diminishing sensitivity and specificity of the smart devices. In a clinical setting, manual review of tracings is required in about one-fourth of cases.", "FirstAuthor": "Mannhart"},
        {"PMID": "36752453", "Year": "2022", "Title": "Clinical Outcomes in Conduction System Pacing Compared to Right Ventricular Pacing in Bradycardia.", "Abstract": "Conduction system pacing (CSP) provides more physiological ventricular activation than right ventricular pacing (RVP). This study evaluated the differences in clinical outcomes in patients receiving CSP and RVP. Consecutive patients with pacemakers implanted for bradycardia from 2016 to 2021 in 2 centers were prospectively followed for the primary composite outcome of heart failure (HF) hospitalizations, upgrade to biventricular pacing, or all-cause mortality, stratified by ventricular pacing burden (Vp). Among 860 patients (mean age 74 +/- 11 years, 48% female, 48% atrioventricular block), 628 received RVP and 231 received CSP (95 His-bundle pacing, 136 left bundle branch pacing). The primary outcome occurred in 217 (25%) patients, more commonly in patients with RVP than CSP (30% vs 13%, P < 0.001). In multivariable analyses, CSP was independently associated with 47% reduction of the primary outcome (adjusted hazard ratio [AHR]: 0.53; 95% CI: 0.29-0.97; P = 0.04) and HF hospitalization alone (AHR: 0.40; 95% CI: 0.17-0.95; P = 0.04), among only patients with Vp >20%. CSP significantly reduced adverse clinical outcomes for bradycardic patients requiring ventricular pacing and should be the preferred pacing modality of choice.", "FirstAuthor": "Tan"},
        {"PMID": "36752449", "Year": "2022", "Title": "Conduction System Pacing Versus Conventional Cardiac Resynchronization Therapy in Congenital Heart Disease.", "Abstract": "Dyssynchrony-associated left ventricular systolic dysfunction is a major contributor to heart failure in congenital heart disease (CHD). Although conventional cardiac resynchronization therapy (CRT) has shown benefit, the comparative efficacy of cardiac conduction system pacing (CSP) is unknown. The purpose of this study was compare the clinical outcomes of CSP vs conventional CRT in CHD with biventricular, systemic left ventricular anatomy. Retrospective CSP data from 7 centers were compared with propensity score-matched conventional CRT control subjects. Outcomes were lead performance, change in left ventricular ejection fraction (LVEF), and QRS duration at 12 months. A total of 65 CSP cases were identified (mean age 37 +/- 21 years, 46% men). CSP can be reliably achieved in biventricular, systemic left ventricular CHD patients with similar improvement in LVEF and greater QRS narrowing for CSP vs conventional CRT at 1 year. Among CSP patients, pacing electrical parameters were superior for LBBAP vs HBP.", "FirstAuthor": "Moore"},
        {"PMID": "36697195", "Year": "2022", "Title": "Interventricular Septal Hematoma With Pericardial Effusion After Left Bundle Branch Pacing Implantation.", "Abstract": "N/A", "FirstAuthor": "Chen"},
        {"PMID": "36697194", "Year": "2022", "Title": "Electrical Resynchronization After Left Bundle Branch Pacing.", "Abstract": "N/A", "FirstAuthor": "Ponnusamy"},
    ]

    # Add inline articles (only if not already present from files)
    for art in batch4_inline + batch6_inline:
        if art['PMID'] not in all_articles:
            all_articles[art['PMID']] = art

    # Check coverage
    missing = [p for p in required_pmids if p not in all_articles]
    print(f"\nTotal unique articles: {len(all_articles)}")
    print(f"Required PMIDs: {len(required_pmids)}")
    print(f"Missing PMIDs: {len(missing)}")
    if missing:
        print(f"Missing: {missing}")

    # Sort by year descending, then by PMID descending
    rows = [all_articles[p] for p in required_pmids if p in all_articles]
    rows.sort(key=lambda x: (-(int(x['Year']) if x['Year'].isdigit() else 0), -int(x['PMID'])))

    # Write CSV
    output_path = r"C:\Projects\jouranl-title\data\jacc_ep_abstracts.csv"
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['PMID', 'Year', 'Title', 'Abstract', 'FirstAuthor'],
                                quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nCSV written to: {output_path}")
    print(f"Total rows: {len(rows)}")

    # Show year distribution
    from collections import Counter
    year_counts = Counter(r['Year'] for r in rows)
    for y in sorted(year_counts.keys(), reverse=True):
        print(f"  {y}: {year_counts[y]} articles")

if __name__ == '__main__':
    main()
