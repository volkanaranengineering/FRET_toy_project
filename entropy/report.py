"""Offline HTML presentation. No external assets, telemetry or server required."""
import json


def render(results, requirements, nested=False):
    payload = json.dumps({'analyses': results, 'requirements': requirements}).replace('<', '\\u003c')
    prefix = '../' if nested else ''
    return TEMPLATE.replace('__DATA__', payload).replace('__PREFIX__', prefix).replace('__IMPORT__', 'fret-project.json' if nested else 'inputs/fret-project.json')


TEMPLATE = r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>FRET setup — three entropy experiments</title>
<style>
:root{font-family:system-ui,sans-serif;color:#142e46;background:#edf2f7}body{max-width:1160px;margin:auto;padding:24px}h1{font-size:2rem}h2{margin-top:0}nav{display:flex;gap:18px;flex-wrap:wrap;margin:20px 0}a{color:#07598a}article,.context{background:white;border:1px solid #c9d5e0;border-radius:12px;padding:22px;margin:20px 0}.note{background:#fff4d6;padding:14px;border-left:5px solid #a97805}.cards{display:flex;gap:12px;flex-wrap:wrap}.metric{background:#edf5fc;padding:14px;border-radius:8px;min-width:160px}.metric b{display:block;font-size:1.7rem}table{border-collapse:collapse;width:100%;margin:12px 0}th,td{text-align:left;padding:8px;border-bottom:1px solid #dce3e9}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f6f9;padding:12px}button,input{font:inherit;padding:8px;border:1px solid #7a93a9;border-radius:5px;margin:4px}button{background:#e7f1fb;cursor:pointer}button:disabled{opacity:.45;cursor:default}input{width:85px}code{overflow-wrap:anywhere}.status{font-weight:600;color:#145342}.trace{max-width:600px}.small{font-size:.9rem;color:#456}output{display:block;margin:12px 0;font-weight:600}
</style>
<h1>FRET setup: three entropy experiments</h1>
<p>The two original request–response requirements, analyzed separately using NASA FRET compiler output.</p>
<nav><a href="__PREFIX__01_semantic_interpretation/index.html">1 · Meaning</a><a href="__PREFIX__02_behavioral_freedom/index.html">2 · Behavior</a><a href="__PREFIX__03_active_clarification/index.html">3 · Clarification</a><a href="__PREFIX__README.md">Methods & reproduction</a><a href="__IMPORT__">FRET import JSON</a></nav>
<p class="note">Research companion to FRET, not a native FRET panel. Alternative meanings and priors are illustrative experimental inputs. Original FRETish requirements are already precise. No stakeholder responses or acceptance evidence have been invented.</p>
<div id="context" class="context"></div><main id="main"></main>
<script id="data" type="application/json">__DATA__</script>
<script>
'use strict';
const data=JSON.parse(document.getElementById('data').textContent), main=document.getElementById('main');
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const H=p=>-p.reduce((s,v)=>s+(v>0?v*Math.log2(v):0),0);
const fmt=x=>x===null?'undefined':x.toFixed(6);
const context=data.analyses[0].context;
document.getElementById('context').innerHTML=`<b>Exact bounded analysis:</b> ${context.horizon} ticks · ${context.trace_count.toLocaleString()} Boolean traces · uniform distribution · no environment restrictions.<br><span class="small">Weak unfinished deadlines follow FRET's finite formula. Tick duration is unspecified. Equivalence and redundancy apply only to this horizon. Acceptance: not assessed.</span>`;
const requirements=Object.fromEntries(data.requirements.map(r=>[r.reqid,r]));
for(const analysis of data.analyses){
 const header=document.createElement('h2');header.textContent=analysis.idea+'. '+analysis.title;main.append(header);
 for(const row of analysis.results){
  const article=document.createElement('article');main.append(article);
  const original=requirements[row.reqid+'-original'];
  article.innerHTML=`<h3>${esc(row.reqid)}</h3><p>${esc(original.fulltext)}</p><details><summary>Actual FRET output</summary><p>${original.semantics.description}</p><pre>${esc(original.semantics.ftExpanded)}</pre></details>`;
  const body=document.createElement('div');article.append(body);
  if(analysis.idea===1){
   body.innerHTML=`<div class="cards"><div class="metric">Original only<b>0 bits</b></div><div class="metric">Experimental meaning entropy<b>${fmt(row.experimental_meaning_entropy_bits)}</b></div><div class="metric">Ungrouped candidate entropy<b>${fmt(row.experimental_candidate_entropy_bits)}</b></div></div><p>${esc(row.prior_source)}</p><p>Change class weights to explore assumptions. These edits do not modify FRET requirements or the recorded results.</p>`;
   const inputs=[];
   row.classes.forEach(c=>{const label=document.createElement('label');label.style.display='block';label.append(c.members.map(x=>x.replace(row.reqid+'-','')).join(' / ')+' ');const input=document.createElement('input');input.type='number';input.min='0';input.step='0.05';input.value=c.probability;label.append(input);body.append(label);inputs.push(input)});
   const out=document.createElement('output');body.append(out);
   const update=()=>{const w=inputs.map(i=>Number(i.value)),s=w.reduce((a,b)=>a+b,0);out.textContent=w.some((x,i)=>!Number.isFinite(x)||x<0||inputs[i].value==='')||s<=0?'Enter nonnegative weights with positive total.':`Exploratory normalized entropy: ${fmt(H(w.map(x=>x/s)))} bits. Candidate completeness remains unassessed.`};
   inputs.forEach(i=>i.addEventListener('input',update));update();
  }else if(analysis.idea===2){
   body.innerHTML=`<div class="cards"><div class="metric">Admissible traces<b>${row.admissible_traces}</b></div><div class="metric">Behavioral entropy<b>${fmt(row.entropy_bits)}</b></div><div class="metric">Information vs unconstrained<b>${fmt(row.information_bits)}</b></div></div><p>Adding this requirement when the other already holds: ${row.marginal_given_other.before} → ${row.marginal_given_other.after} traces; ${fmt(row.marginal_given_other.information_bits)} bits of additional constraint information.</p><p class="small">${esc(analysis.interpretation)}</p>`;
  }else{
   let probabilities=row.classes.map(c=>c.probability), history=[], pending=null, reopened=false;
   const fixed=document.createElement('p');fixed.textContent='Question model: reliable yes/no answers, equal cost. Neither reopens the candidate set; unsure preserves the distribution. All choices stay in this page until exported.';body.append(fixed);
   const classTable=document.createElement('p');classTable.className='small';classTable.textContent=row.classes.map((c,i)=>`Class ${i+1}: ${c.members.join(', ')}`).join(' | ');body.append(classTable);
   const panel=document.createElement('div');body.append(panel);
   const branch=(q,answer)=>{const w=probabilities.map((p,i)=>q.accepts_by_class[i]===answer?p:0),s=w.reduce((a,b)=>a+b,0);return {mass:s,p:s?w.map(x=>x/s):null}};
   const refresh=()=>{
    const ranked=row.questions.map(q=>{const y=branch(q,true),n=branch(q,false);return {q,gain:H(probabilities)-(y.mass?y.mass*H(y.p):0)-(n.mass?n.mass*H(n.p):0)}}).sort((a,b)=>b.gain-a.gain);
    pending=ranked.length&&ranked[0].gain>1e-10&&!reopened?ranked[0]:null;
    panel.innerHTML=`<p class="status">Current interpretation entropy: ${fmt(H(probabilities))} bits · Answers recorded: ${history.length}</p><p>Class probabilities: ${probabilities.map(fmt).join(', ')}</p>`;
    if(pending){panel.innerHTML+=`<p><b>${esc(row.question)}</b></p><p>Expected information gain: ${fmt(pending.gain)} bits</p><table class="trace"><tr><th>Tick</th><th>Request</th><th>Response</th></tr>${pending.q.trace.map(t=>`<tr><td>${t.tick}</td><td>${Number(t.request)}</td><td>${Number(t.response)}</td></tr>`).join('')}</table>`}
    else panel.innerHTML+=`<p>${reopened?'Candidate set must be revised before continuing.':'No informative question remains within the current candidate set and horizon.'} Acceptance remains unassessed.</p>`;
    for(const [label,answer] of [['Yes',true],['No',false],['Neither interpretation','neither'],['Unsure','unsure']]){const b=document.createElement('button');b.textContent=label;b.disabled=!pending;b.onclick=()=>{const q=pending.q;const before=[...probabilities];if(typeof answer==='boolean'){const next=branch(q,answer);if(!next.mass)return;probabilities=next.p}else if(answer==='neither')reopened=true;history.push({answer,trace:q.trace,before,after:[...probabilities],source:'user interaction; identity not authenticated'});refresh()};panel.append(b)}
   };
   refresh();
   const reset=document.createElement('button');reset.textContent='Reset';reset.onclick=()=>{probabilities=row.classes.map(c=>c.probability);history=[];reopened=false;refresh()};body.append(reset);
   const save=document.createElement('button');save.textContent='Export answer ledger';save.onclick=()=>{const blob=new Blob([JSON.stringify({reqid:row.reqid,context,classes:row.classes,history,probabilities,candidate_set_reopened:reopened,acceptance:'not assessed'},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=row.reqid+'-clarification.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};body.append(save);
  }
 }
}
</script></html>'''
