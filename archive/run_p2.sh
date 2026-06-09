#!/usr/bin/env bash
NN="$1"; OUT="data/p2_pred/p2_${NN}.json"
[ -f "$OUT" ] && python -c "import json;json.load(open('$OUT'))['predictions']" 2>/dev/null && { echo "skip $NN"; exit 0; }
read -r -d '' P <<EOF
You are given electrophysiology journal abstracts with the journal name hidden. For EACH, predict which ONE of these six journals published it, using any cues you can find:
HR = Heart Rhythm; CircAE = Circulation: Arrhythmia and Electrophysiology; Europace; JACC = JACC: Clinical Electrophysiology; PACE = Pacing and Clinical Electrophysiology; JICE = Journal of Interventional Cardiac Electrophysiology.
Read data/p2_chunks/p2_${NN}.json (array of {id, abstract}). For each abstract give: id, predicted_journal (one code), confidence 0-1, and primary_cue (the single strongest signal you used, <=12 words). Return the structured predictions object.
EOF
codex exec -C "C:/Projects/jouranl-title" --skip-git-repo-check --ephemeral -s read-only --output-schema data/p2_schema.json -o "$OUT" "$P" >/dev/null 2>&1
python -c "import json;n=len(json.load(open('$OUT'))['predictions']);print('ok $NN ('+str(n)+')')" 2>/dev/null || echo "FAIL $NN"
