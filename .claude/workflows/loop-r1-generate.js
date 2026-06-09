export const meta = {
  name: 'loop-r1-generate',
  description: 'Iteration loop round 1: extract brief from held-out abstracts, then generate skill vs no-skill abstracts (Claude)',
  phases: [
    { title: 'Brief', detail: 'extract a faithful fact-only brief from each original abstract' },
    { title: 'Generate', detail: 'arm A (with skill) and arm B (no skill) from the brief only' },
  ],
}

const DIR = 'C:/Projects/jouranl-title/data';
const SKILL = 'C:/Projects/jouranl-title/.claude/skills/ep-abstract-advisor/SKILL.md';
// inlined to avoid args-passing ambiguity; brief agents read the abstract from heldout.json by hid
const items = [
  {hid:1,journal:'HR'},{hid:2,journal:'HR'},{hid:3,journal:'HR'},
  {hid:4,journal:'Europace'},{hid:5,journal:'Europace'},{hid:6,journal:'Europace'},
  {hid:7,journal:'JACC'},{hid:8,journal:'JACC'},{hid:9,journal:'JACC'},
  {hid:10,journal:'PACE'},{hid:11,journal:'PACE'},{hid:12,journal:'PACE'},
  {hid:13,journal:'JICE'},{hid:14,journal:'JICE'},{hid:15,journal:'JICE'},
];

const BRIEF_SCHEMA = {
  type: 'object', required: ['hid', 'done'],
  properties: { hid: { type: 'integer' }, done: { type: 'boolean' } },
};

function briefPrompt(it) {
  return `You extract a faithful, COMPLETE study brief from a published abstract, for later regeneration. Output FACTS ONLY — never reuse the abstract's sentences or phrasing.

Read ${DIR}/heldout.json and use ONLY the object whose hid == ${it.hid} (target journal: ${it.journal}); ignore all other entries. Take its "abstract" field as the source.

Extract every fact a writer would need: (1) the knowledge gap/why it matters, (2) study design + setting, (3) population/sample/n, (4) intervention/comparison, (5) ALL key results WITH their exact numbers (effect sizes, %, p-values, CIs — copy numbers faithfully), (6) the main takeaway. Be complete; omit nothing quantitative. Do NOT copy the abstract's wording — use terse bullet facts.

Write the brief as plain text to ${DIR}/loop_r1/brief_${it.hid}.json in this exact JSON shape:
{"hid": ${it.hid}, "journal": "${it.journal}", "brief": "<the fact bullets as one string>"}
Then return {hid: ${it.hid}, done: true}.`;
}

function genAPrompt(it) {
  return `Read two files:
1. The abstract-writing skill at ${SKILL}
2. The study brief at ${DIR}/loop_r1/brief_${it.hid}.json
Do NOT read any other file. You have ONLY the brief — you have not seen any original abstract.

Using the skill's guidance, write the best possible abstract for the target journal "${it.journal}" from the brief's facts. Write ONLY the finished abstract (with section labels if the skill says that journal uses them) to ${DIR}/loop_r1/A_${it.hid}.txt.
Return {hid: ${it.hid}, done: true}.`;
}

function genBPrompt(it) {
  return `Read the study brief at ${DIR}/loop_r1/brief_${it.hid}.json. Do NOT read any other file.
Write the best possible abstract for the target journal "${it.journal}" from the brief's facts, using your own judgment (no special style guide). Write ONLY the finished abstract to ${DIR}/loop_r1/B_${it.hid}.txt.
Return {hid: ${it.hid}, done: true}.`;
}

const results = await pipeline(
  items,
  (it) => agent(briefPrompt(it), { label: `brief:${it.hid}`, phase: 'Brief', schema: BRIEF_SCHEMA }),
  (_b, it) => parallel([
    () => agent(genAPrompt(it), { label: `A(skill):${it.hid}`, phase: 'Generate', schema: BRIEF_SCHEMA }),
    () => agent(genBPrompt(it), { label: `B(noskill):${it.hid}`, phase: 'Generate', schema: BRIEF_SCHEMA }),
  ]),
);
const ok = results.filter(Boolean).length;
log(`round-1 generation done for ${ok}/${items.length} items (brief + A + B each)`);
return { items: items.length, ok };
