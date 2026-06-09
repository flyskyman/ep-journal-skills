#!/usr/bin/env bash
TID="$1"; OUT="data/loop_t2/judge_codex/${TID}.json"
[ -f "$OUT" ] && python -c "import json;json.load(open('$OUT'))['winner']" 2>/dev/null && { echo "skip $TID"; exit 0; }
PROMPT="$(cat data/loop_t2/judge_tasks/${TID}.txt)"
timeout 150 codex exec -C "C:/Projects/jouranl-title" --skip-git-repo-check --ephemeral -s read-only --output-schema data/title_judge_schema.json -o "$OUT" "$PROMPT" >/dev/null 2>&1
python -c "import json;json.load(open('$OUT'))['winner'];print('ok $TID')" 2>/dev/null || { echo "FAIL $TID"; rm -f "$OUT"; }
