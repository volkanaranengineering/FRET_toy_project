"""Audit persisted raw observations against the published aggregates."""
from pathlib import Path
from collections import Counter
import json,csv,base64,hashlib
ROOT=Path(__file__).resolve().parent
def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def csvload(name):
    with (ROOT/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
raw=load('http_raw.json');assert len(raw)==40
observed={}
for item in raw:
    data=base64.b64decode(item['response_base64'],validate=True)
    assert hashlib.sha256(data).hexdigest()==item['sha256']
    headers,body=data.split(b'\r\n\r\n',1)
    assert headers.split(b'\r\n')[0]==b'HTTP/1.1 200 OK'
    fields=dict(line.decode('ascii').split(': ',1) for line in headers.split(b'\r\n')[1:])
    key=(item['mode'],item['path'],item['method']);assert key not in observed
    observed[key]=(fields,body)
pairs=csvload('http_pairs.csv');assert len(pairs)==20
for row in pairs:
    mode,path=row['mode'],row['path']
    _,getbody=observed[(mode,path,'GET')];headfields,headbody=observed[(mode,path,'HEAD')]
    n=int(path[2:]);assert getbody==b'x'*n and int(row['get_bytes'])==n
    assert int(row['head_bytes'])==len(headbody)
    length=headfields.get('Content-Length','absent');assert row['head_length']==length
    assert (row['C1']=='True')==(len(headbody)==0)
    assert (row['C2']=='True')==(length=='absent' or int(length)==n)
for case in load('http_records.json'):
    rs=[x for x in pairs if x['mode']==case['mode']];assert len(rs)==5
    for j,ev in enumerate(case['record']['evidence'],start=1):
        assert (ev['result']=='pass')==all(x[f'C{j}']=='True' for x in rs)
    expected='accepted' if all(x['C1']=='True' and x['C2']=='True' for x in rs) else 'failed'
    assert case['status']['acceptance']==expected
    assert case['status']['class_entropy']==0
summary=load('summary.json');finite=csvload('finite_cases.csv')
assert len(finite)==summary['finite_cases']==2480
assert Counter(x['acceptance'] for x in finite)==summary['status_counts']
bound=csvload('boundary_cases.csv');assert len(bound)==52
assert sum(x['old_zero_condition']=='True' for x in bound)==summary['old_false_closures']==7
assert all(x['closed']=='False' for x in bound)
assert len(csvload('invalid_cases.csv'))==summary['invalid_cases']==41
matlab=load('matlab_validation.json');assert matlab['fixtures']==2573 and matlab['status']=='passed'
assert matlab['max_entropy_difference']<1e-12
flow=csvload('trajectory.csv');assert [x['acceptance'] for x in flow]==['pending','pending','failed','pending','accepted','accepted']
report=dict(raw_responses=40,http_pairs=20,finite_records=len(finite),matlab_records=2573,status='passed')
(ROOT/'bundle_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report)
