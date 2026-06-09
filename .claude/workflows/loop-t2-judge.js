export const meta={name:'loop-t2-judge',description:'Blind title judging round-2 (Claude)',phases:[{title:'Judge'}]}
const D='C:/Projects/jouranl-title/data/loop_t2';
const tids=['1_AvB','2_AvB','3_AvB','4_AvB','5_AvB','6_AvB','7_AvB','8_AvB','9_AvB','10_AvB','11_AvB','12_AvB','13_AvB','14_AvB','15_AvB'];
const RET={type:'object',required:['tid','done'],properties:{tid:{type:'string'},done:{type:'boolean'}}};
function p(tid){return `Read ${D}/judge_tasks/${tid}.txt — a self-contained instruction comparing two titles (X,Y) on a rubric. Follow it as an impartial expert editor. Write STRICT JSON to ${D}/judge_out/${tid}.json: {"x_scores":{"journal_fit":<1-5>,"informativeness":<1-5>,"clarity":<1-5>,"appeal":<1-5>},"y_scores":{...},"winner":"X"|"Y"|"tie","rationale":"...","loser_weakness":"..."}. Valid JSON only. Return {tid:"${tid}",done:true}.`;}
phase('Judge');
const r=await parallel(tids.map(t=>()=>agent(p(t),{label:`j:${t}`,phase:'Judge',model:'sonnet',schema:RET})));
log(`judged ${r.filter(Boolean).length}/15`); return {ok:r.filter(Boolean).length};
