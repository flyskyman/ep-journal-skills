#!/usr/bin/env bash
NN="$1"
OUT="data/codings_codex/codex_${NN}.json"
# skip if already valid
if [ -f "$OUT" ] && python -c "import json,sys; d=json.load(open('$OUT')); sys.exit(0 if len(d.get('codings',[]))>=1 else 1)" 2>/dev/null; then
  echo "skip $NN (done)"; exit 0
fi
read -r -d '' PROMPT <<'EOF'
You are an independent research coder labeling biomedical journal abstracts on a fixed codebook. You are BLIND to which journal each came from; judge only the text. Read the file data/chunks_v2/chunk_NN_PLACEHOLDER.json (a JSON array of {id,title,abstract}). For EACH abstract assign EXACTLY ONE allowed value per dimension.

study_type: original_clinical | original_preclinical_basic | ai_ml | meta_analysis_review | case_report_series | other
gap_type (the precise knowledge deficit claimed): mechanistic_deficit | comparative_unknown | capability_gap | guideline_inadequacy | feasibility_in_niche | optimization_unknown | prevalence_or_characterization | literature_void_weak | no_clear_gap
contribution_frame (what the paper offers): mechanism_insight | realworld_scale_evidence | validated_ai_capability | clinical_decision_change | comparative_effectiveness | procedural_refinement | evidence_synthesis_meta | feasibility_safety_demo | prognostic_predictor
results_logic: effectsize_comparator_ci | p_value_only | discriminator_threshold_roc | noninferiority | meta_pooled_effect | descriptive_only
benchmarking: vs_guideline_standard | vs_alternative_technique | vs_baseline_prepost | vs_existing_model | none
conclusion_stance: decisive_clinical | mechanistic_elevation | translational_honest | practical_modest | exploratory_hypothesis_generating | null_finding_neutral
certainty_calibration (does the closing claim fit the design): matches_design | overclaims | underclaims
voice: first_person_we | impersonal
external_validation: external | internal_only | not_applicable

Return ONLY the structured object with a codings array, one element per abstract.
EOF
PROMPT="${PROMPT//NN_PLACEHOLDER/$NN}"
codex exec -C "C:/Projects/jouranl-title" --skip-git-repo-check --ephemeral -s read-only \
  --output-schema data/codex_schema.json -o "$OUT" "$PROMPT" >/dev/null 2>&1
# validate
if python -c "import json,sys; d=json.load(open('$OUT')); sys.exit(0 if len(d.get('codings',[]))>=1 else 1)" 2>/dev/null; then
  echo "ok $NN"
else
  echo "FAIL $NN"
fi
