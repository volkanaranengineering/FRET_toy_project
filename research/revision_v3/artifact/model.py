"""Finite, explicit record contract. No claim of real-world correctness.
Masses are nonnegative integers whose total is in [1, 2**52].
Equivalence classes are supplied, not inferred from natural language.
"""
import math
from collections import defaultdict

LIMIT = 2**52

def identifier(x):
    return isinstance(x, str) and bool(x.strip()) and x == x.strip()

def entropy(masses):
    total = sum(masses)
    return math.fsum(-(m/total)*math.log2(m/total) for m in masses if m)

def evaluate(r):
    invalid = dict(decision='invalid', acceptance='invalid', closed=False,
                   label_entropy=None, class_entropy=None, support=None)
    if not isinstance(r, dict): return invalid
    if not all(identifier(r.get(k)) for k in ('requirement','version','implementation')): return invalid
    if not all(type(r.get(k)) is bool for k in ('reviewed','conflict')): return invalid
    c, e, a = r.get('criteria'), r.get('evidence'), r.get('alternatives')
    if not isinstance(c,list) or not c or not all(identifier(x) for x in c) or len(set(c)) != len(c): return invalid
    if not isinstance(e,list) or not isinstance(a,list) or not a: return invalid
    if not all(isinstance(x,dict) and identifier(x.get('id')) and identifier(x.get('class'))
               and type(x.get('mass')) is int and x['mass'] >= 0 for x in a): return invalid
    if len({x['id'] for x in a}) != len(a) or not 0 < sum(x['mass'] for x in a) <= LIMIT: return invalid
    fields = ('id','criterion','requirement','version','implementation','source','reviewer')
    if not all(isinstance(x,dict) and all(identifier(x.get(k)) for k in fields)
               and type(x.get('approved')) is bool and x.get('result') in ('pass','fail') for x in e): return invalid
    if len({x['id'] for x in e}) != len(e) or len({x['criterion'] for x in e}) != len(e): return invalid
    if any(x['criterion'] not in c for x in e): return invalid
    groups = defaultdict(int)
    for x in a: groups[x['class']] += x['mass']
    support = sum(v > 0 for v in groups.values())
    closed = support == 1 and not r['conflict']
    decision = 'inconsistent' if r['conflict'] else ('committed' if closed else 'open')
    bound = len(e) == len(c) and all(
        all(x[k] == r[k] for k in ('requirement','version','implementation')) and x['approved'] for x in e)
    acceptance = 'pending'
    if r['reviewed'] and not r['conflict'] and bound:
        acceptance = 'accepted' if all(x['result'] == 'pass' for x in e) else 'failed'
    return dict(decision=decision, acceptance=acceptance, closed=closed,
                label_entropy=entropy([x['mass'] for x in a]),
                class_entropy=entropy(list(groups.values())), support=support)

def base_record(n=2):
    r = dict(requirement='R', version='v1', implementation='build1', reviewed=True, conflict=False,
             criteria=[f'C{i}' for i in range(n)],
             alternatives=[dict(id='a', **{'class':'A'}, mass=1),dict(id='b', **{'class':'B'}, mass=1)])
    r['evidence'] = [dict(id=f'E{i}',criterion=c,requirement='R',version='v1',implementation='build1',
                          source=f'constructed://{i}',reviewer='declared-policy',approved=True,result='pass')
                     for i,c in enumerate(r['criteria'])]
    return r
