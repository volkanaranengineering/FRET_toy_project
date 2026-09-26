from pathlib import Path
from itertools import product
from copy import deepcopy
import csv, json, math
from model import evaluate, base_record
ROOT=Path(__file__).resolve().parent

def savecsv(name, rows):
    with (ROOT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def split_labels(r):
    s=deepcopy(r);s['alternatives']=[]
    for a in r['alternatives']:
        for suffix in ('x','y'):
            b=dict(a);b['id']+=suffix;s['alternatives'].append(b)
    return s

def main():
    fixtures=[];rows=[];inv=0;maxerr=0
    profiles=[([1,0],['A','B']),([1,1],['A','B']),([2**50-1,1],['A','B']),([1,1],['A','A'])]
    for n in (1,2,3):
      for states in product(('pass','fail','missing','stale','other_build'),repeat=n):
       for reviewed,conflict in product((False,True),repeat=2):
        for masses,classes in profiles:
            r=base_record(n);r.update(reviewed=reviewed,conflict=conflict)
            for i in range(2):r['alternatives'][i].update(mass=masses[i], **{'class':classes[i]})
            ev=[]
            for e,s in zip(r['evidence'],states):
                if s=='missing':continue
                if s=='fail':e['result']='fail'
                if s=='stale':e['version']='old'
                if s=='other_build':e['implementation']='other'
                ev.append(e)
            r['evidence']=ev
            # Oracle is the constructed condition, independent of entropy / implementation logic.
            expected='pending'
            if reviewed and not conflict and all(s in ('pass','fail') for s in states):
                expected='failed' if 'fail' in states else 'accepted'
            support=len({cl for cl,m in zip(classes,masses) if m})
            dec='inconsistent' if conflict else ('committed' if support==1 else 'open')
            out=evaluate(r);assert (out['acceptance'],out['decision'])==(expected,dec)
            split=evaluate(split_labels(r));assert split['acceptance']==out['acceptance'] and split['decision']==out['decision']
            maxerr=max(maxerr,abs(split['class_entropy']-out['class_entropy']),abs(split['label_entropy']-out['label_entropy']-1))
            inv+=1
            perm=deepcopy(r);perm['alternatives'].reverse();assert evaluate(perm)==out;inv+=1
            stale=deepcopy(r);stale['version']='v2';assert evaluate(stale)['acceptance']!='accepted';inv+=1
            rows.append(dict(id=len(rows),n=n,states='|'.join(states),reviewed=reviewed,conflict=conflict,
                             masses='|'.join(map(str,masses)),classes='|'.join(classes),**out))
            fixtures.append(dict(record=r,expected=out))
    savecsv('finite_cases.csv',rows)
    boundaries=[]
    for k in range(1,53):
        r=base_record();r['alternatives'][0]['mass']=2**k-1
        out=evaluate(r);assert out['decision']=='open' and not out['closed']
        boundaries.append(dict(k=k,mass_a=2**k-1,mass_b=1,entropy=out['class_entropy'],
                               old_zero_condition=out['class_entropy']<=1e-12,closed=out['closed']))
        fixtures.append(dict(record=r,expected=out))
    savecsv('boundary_cases.csv',boundaries)
    invalid=[]
    for field in ('requirement','version','implementation'):
      for val in ('',' ',' x'):
        r=base_record();r[field]=val;invalid.append((f'{field}:{val!r}',r))
    for field in ('id','criterion','requirement','version','implementation','source','reviewer'):
      for val in ('',' ',' x'):
        r=base_record();r['evidence'][0][field]=val;invalid.append((f'evidence.{field}:{val!r}',r))
    for name,fn in [
        ('empty_criterion',lambda r:r['criteria'].__setitem__(0,'')),
        ('duplicate_criterion',lambda r:r['criteria'].__setitem__(1,'C0')),
        ('duplicate_evidence',lambda r:r['evidence'][1].update(id='E0')),
        ('duplicate_coverage',lambda r:r['evidence'][1].update(criterion='C0')),
        ('unknown_coverage',lambda r:r['evidence'][0].update(criterion='unknown')),
        ('empty_class',lambda r:r['alternatives'][0].update({'class':''})),
        ('duplicate_candidate',lambda r:r['alternatives'][1].update(id='a')),
        ('negative_mass',lambda r:r['alternatives'][0].update(mass=-1)),
        ('fractional_mass',lambda r:r['alternatives'][0].update(mass=.5)),
        ('zero_mass',lambda r:[a.update(mass=0) for a in r['alternatives']]),
        ('over_limit',lambda r:r['alternatives'][0].update(mass=2**52))]:
        r=base_record();fn(r);invalid.append((name,r))
    invalidrows=[]
    for name,r in invalid:
        out=evaluate(r);assert out['acceptance']=='invalid'
        invalidrows.append(dict(name=name,result=out['acceptance']))
        fixtures.append(dict(record=r,expected=out))
    savecsv('invalid_cases.csv',invalidrows)
    (ROOT/'fixtures.json').write_text(json.dumps(fixtures,indent=1),encoding='utf-8')
    summary=dict(finite_cases=len(rows),metamorphic_checks=inv,refinement_max_error=maxerr,
                 boundary_cases=len(boundaries),old_false_closures=sum(x['old_zero_condition'] for x in boundaries),
                 invalid_cases=len(invalid),matlab_fixture_count=len(fixtures),
                 status_counts={s:sum(x['acceptance']==s for x in rows) for s in ('accepted','failed','pending')})
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(summary)

if __name__=='__main__':main()
