"""Idea 2: exact bounded trace counts and marginal constraint information."""
import argparse
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import ROOT, load, write_json


def measure(before, after):
    if not before:
        return {'status': 'inconsistent context', 'entropy_bits': None, 'information_bits': None}
    if not after:
        return {'status': 'inconsistent result', 'entropy_bits': None, 'information_bits': None}
    return {'status': 'consistent', 'entropy_bits': math.log2(after), 'information_bits': math.log2(before / after)}


def analyze(data):
    config, rows, traces, vectors, meta = data
    ids = [r['reqid'] + '-original' for r in config['originals']]
    counts = {i: sum(vectors[i]) for i in ids}
    joint = sum(all(vectors[i][t] for i in ids) for t in range(len(traces)))
    return {'idea': 2, 'title': 'Behavioral freedom and constraint information', 'context': meta,
            'unconstrained_entropy_bits': math.log2(len(traces)),
            'results': [{'reqid': i.removesuffix('-original'), 'admissible_traces': counts[i],
                         **measure(len(traces), counts[i]),
                         'marginal_given_other': {'before': counts[ids[1-j]], 'after': joint,
                                                 **measure(counts[ids[1-j]], joint)}} for j, i in enumerate(ids)],
            'conjunction': {'admissible_traces': joint, **measure(len(traces), joint)},
            'interpretation': 'Freedom is not ambiguity, quality, correctness, or acceptance. Counts are not counts of implementations.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--horizon', type=int, default=6); args = p.parse_args()
    result = analyze(load(args.horizon))
    write_json(ROOT / '02_behavioral_freedom/results.json', result)
    print([(r['reqid'], r['admissible_traces']) for r in result['results']])
