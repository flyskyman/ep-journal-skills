export const meta = {
  name: 'abstract-coding-v2',
  description: 'Blind-code 1677 EP-journal abstracts (expanded representative corpus) on the content codebook (Sonnet, 140 batches)',
  phases: [{ title: 'Classify', detail: 'one agent per 12-abstract chunk; writes coded_NNN.json' }],
}

const CODEBOOK = `
DIMENSIONS (assign EXACTLY ONE allowed value per dimension):

study_type: original_clinical | original_preclinical_basic | ai_ml | meta_analysis_review | case_report_series | other

gap_type — the precise knowledge deficit the abstract claims to fill:
  mechanistic_deficit | comparative_unknown | capability_gap | guideline_inadequacy | feasibility_in_niche | optimization_unknown | prevalence_or_characterization | literature_void_weak | no_clear_gap

opening_move: premise_then_however | aim_first | hypothesis_first | trial_or_cohort_name_first | entity_definition | clinical_problem_first

contribution_frame: mechanism_insight | realworld_scale_evidence | validated_ai_capability | clinical_decision_change | comparative_effectiveness | procedural_refinement | evidence_synthesis_meta | feasibility_safety_demo | prognostic_predictor

results_logic: effectsize_comparator_ci | p_value_only | discriminator_threshold_roc | noninferiority | meta_pooled_effect | descriptive_only

benchmarking: vs_guideline_standard | vs_alternative_technique | vs_baseline_prepost | vs_existing_model | none

conclusion_stance: decisive_clinical | mechanistic_elevation | translational_honest | practical_modest | exploratory_hypothesis_generating | null_finding_neutral

certainty_calibration: matches_design | overclaims | underclaims

voice: first_person_we | impersonal

external_validation: external | internal_only | not_applicable
`;

const SCHEMA = {
  type: 'object', required: ['chunk', 'coded', 'novel_count'],
  properties: { chunk: { type: 'integer' }, coded: { type: 'integer' }, novel_count: { type: 'integer' } },
};

const DIR = 'C:/Projects/jouranl-title/data';

function prompt(nn) {
  return `You are a research coder labeling biomedical journal abstracts on a FIXED codebook.
You are BLIND to which journal each abstract came from. Do NOT guess the journal. Code ONLY the rhetorical/scientific content.

STEP 1 — Read ${DIR}/chunks_v2/chunk_${nn}.json (a JSON array of {id, title, abstract}).
STEP 2 — For EACH abstract assign EXACTLY ONE allowed value per dimension:${CODEBOOK}
STEP 3 — For each abstract set fits_codebook:false + a SHORT novel_pattern ONLY if a salient content move escapes the codebook; else fits_codebook:true, novel_pattern:"". Give evidence_quote: a <=15-word verbatim quote anchoring gap_type AND conclusion_stance.
STEP 4 — Write results with the Write tool to ${DIR}/codings_v2/coded_${nn}.json as a JSON array. Each element MUST have EXACTLY these keys:
{"id":<int>,"study_type":"...","gap_type":"...","opening_move":"...","contribution_frame":"...","results_logic":"...","benchmarking":"...","conclusion_stance":"...","certainty_calibration":"...","voice":"...","external_validation":"...","fits_codebook":<bool>,"novel_pattern":"...","evidence_quote":"..."}
Use ONLY the allowed lowercase_underscore enum values. Output valid JSON only.

Return {chunk:${parseInt(nn,10)}, coded:<count>, novel_count:<count with fits_codebook=false>}.`;
}

phase('Classify');
const nns = Array.from({ length: 140 }, (_, i) => String(i + 1).padStart(3, '0'));
const results = await parallel(
  nns.map((nn) => () =>
    agent(prompt(nn), { label: `code:${nn}`, phase: 'Classify', model: 'sonnet', schema: SCHEMA })
  )
);
const ok = results.filter(Boolean);
const failed = nns.filter((nn, i) => !results[i]);
log(`coded ${ok.reduce((s, r) => s + (r.coded || 0), 0)}/1677 across ${ok.length}/140; novel=${ok.reduce((s, r) => s + (r.novel_count || 0), 0)}; failed=[${failed.join(',')}]`);
return { chunksOk: ok.length, failed, totalNovel: ok.reduce((s, r) => s + (r.novel_count || 0), 0) };
