export const meta = {
  name: 'loop-t1-generate',
  description: 'Title-skill validation: generate title (skill vs no-skill) from held-out briefs',
  phases: [{ title: 'Generate', detail: 'title A (skill) and B (no-skill) from each brief' }],
}
const D = 'C:/Projects/jouranl-title/data';
const SKILL = 'C:/Projects/jouranl-title/.claude/skills/ep-title-advisor/SKILL.md';
const PROF = 'C:/Projects/jouranl-title/.claude/skills/ep-title-advisor/references/journal-profiles.md';
const items = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];
const RET = { type:'object', required:['hid','done'], properties:{ hid:{type:'integer'}, done:{type:'boolean'} } };
function genA(hid){return `Read three files: the title skill ${SKILL}, its journal profiles ${PROF}, and the study brief ${D}/loop_r2/brief_${hid}.json (which names the target journal). Do NOT read any other file. Using the skill's guidance for that journal, write the SINGLE best manuscript title from the brief's facts. Write ONLY the title text (one line, no quotes) to ${D}/loop_t1/A_${hid}.txt. Return {hid:${hid},done:true}.`;}
function genB(hid){return `Read the study brief ${D}/loop_r2/brief_${hid}.json (which names the target journal). Do NOT read any other file. Write the SINGLE best manuscript title for that journal from the brief's facts, using your own judgment (no style guide). Write ONLY the title text (one line, no quotes) to ${D}/loop_t1/B_${hid}.txt. Return {hid:${hid},done:true}.`;}
phase('Generate');
const r = await parallel(items.flatMap(hid=>[
  ()=>agent(genA(hid),{label:`A(skill):${hid}`,phase:'Generate',schema:RET}),
  ()=>agent(genB(hid),{label:`B(noskill):${hid}`,phase:'Generate',schema:RET}),
]));
log(`title gen done: ${r.filter(Boolean).length}/${items.length*2}`);
return { ok:r.filter(Boolean).length };
