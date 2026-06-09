export const meta = { name:'loop-t1-judge', description:'Blind title judging (Claude)', phases:[{title:'Judge'}] }
const D='C:/Projects/jouranl-title/data/loop_t1';
const tids=['1_AvB','1_AvO','2_AvB','2_AvO','3_AvB','3_AvO','4_AvB','4_AvO','5_AvB','5_AvO','6_AvB','6_AvO','7_AvB','7_AvO','8_AvB','8_AvO','9_AvB','9_AvO','10_AvB','10_AvO','11_AvB','11_AvO','12_AvB','12_AvO','13_AvB','13_AvO','14_AvB','14_AvO','15_AvB','15_AvO'];
const RET={type:'object',required:['tid','done'],properties:{tid:{type:'string'},done:{type:'boolean'}}};
function p(tid){return `Read ${D}/judge_tasks/${tid}.txt — a self-contained instruction comparing two manuscript titles (X and Y) on a rubric. Follow it as an impartial expert editor. Do NOT read other files. Write STRICT JSON to ${D}/judge_out/${tid}.json with keys: {"x_scores":{"journal_fit":<1-5>,"informativeness":<1-5>,"clarity":<1-5>,"appeal":<1-5>},"y_scores":{...same...},"winner":"X"|"Y"|"tie","rationale":"<one sentence>","loser_weakness":"<what the weaker title lacked>"}. Integer scores; valid JSON only. Return {tid:"${tid}",done:true}.`;}
phase('Judge');
const r=await parallel(tids.map(t=>()=>agent(p(t),{label:`judge:${t}`,phase:'Judge',model:'sonnet',schema:RET})));
log(`judged ${r.filter(Boolean).length}/${tids.length}`); return {ok:r.filter(Boolean).length};
