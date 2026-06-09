export const meta = {
  name: 'loop-r2-judge',
  description: 'Round-1 blind judging (Claude) of skill-vs-noskill and skill-vs-original abstract pairs',
  phases: [{ title: 'Judge', detail: 'one agent per blinded pair; writes judge_out/<tid>.json' }],
}

const DIR = 'C:/Projects/jouranl-title/data/loop_r2';
const tids = ['1_AvB','1_AvO','2_AvB','2_AvO','3_AvB','3_AvO','4_AvB','4_AvO','5_AvB','5_AvO','6_AvB','6_AvO','7_AvB','7_AvO','8_AvB','8_AvO','9_AvB','9_AvO','10_AvB','10_AvO','11_AvB','11_AvO','12_AvB','12_AvO','13_AvB','13_AvO','14_AvB','14_AvO','15_AvB','15_AvO'];

const RET = { type: 'object', required: ['tid', 'done'], properties: { tid: { type: 'string' }, done: { type: 'boolean' } } };

function prompt(tid) {
  return `Read the file ${DIR}/judge_tasks/${tid}.txt — it contains a complete, self-contained instruction asking you to blindly compare two abstracts (labeled X and Y) written for an EP journal, scoring each on a rubric. Follow that instruction exactly as an impartial expert EP-journal editor. Do NOT read any other file.

Then write your judgment as STRICT JSON to ${DIR}/judge_out/${tid}.json with EXACTLY these keys:
{"x_scores":{"gap_specificity":<1-5>,"results_rigor":<1-5>,"certainty_calibration":<1-5>,"journal_fit":<1-5>,"clarity":<1-5>},"y_scores":{"gap_specificity":<1-5>,"results_rigor":<1-5>,"certainty_calibration":<1-5>,"journal_fit":<1-5>,"clarity":<1-5>},"winner":"X"|"Y"|"tie","rationale":"<one sentence>","loser_weakness":"<what the weaker abstract most lacked>"}
Integer scores only; valid JSON only in that file.

Return {tid:"${tid}", done:true}.`;
}

phase('Judge');
const results = await parallel(tids.map((tid) => () =>
  agent(prompt(tid), { label: `judge:${tid}`, phase: 'Judge', model: 'sonnet', schema: RET })));
const ok = results.filter(Boolean).length;
log(`judged ${ok}/${tids.length} pairs`);
return { ok, total: tids.length };
