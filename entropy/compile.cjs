// Compile the setup examples and explicitly experimental variants using NASA FRET.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname, '..');
const home = path.resolve(process.env.FRET_HOME || path.join(root, 'vendor/fret/fret-electron'));
process.chdir(home);
require(path.join(home, 'node_modules/@babel/register'))({cwd: home});
const {compile} = require(path.join(home, 'app/parser/FretSemantics.js'));
const sourcePath = path.join(root, 'tutorial/FRET_Tutorial_TR.json');
const originals = JSON.parse(fs.readFileSync(sourcePath)).requirements;
const requirements = [];
const hypotheses = {};
for (const r of originals) {
  if (!/^(when|whenever) request the ResponseSystem shall within 3 ticks satisfy response$/.test(r.fulltext))
    throw Error('Unsupported setup requirement: ' + r.fulltext);
  const alternate = r.fulltext.startsWith('whenever ') ? r.fulltext.replace(/^whenever /, 'when ') : r.fulltext.replace(/^when /, 'whenever ');
  const candidates = [
    ['original', r.fulltext, 0.25],
    ['punctuation_alias', r.fulltext + '.', 0.25],
    ['tighter_deadline', r.fulltext.replace('3 ticks', '2 ticks'), 0.25],
    ['alternate_trigger', alternate, 0.25]
  ];
  hypotheses[r.reqid] = [];
  for (const [name, fulltext, prior] of candidates) {
    const result = compile(fulltext);
    if (result.parseErrors?.length || !result.collectedSemantics?.ftExpanded) throw Error(JSON.stringify(result));
    const reqid = `${r.reqid}-${name}`;
    requirements.push({reqid, fulltext, project: 'Entropy_Setup_Hypotheses', parent_reqid: '', status: '',
      rationale: 'Experimental interpretation candidate; not an ambiguity annotation or stakeholder probability supplied by NASA.',
      semantics: result.collectedSemantics});
    hypotheses[r.reqid].push({id: reqid, name, prior, trigger: fulltext.startsWith('whenever') ? 'holding' : 'rising', deadline: name === 'tighter_deadline' ? 2 : 3});
  }
}
const out = path.join(__dirname, 'inputs');
fs.mkdirSync(out, {recursive: true});
fs.writeFileSync(path.join(out, 'fret-project.json'), JSON.stringify({requirements}, null, 2) + '\n');
fs.writeFileSync(path.join(out, 'analysis.json'), JSON.stringify({schema_version: 1, originals: originals.map(({reqid, fulltext}) => ({reqid, fulltext})), hypotheses,
  prior_source: 'Illustrative analyst prior: original meaning 0.5, tighter deadline 0.25, alternate trigger 0.25. Original mass is split between two equivalent spellings.',
  candidate_completeness: 'unassessed', acceptance: 'not assessed',
  source: 'tutorial/FRET_Tutorial_TR.json', source_sha256: crypto.createHash('sha256').update(fs.readFileSync(sourcePath)).digest('hex'),
  compiler_sha256: crypto.createHash('sha256').update(fs.readFileSync(path.join(home, 'app/parser/FretSemantics.js'))).digest('hex'),
  compiled_candidates: requirements.length}, null, 2) + '\n');
console.log(`NASA FRET compiled ${requirements.length} candidates from ${originals.length} setup requirements.`);
