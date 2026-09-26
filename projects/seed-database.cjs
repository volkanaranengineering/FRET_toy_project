/* Dedicated demo database only. Does not modify NASA-FRET/data. */
const fs=require('fs'),path=require('path');
const base=path.resolve(process.env.FRET_HOME || path.join(__dirname,'../vendor/fret/fret-electron'));
const PouchDB=require(path.join(base,'app/node_modules/pouchdb'));
const db=new PouchDB(path.join(__dirname,'desktop-data/fret-db'));
(async()=>{
 const {requirements}=JSON.parse(fs.readFileSync(path.join(__dirname,'all-projects.json'),'utf8'));
 const existing=await db.allDocs();
 if(existing.rows.length)throw Error('Dedicated demo database already exists. Import updated JSON through FRET rather than overwriting it.');
 const docs=requirements.map(r=>({...r,_id:r.project+'::'+r.reqid}));
 docs.push({_id:'FRET_PROJECTS',names:[...new Set(requirements.map(r=>r.project))]});
 const result=await db.bulkDocs(docs);if(result.some(r=>r.error))throw Error(JSON.stringify(result));
 const count=(await db.allDocs()).rows.length-1;
 if(count!==requirements.length)throw Error('Database count mismatch');
 await db.close();console.log('Dedicated FRET database populated: '+count+' requirements');
})().catch(e=>{console.error(e);process.exitCode=1});
