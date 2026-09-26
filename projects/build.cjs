/* Reproducible adapter to the installed, unmodified NASA FRET compiler. */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = __dirname;
const base = path.resolve(process.env.FRET_HOME || path.join(root, '../vendor/fret/fret-electron'));
process.chdir(base);
require(path.join(base, 'node_modules/@babel/register'))({cwd: base});
const {compile} = require(path.join(base, 'app/parser/FretSemantics.js'));
const projects = [];
function project(id, title, source, assumptions, variables) {
  const p = {id, title, source, assumptions, variables, requirements: []}; projects.push(p); return p;
}
function req(p, id, text, meaning, predicate, timing='immediately', trigger='snapshot', parent='') {
  p.requirements.push({reqid:id, fulltext:text, rationale:meaning, project:p.id, parent_reqid:parent,
    status:'', check:{predicate,timing,trigger}});
}
const door = project('01_Door_Mechanism','Door mechanism — clarified toy baseline',
  ['Boran chat, 26–27 August 2026: hinged room door; stakeholder/system/subsystem requirements; no sharp edges.',
   'report_build/build_project_report.py: target package 1011; ages 6–12, P0, 10 N, full opening/closing.'],
  ['The original nine-requirement attachment is absent. These are traceable decompositions of the available text, not a recovered verbatim list.',
   '10 N, ages 6–12, P0 and 90 degrees come from the illustrative project report, not a child-safety standard.',
   'P0 geometry, operating speed, environment and edge criteria remain unspecified. p0_active/test_active are test-harness signals, not evidence that a real test took place.',
   'Open and close requests are separate phases; no maximum duration was supplied. Eventually therefore has no invented deadline.',
   'sharp_edges_present needs an agreed inspection method. No unprovided edge radius is invented.'],
  {test_active:'bool: active, correctly configured P0 trial', p0_active:'bool: P0 fixture in use', force_n:'nonnegative real: measured instantaneous operating force, N', hands_used:'integer: number of hands used', scope_approved:'bool: approved scope record', minimum_age:'integer: lower age in approved scope', maximum_age:'integer: upper age in approved scope', fixture_approved:'bool: fixture/procedure approval', open_requested:'bool: rising edge begins an opening operation', close_requested:'bool: rising edge begins closing', latch_released:'bool: latch disengaged', opened_90:'bool: observed opening from 0 to 90 degrees', closed_and_latched:'bool: observed closed and engaged', inspection_active:'bool: agreed edge inspection in progress', sharp_edges_present:'bool: inspection result; criterion unresolved'});
req(door,'DOOR-01','whenever scope_approved the DoorSystem shall immediately satisfy (minimum_age = 6 & maximum_age = 12)','Approved user scope follows target A=1.', '(minimum_age === 6 && maximum_age === 12)','immediately','scope_approved');
req(door,'DOOR-02','whenever test_active the DoorSystem shall immediately satisfy (p0_active & fixture_approved)','P0 and its approved procedure are required during the trial.', 'p0_active && fixture_approved','immediately','test_active');
req(door,'DOOR-03','whenever test_active the DoorSystem shall immediately satisfy (force_n <= 10)','The 10 N peak limit is expressed at every sampled trial point; sampling must capture the true peak.', 'force_n <= 10','immediately','test_active');
req(door,'DOOR-04','whenever test_active the DoorSystem shall immediately satisfy (hands_used = 1)','One-handed operation at every active trial sample.', 'hands_used === 1','immediately','test_active');
req(door,'DOOR-05','when open_requested the DoorSystem shall eventually satisfy latch_released','Opening requires eventual latch release. Added decomposition of the stated full function.', 'latch_released','eventually','open_requested');
req(door,'DOOR-06','when open_requested the DoorSystem shall eventually satisfy opened_90','Opening reaches the report’s 90-degree target.', 'opened_90','eventually','open_requested');
req(door,'DOOR-07','when close_requested the DoorSystem shall eventually satisfy closed_and_latched','Closing completes and latch engages; no deadline was supplied.', 'closed_and_latched','eventually','close_requested');
req(door,'DOOR-08','whenever inspection_active the DoorSystem shall immediately satisfy !sharp_edges_present','Preserves the no-sharp-edges concern, with inspection criterion explicitly unresolved.', '!sharp_edges_present','immediately','inspection_active');

const truss = project('02_Steel_Truss','Steel truss — feasibility and bounded optimality contract',
 ['Boran chat, 29 August 2026 11:24 and 11:32: 2 m wall offset; solid circular fixed-section steel bars; 1 m/sqrt(2) m lengths; 1000 kgf; displacement below 2 cm; yielding/buckling; minimum mass.'],
 ['The original grid image and structural report are absent. Grid nodes, diameter, steel properties, support/joint model, safety factors and tolerances remain open.',
  'Displacement is interpreted as total displacement magnitude. Vertical-only is retained as a separate alternative requirement, not conjoined with the selected interpretation.',
  'FRET does not solve statics or optimization. Geometry/stability/utilizations are inputs from a separate solver. No structural design is claimed verified.',
  'Yield/buckling utilization <=1 means the demand/capacity ratio with the chosen safety factor already included. Capacity model and factor must be agreed.',
  'enumerated_min_mass_kg refers only to a declared finite, exhaustively checked candidate set. It is not a global continuous-design optimum.'],
 {assessment_active:'bool: evaluate one declared candidate/load case', load_kgf:'real: downward vertical load magnitude, kgf', offset_m:'real: loaded node distance from wall, m', steel_only:'bool: all bars are specified steel', solid_circular:'bool: all bars solid circular', fixed_section:'bool: common specified cross-section', allowed_lengths:'bool: every bar has length 1 m or sqrt(2) m within agreed tolerance', available_grid_only:'bool: endpoints belong to the provided grid', connected_to_wall:'bool: loaded node connected to wall supports', stable:'bool: solver establishes a stable supported structure', joints_rigid_enough:'bool: joint deformation neglected under source assumption', displacement_m:'nonnegative real: loaded-node displacement magnitude, m', vertical_displacement_m:'nonnegative real: absolute vertical displacement, m', yield_utilization:'nonnegative real: maximum yielding demand/capacity across bars', buckling_utilization:'nonnegative real: maximum compressive demand/buckling capacity across bars', selection_complete:'bool: candidate selection complete', feasible:'bool: conjunction of all feasibility checks for this load case', enumeration_complete:'bool: declared finite set exhaustively checked', mass_kg:'nonnegative real: selected candidate mass', enumerated_min_mass_kg:'nonnegative real: independently computed minimum feasible mass in the declared set'});
const trows=[
 ['01','(load_kgf = 1000 & offset_m = 2)','load_kgf === 1000 && offset_m === 2','The specified load case and wall offset.'],
 ['02','(steel_only & solid_circular & fixed_section)','steel_only && solid_circular && fixed_section','Source material and cross-section restrictions.'],
 ['03','(allowed_lengths & available_grid_only)','allowed_lengths && available_grid_only','Allowed bar lengths and grid membership; upstream geometry checks.'],
 ['04','(connected_to_wall & stable & joints_rigid_enough)','connected_to_wall && stable && joints_rigid_enough','Connection, stability and the source joint idealization.'],
 ['05','(displacement_m < 0.02)','displacement_m < 0.02','Strictly below 2 cm; total magnitude interpretation.'],
 ['06','(yield_utilization <= 1)','yield_utilization <= 1','Every member satisfies the chosen yield criterion.'],
 ['07','(buckling_utilization <= 1)','buckling_utilization <= 1','Every compressed member satisfies the chosen buckling criterion.']];
for (const [id,exp,pred,note] of trows) req(truss,'TRUSS-'+id,`whenever assessment_active the TrussSystem shall immediately satisfy ${exp}`,note,pred,'immediately','assessment_active');
req(truss,'TRUSS-08','whenever selection_complete the TrussSystem shall immediately satisfy (feasible & enumeration_complete & mass_kg = enumerated_min_mass_kg)','Bounded optimality certificate from an external enumerator; no global-optimality proof is produced by FRET.','feasible && enumeration_complete && mass_kg === enumerated_min_mass_kg','immediately','selection_complete');
const trussAlt = project('03_Truss_Vertical_Alternative','Truss — vertical-only displacement interpretation',truss.source,
 ['This is the unresolved alternative meaning of displacement, not an additional constraint on project 02.', 'Only the differing requirement is included; all other constraints are shared with project 02.'],truss.variables);
req(trussAlt,'TRUSS-V-05','whenever assessment_active the TrussSystem shall immediately satisfy (vertical_displacement_m < 0.02)','Alternative interpretation retained for stakeholder clarification.','vertical_displacement_m < 0.02','immediately','assessment_active');

const response = project('04_Request_Response','Request/response — edge versus sustained trigger',
 ['Task Gereksinim anlama görselleştirmesi, 24 September 2026; NASA-FRET/prepare-example.cjs and tutorial/verified-semantics.json.'],
 ['The original phrase “short time” is ambiguous. The three-tick bound is the existing tutorial’s example choice, not an elicited service-level agreement.',
  'request/response meaning (send vs receive; acknowledgement vs completed result) and load conditions remain open.',
  'when and whenever are alternative interpretations shown side by side. Each request is a Boolean event; concurrent request identity/matching is outside this toy abstraction.',
  'FRET counts discrete timepoints and does not convert units. The finite semantics permits a trace to end before the deadline without a response. Independent examples report that situation as INCOMPLETE.'],
 {request:'bool: request signal',response:'bool: response signal',tick:'integer: abstract discrete timepoint; no physical duration assigned'});
req(response,'RESP-EDGE','when request the ResponseSystem shall within 3 ticks satisfy response','Existing tutorial: first true point and false-to-true edges trigger obligations.','response','within3-edge','request');
req(response,'RESP-LEVEL','whenever request the ResponseSystem shall within 3 ticks satisfy response','Existing tutorial: every true request sample triggers an obligation.','response','within3-level','request');

const http=project('05_HTTP_HEAD','HTTP HEAD — no body and optional correct Content-Length',
 ['output/pdf/research_revision_v3/artifact/http_case.py and paper.tex §119–121.', 'RFC 9110 sections 9.3.2 and 8.6: https://www.rfc-editor.org/rfc/rfc9110.html'],
 ['Snapshot is taken after a complete successful HTTP/1.1 response. Same stable resource and representation as paired GET; no compression, transfer coding, proxies or concurrent changes.',
  'Content-Length may be absent. A raw-socket recorder is needed to detect an illegal HEAD body.',
  'GET body correctness is a test-fixture control, not a newly attributed RFC requirement.'],
 {head_complete:'bool: completed HEAD observation',head_bytes:'integer >=0: raw HEAD content octets',length_present:'bool: Content-Length present',head_length:'integer >=0 when present: parsed field value',get_bytes:'integer >=0: paired GET content length'});
req(http,'HTTP-01','whenever head_complete the HttpServer shall immediately satisfy (head_bytes = 0)','HEAD response has no content.','head_bytes === 0','immediately','head_complete');
req(http,'HTTP-02','whenever (head_complete & length_present) the HttpServer shall immediately satisfy (head_length = get_bytes)','If present, Content-Length matches the corresponding GET.','head_length === get_bytes','immediately','head_complete && length_present');

const methodNames=['Sequential decision gates','Parallel work packages','Constraint propagation','Evidence updates and final commitment','Prototype candidate elimination'];
const counts=[[16,16,8,4,2,1],[16,16,4,4,2,1],[16,16,8,4,2,1],[16,16,16,16,16,1],[16,12,8,4,2,1]];
for(let m=1;m<=5;m++) {
 const p=project(`${String(m+5).padStart(2,'0')}_Door_Method_${m}`,`Door workflow ${m} — ${methodNames[m-1]}`,
  ['output/pdf/conference_revision_v2/artifact/ledger_schedules.py (existing six-level schedule).',...door.source],
  ['The physical door contract is project 01. These are workflow-observation requirements, not five different physical products.',
   'Six levels: steps 0, 11, 22, 33, 44, 55. Ten exploration steps occur between gates.',
   'Candidate counts and target package 1011 come from the existing stipulated schedule; prototype ranks and evidence likelihoods are synthetic.',
   'Added formalization: closure requires all four current matching acceptance records. A unique candidate and zero entropy alone never imply acceptance.'],
  {gate_observed:'bool: a level/gate record is available',level:'integer 1..6',step:'integer: model step',candidate_count:'integer: strictly positive support count',selected_package:'integer: ABCD binary interpreted as integer; target 1011 = 11',accepted:'bool: workflow claims implementation accepted',open_topics:'integer: unresolved decisions',current_evidence_count:'integer: distinct passing criteria matching requirement and implementation versions',evidence_valid:'bool: record identities, versions, sources and results are valid',test_failed:'bool: any current criterion failed'});
 for(let g=0;g<6;g++) req(p,`M${m}-L${g+1}`,`whenever (gate_observed & level = ${g+1}) the DecisionLedger shall immediately satisfy (step = ${g*11} & candidate_count = ${counts[m-1][g]})`,`Existing method ${m}, level ${g+1} schedule snapshot.`,`step === ${g*11} && candidate_count === ${counts[m-1][g]}`,'immediately',`gate_observed && level === ${g+1}`);
 req(p,`M${m}-FINAL`,'whenever (gate_observed & level = 6) the DecisionLedger shall immediately satisfy (selected_package = 11 & open_topics = 0)','Final design commitment is package 1011, without claiming acceptance.','selected_package === 11 && open_topics === 0','immediately','gate_observed && level === 6');
 req(p,`M${m}-ACCEPT`,'whenever accepted the DecisionLedger shall immediately satisfy (current_evidence_count = 4 & evidence_valid & !test_failed)','Added acceptance guard, consistent with later paper revisions. Four distinct, current, matching passing records are required.','current_evidence_count === 4 && evidence_valid && !test_failed','immediately','accepted');
}

let compiled=0;
for(const p of projects){
 const dir=path.join(root,p.id);fs.mkdirSync(dir,{recursive:true});
 for(const r of p.requirements){
  const result=compile(r.fulltext);
  if(result.parseErrors || !result.collectedSemantics?.ftExpanded) throw new Error(`${r.reqid}: ${JSON.stringify(result)}`);
  r.semantics=JSON.parse(JSON.stringify(result.collectedSemantics)); compiled++;
  const file=path.join(base,'docs',r.semantics.diagram);
  if(!fs.existsSync(file)) throw Error('Missing FRET diagram: '+file);
  fs.copyFileSync(file,path.join(dir,`${r.reqid}.svg`));
 }
 const exported=p.requirements.map(({check,...r})=>r);
 fs.writeFileSync(path.join(dir,'fret-project.json'),JSON.stringify({requirements:exported},null,2));
 fs.writeFileSync(path.join(dir,'fret-output.json'),JSON.stringify(p.requirements.map(r=>({id:r.reqid,input:r.fulltext,semantics:r.semantics})),null,2));
 fs.writeFileSync(path.join(dir,'README.md'),`# ${p.title}\n\n## Sources\n${p.source.map(s=>'- '+s).join('\n')}\n\n## Assumptions and unresolved inputs\n${p.assumptions.map(s=>'- '+s).join('\n')}\n\n## Signals\n${Object.entries(p.variables).map(([k,v])=>'- `'+k+'`: '+v).join('\n')}\n\n`+p.requirements.map(r=>`### ${r.reqid}\n\n${r.fulltext}\n\n${r.rationale}\n\nFRET infinite-trace formula:\n\n\`\`\`text\n${r.semantics.ftInfAUExpanded}\n\`\`\`\n`).join('\n'));
}
fs.writeFileSync(path.join(root,'catalog.json'),JSON.stringify(projects,null,2));
fs.writeFileSync(path.join(root,'all-projects.json'),JSON.stringify({requirements:projects.flatMap(p=>p.requirements.map(({check,...r})=>r))},null,2));
const summary={compiler:'NASA FRET '+require(path.join(base,'package.json')).version,compiler_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(base,'app/parser/FretSemantics.js'))).digest('hex'),projects:projects.length,requirements:compiled,parse_errors:0,formalization_only:true,projects_detail:projects.map(p=>({id:p.id,title:p.title,requirements:p.requirements.length}))};
fs.writeFileSync(path.join(root,'compilation-summary.json'),JSON.stringify(summary,null,2));
console.log(JSON.stringify(summary,null,2));
