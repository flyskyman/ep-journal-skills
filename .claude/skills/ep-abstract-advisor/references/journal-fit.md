# Journal fit — scope & format detail

Operational detail for Step 3 (fit) and Step 4 (format) of the skill. Numbers are full-corpus values (n=1,677, dual-model coded), **conditional on the sampled topic mix (2023–2026)** — treat them as in-corpus tendencies, not certified journal output rates. The content signal between journals is weak (see `evidence.md`); the two most robust levers are study-type fit and JACC's impersonal voice.

## Per-journal scope (Step 3)

| Journal | What it publishes / rewards (scope) | Dial up | Style knob |
|---------|-------------------------------------|---------|-----------|
| **HR** | Broadest scope; any topic. Slightly more decisive conclusions. Default home if fit is unclear. | A clear, confident takeaway | — |
| **Circ AE** | Mechanism & basic/preclinical science (highest preclinical share, 29%); highest mechanistic-deficit gaps (24%). Bench/translational work other EP journals won't take. | A hypothesis; mechanism; external validation if AI | "we" more common than elsewhere (~38%), but impersonal still the majority (62%) |
| **Europace** | Evidence synthesis & meta-analysis, registry/real-world, comparison studies (highest comparative-unknown gap, 23%). | A comparison/non-inferiority or synthesis; registry; reproducibility (NCT/PROSPERO/PRISMA) | — |
| **JACC EP** | Clinical studies argued quantitatively (highest effect-size+CI reporting, 38%). Smallest sample (n=200) → widest uncertainty. | Effect sizes + CI; P to 3 decimals | **Impersonal voice ~90%; prefer "this study sought to…" over "we"** — strong preference, not absolute (small n=200, voice reliability moderate κ=0.54) |
| **PACE** | Widest gate: case reports/series (30% in-corpus — by far the most of the six), feasibility/safety studies, meta-analyses. Lightest statistics (53% descriptive). | Practical feasibility/safety; success rate; keep stats simple | — |
| **JICE** | Interventional: technique head-to-head comparison & procedural refinement (highest "vs alternative technique", 42%). | The comparison (name both arms); procedural detail (sheath, capture type, distances); exploratory framing OK | "we" more common than JACC (~31%), but impersonal still majority (69%) |

How to use: match study **type** to a journal's scope first (case report → PACE not HR; bench mechanism → Circ AE; technique A-vs-B → JICE), then dial the listed emphasis. The six-move engine (skill Step 2) stays identical.

## Per-journal format (Step 4)

| Journal | Words (median [IQR]) | Original-research structure (real PubMed section labels) |
|---------|----------------------|----------------------------------------------------------|
| HR | 256 [246–270] | BACKGROUND / OBJECTIVE / METHODS / RESULTS / CONCLUSION |
| Circ AE | 281 [258–303] | BACKGROUND / METHODS / RESULTS / CONCLUSIONS (+REGISTRATION for trials) |
| Europace | 252 [241–267] | **AIMS / METHODS AND RESULTS / CONCLUSION** — Methods and Results are **one combined section** (ESC/Oxford house style; +CLINICAL TRIAL REGISTRATION) |
| JACC EP | 266 [251–280] | BACKGROUND / **OBJECTIVES** / METHODS / RESULTS / CONCLUSIONS; impersonal voice; P to 3 decimals |
| PACE | 230 [110–252] | BACKGROUND or INTRODUCTION / METHODS / RESULTS / CONCLUSION; case reports run short & unstructured |
| JICE | 252 [239–272] | BACKGROUND or PURPOSE / METHODS / RESULTS / CONCLUSION |

Structure (measured from PubMed XML, n=1,677): original research is structured in 86–96% of the original-research-heavy journals; PACE is 70% only because it carries the most case reports. Unstructured = article-type exception (case reports, images, narrative reviews, editorials, research letters), not a journal style. Match the exact label set; Europace's combined `METHODS AND RESULTS` is the one most authors get wrong.

## Worked examples
Three skill-generated abstracts (one each for PACE / Circ AE / JICE, from novel briefs) demonstrating the universal engine + scope fit + format: see `../../../../data/p4_claude_generations.md` (project data), or regenerate via the skill.
