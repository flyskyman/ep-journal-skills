export const meta = {
  name: 'abstract-coding',
  description: 'Blind-code 414 EP-journal abstracts on a fixed content codebook (Sonnet, 60 batches)',
  phases: [{ title: 'Classify', detail: 'one agent per 7-abstract chunk; writes coded_NN.json' }],
}

// ---- Codebook (the scientific instrument). Agents code BLIND to journal. ----
const CODEBOOK = `
DIMENSIONS (assign EXACTLY ONE allowed value per dimension):

study_type: original_clinical | original_preclinical_basic | ai_ml | meta_analysis_review | case_report_series | other

gap_type — the precise knowledge deficit the abstract claims to fill:
  mechanistic_deficit       = a mechanism/extent/relationship is "incompletely characterized/understood"
  comparative_unknown       = head-to-head effect of A vs B is unknown/elusive
  capability_gap            = a needed capability (detect/predict X) is hard/absent today
  guideline_inadequacy      = current guideline/standard tool has limited accuracy/scope
  feasibility_in_niche      = feasibility/safety unknown in a specific population/setting
  optimization_unknown      = optimal parameter/strategy of an accepted therapy is unknown
  prevalence_or_characterization = aims to describe/characterize an entity or its frequency
  literature_void_weak      = gap stated only as "few/no/limited studies" with no specific deficit
  no_clear_gap              = no identifiable gap statement

opening_move — how sentence 1-2 open:
  premise_then_however | aim_first | hypothesis_first | trial_or_cohort_name_first | entity_definition | clinical_problem_first

contribution_frame — what the paper offers:
  mechanism_insight | realworld_scale_evidence | validated_ai_capability | clinical_decision_change |
  comparative_effectiveness | procedural_refinement | evidence_synthesis_meta | feasibility_safety_demo | prognostic_predictor

results_logic — dominant way results are reported:
  effectsize_comparator_ci | p_value_only | discriminator_threshold_roc | noninferiority | meta_pooled_effect | descriptive_only

benchmarking — what the result is measured against:
  vs_guideline_standard | vs_alternative_technique | vs_baseline_prepost | vs_existing_model | none

conclusion_stance — the final 1-2 sentences:
  decisive_clinical            = strong clinical-utility claim
  mechanistic_elevation        = elevates finding to physiology/mechanism significance
  translational_honest         = translational claim + explicit acknowledgement of what's still unknown
  practical_modest             = modest feasibility/practical claim
  exploratory_hypothesis_generating = explicitly exploratory / hypothesis-generating / needs RCT
  null_finding_neutral         = neutral statement of a no-difference result

certainty_calibration — does the conclusion's strength match the study design?
  matches_design | overclaims | underclaims

voice: first_person_we (uses "we ...") | impersonal ("this study ...")

external_validation: external (validated in a separate cohort) | internal_only | not_applicable
`;

const SCHEMA = {
  type: 'object',
  required: ['chunk', 'coded', 'novel_count'],
  properties: {
    chunk: { type: 'integer' },
    coded: { type: 'integer', description: 'number of abstracts coded and written' },
    novel_count: { type: 'integer', description: 'count of abstracts with fits_codebook=false' },
  },
};

const DIR = 'C:/Projects/jouranl-title/data';

function prompt(nn) {
  return `You are a research coder labeling biomedical journal abstracts on a FIXED codebook.
You are BLIND to which journal each abstract came from. Do NOT guess the journal. Code ONLY the rhetorical/scientific content of the abstract text.

STEP 1 — Read the file ${DIR}/chunks/chunk_${nn}.json (a JSON array of {id, title, abstract}).

STEP 2 — For EACH abstract, assign EXACTLY ONE allowed value per dimension below.
${CODEBOOK}

STEP 3 — For each abstract also set:
  fits_codebook: false (and fill novel_pattern with a SHORT phrase) ONLY if the abstract has a salient content/rhetorical move the codebook above cannot capture; otherwise fits_codebook: true and novel_pattern: "".
  evidence_quote: a <=15-word verbatim quote from the abstract that anchors your gap_type AND conclusion_stance codes.

STEP 4 — Write your results with the Write tool to ${DIR}/codings/coded_${nn}.json as a JSON array.
Each element MUST be an object with EXACTLY these keys:
{"id":<int>,"study_type":"...","gap_type":"...","opening_move":"...","contribution_frame":"...","results_logic":"...","benchmarking":"...","conclusion_stance":"...","certainty_calibration":"...","voice":"...","external_validation":"...","fits_codebook":<bool>,"novel_pattern":"...","evidence_quote":"..."}
Use ONLY allowed enum values exactly as written (lowercase with underscores). Output valid JSON only in that file.

Then return the summary object {chunk:${parseInt(nn,10)}, coded:<number coded>, novel_count:<number with fits_codebook=false>}.`;
}

phase('Classify');
const nns = Array.from({ length: 60 }, (_, i) => String(i + 1).padStart(2, '0'));
const results = await parallel(
  nns.map((nn) => () =>
    agent(prompt(nn), { label: `code:${nn}`, phase: 'Classify', model: 'sonnet', schema: SCHEMA })
  )
);
const ok = results.filter(Boolean);
const totalCoded = ok.reduce((s, r) => s + (r.coded || 0), 0);
const totalNovel = ok.reduce((s, r) => s + (r.novel_count || 0), 0);
const failed = nns.filter((nn, i) => !results[i]).map((nn) => nn);
log(`coded ${totalCoded}/414 across ${ok.length}/60 chunks; novel flags=${totalNovel}; failed chunks=[${failed.join(',')}]`);
return { totalCoded, totalNovel, chunksOk: ok.length, failedChunks: failed, perChunk: ok };
