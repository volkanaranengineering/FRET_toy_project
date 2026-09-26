"""Idea 3: enumerate distinct trace questions and exact expected information gain."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import ROOT, entropy, group, load, trace_json, write_json


def posterior(classes, accepted, answer):
    weights = [c['probability'] if flag == answer else 0.0 for c, flag in zip(classes, accepted)]
    mass = sum(weights)
    return {'probability': mass, 'posterior': [w / mass for w in weights] if mass else None,
            'entropy_bits': entropy([w / mass for w in weights]) if mass else None}


def analyze(data):
    config, rows, traces, vectors, meta = data
    results = []
    for original in config['originals']:
        classes = group(config['hypotheses'][original['reqid']], vectors)
        initial = entropy([c['probability'] for c in classes])
        partitions = {}
        for index, trace in enumerate(traces):
            flags = tuple(bool(vectors[c['members'][0]][index]) for c in classes)
            if len(set(flags)) < 2 or flags in partitions: continue
            yes, no = posterior(classes, flags, True), posterior(classes, flags, False)
            expected = sum(b['probability'] * b['entropy_bits'] for b in (yes, no) if b['probability'])
            partitions[flags] = {'trace': trace_json(trace), 'accepts_by_class': list(flags),
                                 'expected_information_gain_bits': max(0.0, initial - expected),
                                 'yes': yes, 'no': no}
        questions = sorted(partitions.values(), key=lambda q: -q['expected_information_gain_bits'])
        results.append({**original, 'initial_entropy_bits': initial, 'classes': classes, 'questions': questions,
                        'question': 'Should this complete finite execution be permitted by the intended requirement?',
                        'answer_status': 'unanswered; no stakeholder response simulated',
                        'outside_candidate_answers': {'neither': 'reopen candidate set; no Bayesian update',
                                                      'unsure': 'retain current distribution'},
                        'answer_model': 'reliable binary answer; equal question cost; hypothesis-conditional predictions'})
    return {'idea': 3, 'title': 'Information-guided clarification', 'context': meta, 'results': results}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--horizon', type=int, default=6); args = p.parse_args()
    result = analyze(load(args.horizon))
    write_json(ROOT / '03_active_clarification/results.json', result)
    print([(r['reqid'], len(r['questions'])) for r in result['results']])
