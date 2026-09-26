"""Regenerate all three independent analyses and their offline interactive pages."""
import argparse
import copy
import importlib.util
import json
from common import ROOT, load, write_json
from report import render

DIRECTORIES = ['01_semantic_interpretation', '02_behavioral_freedom', '03_active_clarification']


def module(directory):
    spec = importlib.util.spec_from_file_location(directory, ROOT / directory / 'run.py')
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result


def main():
    p = argparse.ArgumentParser(); p.add_argument('--horizon', type=int, default=6); args = p.parse_args()
    data = load(args.horizon)
    results = [module(d).analyze(data) for d in DIRECTORIES]
    for directory, result in zip(DIRECTORIES, results):
        write_json(ROOT / directory / 'results.json', result)
        exported = []
        for requirement in data[1]:
            if result['idea'] == 2 and not requirement['reqid'].endswith('-original'):
                continue
            entry = copy.deepcopy(requirement)
            source_id = requirement['reqid'].split('-')[0] + '-' + requirement['reqid'].split('-')[1]
            summary = next(r for r in result['results'] if r['reqid'] == source_id)
            snapshot = {k: v for k, v in summary.items() if k.endswith('_bits') or k == 'admissible_traces'}
            if result['idea'] == 3:
                snapshot['best_expected_information_gain_bits'] = summary['questions'][0]['expected_information_gain_bits'] if summary['questions'] else 0
            entry['project'] = 'Entropy_' + directory
            entry['reqid'] = f"E{result['idea']}-" + requirement['reqid']
            entry['rationale'] = (f"{result['title']}. Source: {requirement['reqid']}. "
                f"Horizon {args.horizon} ticks. Analysis snapshot: {json.dumps(snapshot)}. "
                "Experimental priors/variants are analyst assumptions, not NASA ambiguity annotations. "
                "Acceptance not assessed. See the companion entropy report for full context.")
            exported.append(entry)
        write_json(ROOT / directory / 'fret-project.json', {'requirements': exported})
        (ROOT / directory / 'index.html').write_text(render([result], data[1], nested=True), encoding='utf-8', newline='\n')
    (ROOT / 'index.html').write_text(render(results, data[1]), encoding='utf-8', newline='\n')
    print('Generated three separate analyses and interactive HTML pages.')
    for result in results:
        print(result['title'])
        for row in result['results']:
            print(row['reqid'], {k: v for k, v in row.items() if k.endswith('_bits') or k == 'admissible_traces'})


if __name__ == '__main__': main()
