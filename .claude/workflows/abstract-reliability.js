export const meta = {
  name: 'abstract-reliability',
  description: 'Independent second-coder pass on an 87-abstract stratified sample for inter-coder reliability (Sonnet, 13 batches)',
  phases: [{ title: 'Recode', detail: 'second coder, alternate framing; writes rel_coded_NN.json' }],
}

// Same enum values as coder 1 (for comparability) but DIFFERENT instructional framing
// to avoid shared-prompt anchoring: reviewer reasons first, then picks the category.
const CATS = `
study_type: original_clinical | original_preclinical_basic | ai_ml | meta_analysis_review | case_report_series | other
gap_type: mechanistic_deficit (a mechanism/extent/relationship is incompletely understood) | comparative_unknown (A-vs-B effect unknown) | capability_gap (a needed detect/predict capability is missing/hard) | guideline_inadequacy (current standard tool is inaccurate/limited) | feasibility_in_niche (works in this specific population/setting?) | optimization_unknown (best parameter/strategy of an accepted therapy unknown) | prevalence_or_characterization (describe an entity/its frequency) | literature_void_weak (gap is only "few/limited studies", no specific deficit) | no_clear_gap
opening_move: premise_then_however | aim_first | hypothesis_first | trial_or_cohort_name_first | entity_definition | clinical_problem_first
contribution_frame: mechanism_insight | realworld_scale_evidence | validated_ai_capability | clinical_decision_change | comparative_effectiveness | procedural_refinement | evidence_synthesis_meta | feasibility_safety_demo | prognostic_predictor
results_logic: effectsize_comparator_ci | p_value_only | discriminator_threshold_roc | noninferiority | meta_pooled_effect | descriptive_only
benchmarking: vs_guideline_standard | vs_alternative_technique | vs_baseline_prepost | vs_existing_model | none
conclusion_stance: decisive_clinical | mechanistic_elevation | translational_honest | practical_modest | exploratory_hypothesis_generating | null_finding_neutral
certainty_calibration: matches_design | overclaims | underclaims
voice: first_person_we | impersonal
external_validation: external | internal_only | not_applicable`;

const SCHEMA = {
  type: 'object',
  required: ['chunk', 'coded'],
  properties: { chunk: { type: 'integer' }, coded: { type: 'integer' } },
};

const DIR = 'C:/Projects/jouranl-title/data';

function prompt(nn) {
  return `You are an INDEPENDENT second reviewer auditing how biomedical abstracts are written. You have NOT seen any prior coding. You do NOT know which journal each came from — judge only the text.

Read ${DIR}/rel_chunks/rel_chunk_${nn}.json (array of {id, title, abstract}).

For EACH abstract, work in this order:
  1. In your head, identify the actual rhetorical FUNCTION of (a) the opening, (b) the stated gap, (c) what the paper offers, (d) how results are argued, (e) the closing claim.
  2. THEN map each to the single best-fitting category from the controlled vocabulary below. If two seem close, pick the one matching the DOMINANT move. Use the exact lowercase_underscore tokens.

Controlled vocabulary:${CATS}

Also judge:
  certainty_calibration: does the closing claim's strength fit the study design (sample size, design, validation)? matches_design / overclaims / underclaims.

Write results with the Write tool to ${DIR}/rel_codings/rel_coded_${nn}.json as a JSON array. Each element MUST have EXACTLY these keys (string values from the vocabulary; no extra keys):
{"id":<int>,"study_type":"...","gap_type":"...","opening_move":"...","contribution_frame":"...","results_logic":"...","benchmarking":"...","conclusion_stance":"...","certainty_calibration":"...","voice":"...","external_validation":"..."}

Then return {chunk:${parseInt(nn, 10)}, coded:<count>}.`;
}

phase('Recode');
const nns = Array.from({ length: 13 }, (_, i) => String(i + 1).padStart(2, '0'));
const results = await parallel(
  nns.map((nn) => () =>
    agent(prompt(nn), { label: `recode:${nn}`, phase: 'Recode', model: 'sonnet', schema: SCHEMA })
  )
);
const ok = results.filter(Boolean);
const failed = nns.filter((nn, i) => !results[i]);
log(`recoded ${ok.reduce((s, r) => s + (r.coded || 0), 0)}/87; failed=[${failed.join(',')}]`);
return { chunksOk: ok.length, failed };
