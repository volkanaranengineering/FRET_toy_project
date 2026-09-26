from copy import deepcopy
from pathlib import Path
import json
from model import evaluate
from experiments import savecsv
root=Path(__file__).resolve().parent
records=json.loads((root/'http_records.json').read_text(encoding='utf-8'))
good=next(x['record'] for x in records if x['mode']=='correct')
bad=next(x['record'] for x in records if x['mode']=='body_bug')
stages=[]
def add(label,r):stages.append(dict(level=len(stages)+1,event=label,**evaluate(r)))
r=deepcopy(bad);r['evidence']=[];r['alternatives'][1]['mass']=1
add('İki tasarım, test yok',r)
r['alternatives'][1]['mass']=0;add('Tek tasarım seçildi',r)
r=deepcopy(bad);add('Test başarısız',r)
r['implementation']='correct';add('Kod değişti, kanıt eski',r)
r=deepcopy(good);add('Yeni test başarılı',r)
r['alternatives']=[dict(id='name1',**{'class':'same-code'},mass=1),dict(id='name2',**{'class':'same-code'},mass=1)]
add('Aynı koda iki etiket',r)
savecsv('trajectory.csv',stages)
print([(s['level'],s['label_entropy'],s['class_entropy'],s['acceptance']) for s in stages])
