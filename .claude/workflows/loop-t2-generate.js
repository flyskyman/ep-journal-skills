export const meta={name:'loop-t2-generate',description:'Title round-2: regenerate A with improved (info-density) skill',phases:[{title:'Generate'}]}
const D='C:/Projects/jouranl-title/data';
const SKILL='C:/Projects/jouranl-title/.claude/skills/ep-title-advisor/SKILL.md';
const PROF='C:/Projects/jouranl-title/.claude/skills/ep-title-advisor/references/journal-profiles.md';
const items=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];
const RET={type:'object',required:['hid','done'],properties:{hid:{type:'integer'},done:{type:'boolean'}}};
function genA(hid){return `Read three files: the title skill ${SKILL}, its journal profiles ${PROF}, and the study brief ${D}/loop_r2/brief_${hid}.json (names the target journal). Do NOT read other files. Follow the skill — especially Step 2a (pack in the specific finding/outcomes, both comparison arms, named device/study, cohort size/design) before fitting style. Write the SINGLE best, most informative title that still fits the journal to ${D}/loop_t2/A_${hid}.txt (one line, no quotes). Return {hid:${hid},done:true}.`;}
phase('Generate');
const r=await parallel(items.map(h=>()=>agent(genA(h),{label:`A2:${h}`,phase:'Generate',schema:RET})));
log(`t2 A regenerated: ${r.filter(Boolean).length}/15`); return {ok:r.filter(Boolean).length};
