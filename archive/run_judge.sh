#!/usr/bin/env bash
TID="$1"; OUT="data/loop_r1/judge_out/${TID}.json"
[ -f "$OUT" ] && python -c "import json;json.load(open('$OUT'))['winner']" 2>/dev/null && { echo "skip $TID"; exit 0; }
PROMPT="$(cat data/loop_r1/judge_tasks/${TID}.txt)"
codex exec -C "C:/Projects/jouranl-title" --skip-git-repo-check --ephemeral -s read-only \
  --output-schema data/judge_schema.json -o "$OUT" "$PROMPT" >/dev/null 2>&1
python -c "import json;json.load(open('$OUT'))['winner'];print('ok $TID')" 2>/dev/null || echo "FAIL $TID"
