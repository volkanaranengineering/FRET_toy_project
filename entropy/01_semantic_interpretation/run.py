"""Idea 1: mass-preserving bounded semantic interpretation entropy."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import ROOT, entropy, group, load, write_json


def analyze(data):
    config, rows, traces, vectors, meta = data
    results = []
    for original in config['originals']:
        candidates = config['hypotheses'][original['reqid']]
        classes = group(candidates, vectors)
        results.append({**original, 'baseline_single_interpretation_entropy_bits': 0.0,
                        'baseline_interpretation': 'Original FRETish is already precise; no measured ambiguity asserted.',
                        'experimental_candidate_entropy_bits': entropy([c['prior'] for c in candidates]),
                        'experimental_meaning_entropy_bits': entropy([c['probability'] for c in classes]),
                        'classes': classes, 'prior_source': config['prior_source'],
                        'candidate_completeness': config['candidate_completeness'], 'acceptance': config['acceptance']})
    return {'idea': 1, 'title': 'Semantic interpretation entropy', 'context': meta, 'results': results}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--horizon', type=int, default=6); args = p.parse_args()
    result = analyze(load(args.horizon))
    write_json(ROOT / '01_semantic_interpretation/results.json', result)
    print([(r['reqid'], r['experimental_meaning_entropy_bits']) for r in result['results']])
