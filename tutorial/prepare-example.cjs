const fs = require('fs');
const path = require('path');
const base = path.resolve(process.env.FRET_HOME || path.join(__dirname, '../vendor/fret/fret-electron'));
process.chdir(base);
require(path.join(base, 'node_modules', '@babel', 'register'))({cwd:base});
const {compile} = require(path.join(base, 'app', 'parser', 'FretSemantics.js'));
const output = __dirname;
fs.mkdirSync(output, {recursive:true});
const cases = [
 ['REQ-001', 'when request the ResponseSystem shall within 3 ticks satisfy response', 'Talep sinyalinin yukselen kenarindan itibaren, ayni adim dahil en gec uc adim icinde yanit sinyali dogru olmalidir.'],
 ['REQ-002', 'whenever request the ResponseSystem shall within 3 ticks satisfy response', 'Karsilastirma: request dogru oldugu her adim yeni bir yukumluluk baslatir.'],
];
const requirements = cases.map(([reqid,fulltext,rationale])=>{
 const result = compile(fulltext);
 if(!result.collectedSemantics || result.parseErrors?.length) throw Error(JSON.stringify(result));
 return {reqid,fulltext,rationale,project:'FRET_Tutorial_TR',parent_reqid:'',status:'',semantics:result.collectedSemantics};
});
fs.writeFileSync(path.join(output,'FRET_Tutorial_TR.json'),JSON.stringify({requirements},null,2));
const summary = requirements.map(r=>({id:r.reqid,text:r.fulltext,description:r.semantics.description,formula:r.semantics.ftInfAUExpanded,finite:r.semantics.ftExpanded,diagram:r.semantics.diagram}));
fs.writeFileSync(path.join(output,'verified-semantics.json'),JSON.stringify(summary,null,2));
console.log(JSON.stringify(summary,null,2));
