"""Check the notes' numerical examples against the saved experiment outputs."""
from pathlib import Path
import json
import math
from itertools import product
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
DATA = next(candidate for ancestor in HERE.parents
            for candidate in (ancestor / 'entropy', ancestor / 'FRET_toy_project/entropy')
            if (candidate / 'inputs/analysis.json').is_file())

def H(ps): return -sum(p * math.log2(p) for p in ps if p)
def read(path): return json.loads(path.read_text(encoding='utf-8'))

def main():
    traces = list(product(((0, 0), (0, 1), (1, 0), (1, 1)), repeat=6))
    counts = []
    events = {}
    for mode in ('when', 'whenever'):
        sets = [{i for i, trace in enumerate(traces)
                 if trace[t][0] and (mode == 'whenever' or t == 0 or not trace[t-1][0])
                 and not any(trace[j][1] for j in range(t, t+4))} for t in range(3)]
        event_counts = [len(s) for s in sets]
        intersections = [len(sets[0] & sets[1]), len(sets[1] & sets[2]), len(sets[0] & sets[2])]
        triple = len(sets[0] & sets[1] & sets[2])
        passed = len(traces) - len(set.union(*sets))
        events[mode] = dict(single=event_counts, pair=intersections, triple=triple, passed=passed)
        counts.append(passed)
    assert events['when'] == dict(single=[128,64,64],pair=[0,0,8],triple=0,passed=3848)
    assert events['whenever'] == dict(single=[128,128,128],pair=[32,32,16],triple=8,passed=3784)
    behavior = read(DATA / '02_behavioral_freedom/results.json')['results']
    assert counts == [r['admissible_traces'] for r in behavior]
    meaning = read(DATA / '01_semantic_interpretation/results.json')['results']
    assert all(r['experimental_meaning_entropy_bits'] == H([.5,.25,.25]) for r in meaning)
    questions = read(DATA / '03_active_clarification/results.json')['results']
    assert math.isclose(questions[0]['questions'][0]['expected_information_gain_bits'], 1)
    assert math.isclose(questions[1]['questions'][0]['expected_information_gain_bits'], H([.25,.75]))
    pdf = PdfReader(HERE / 'FRET_Entropy_Class_Notes.pdf')
    assert len(pdf.pages) == 15
    text = '\n'.join(page.extract_text() for page in pdf.pages)
    compact = ''.join(text.split())
    for s in ['3,848', '3,784', '0.811278', '43,680', 'Exercises']:
        assert s in compact, s
    assert all(len(page.extract_text()) > 500 for page in pdf.pages)
    log = (HERE / 'FRET_Entropy_Class_Notes.log').read_text(errors='replace')
    assert 'Overfull' not in log and 'Missing character' not in log
    report = dict(status='PASS', pages=len(pdf.pages), event_counts=events,
                  meaning_entropy=H([.5,.25,.25]), clarification_gain=[1,H([.25,.75])],
                  exercises=dict(ex1=H([.8,.1,.1]),ex2_label=H([.1]*5+[.25]*2),ex4=H([.2,.8])),
                  scope='Numerical examples, PDF text presence, page count, LaTeX overflow/glyph log; visual review performed separately.')
    (HERE / 'notes_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__ == '__main__': main()
