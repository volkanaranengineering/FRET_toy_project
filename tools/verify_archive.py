"""Verify archive integrity and scoped evidence; no FRET or MATLAB execution."""
from pathlib import Path
from html.parser import HTMLParser
import argparse
import base64
import csv
import hashlib
import json
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def read(name): return json.loads((ROOT / name).read_text(encoding='utf-8'))


class Links(HTMLParser):
    def __init__(self): super().__init__(); self.paths = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and not value.startswith(('http:', 'https:', '#', 'data:')):
                self.paths.append(unquote(value.split('#')[0]))


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--write-report', action='store_true'); args = parser.parse_args()
    with (ROOT / 'docs/DATA_CATALOG.csv').open(encoding='utf-8', newline='') as f: rows = list(csv.DictReader(f))
    assert rows and len({r['path'] for r in rows}) == len(rows), 'Empty/duplicate manifest'
    for row in rows:
        p = ROOT / row['path']
        assert p.resolve().is_relative_to(ROOT.resolve()), 'Path escapes repository'
        data = p.read_bytes()
        assert len(data) == int(row['bytes']), f'Size differs: {row["path"]}'
        assert hashlib.sha256(data).hexdigest() == row['sha256'], f'Hash differs: {row["path"]}'
    # A ZIP download is also verifiable; Git coverage checks apply to an actual clone.
    git_coverage = 'not checked (source ZIP)'
    if (ROOT / '.git').exists():
        indexed = {p.decode('utf-8') for p in subprocess.check_output(['git', '-C', str(ROOT), 'ls-files', '-z']).split(b'\0') if p}
        exemptions = {'docs/DATA_CATALOG.csv', 'docs/verification.json'}
        assert indexed - exemptions == {r['path'] for r in rows}, 'Indexed files differ from catalog'
        forbidden = ('node_modules/', 'desktop-data/', '__pycache__/', '.env')
        assert not any(any(x in p for x in forbidden) for p in indexed), 'Excluded runtime/private file indexed'
        git_coverage = 'all indexed payload files covered'
    projects = read('projects/catalog.json'); exported = read('projects/all-projects.json')['requirements']
    assert len(projects) == 10 and len(exported) == 61
    assert len({r['reqid'] for r in exported}) == 61
    for p in projects:
        separate = read('projects/' + p['id'] + '/fret-project.json')['requirements']
        assert len(separate) == len(p['requirements'])
        assert all(r['project'] == p['id'] for r in separate)
        for r in separate:
            assert r['semantics']['ftExpanded'] and r['semantics']['ftInfAUExpanded']
            assert r in exported, 'Separate and combined exports differ'
    checks = read('projects/example-results.json')
    assert len(checks['results']) == 177
    assert all(r['actual'] == r['expected'] and r['ok'] for r in checks['results'])
    assert {r['id'] for r in checks['results']} == {r['reqid'] for r in exported}
    raw = read('projects/http-raw-responses.json'); observed = read('projects/http-observations.json')
    assert len(raw) == 40 and len(observed) == 20
    parsed = {}
    for record in raw:
        wire = base64.b64decode(record['response_base64'], validate=True)
        assert hashlib.sha256(wire).hexdigest() == record['sha256']
        head, body = wire.split(b'\r\n\r\n', 1)
        fields = dict(line.decode('ascii').split(': ', 1) for line in head.split(b'\r\n')[1:])
        key = (record['mode'], record['path'], record['method'])
        assert key not in parsed
        parsed[key] = (fields, body)
    for row in observed:
        gh, gb = parsed[(row['mode'], row['path'], 'GET')]
        hh, hb = parsed[(row['mode'], row['path'], 'HEAD')]
        assert gb == b'x' * int(row['path'][2:])
        assert row['get_bytes'] == len(gb) and row['head_bytes'] == len(hb)
        assert row['head_length'] == hh.get('Content-Length', 'absent')
        assert row['C1'] == (len(hb) == 0)
        assert row['C2'] == ('Content-Length' not in hh or int(hh['Content-Length']) == len(gb))
    snapshots = read('projects/workflow-observations.json')
    assert len(snapshots) == 30
    for row in snapshots:
        assert row['candidate_count'] == sum(w > 0 for w in row['weights'])
        assert abs(sum(row['weights']) - 1) < 1e-12
        assert row['step'] == (row['level'] - 1) * 11
    html = Links(); html.feed((ROOT / 'projects/index.html').read_text(encoding='utf-8'))
    assert all((ROOT / 'projects' / p).is_file() for p in html.paths), 'Broken HTML link'
    compiler = ROOT / 'vendor/fret/fret-electron/app/parser/FretSemantics.js'
    assert hashlib.sha256(compiler.read_bytes()).hexdigest() == read('projects/compilation-summary.json')['compiler_sha256']
    result = dict(status='PASS',catalog_files=len(rows),catalog_bytes=sum(int(r['bytes']) for r in rows),git_coverage=git_coverage,
                  projects=10,formalized_requirements=61,expected_outcomes_matched=177,http_raw_responses_checked=40,
                  workflow_snapshots_checked=30,html_local_links_checked=len(html.paths),compiler_hash_matches=True,
                  scope='Archive/evidence checks only; does not run FRET, a solver, physical tests or MATLAB.')
    if args.write_report: (ROOT / 'docs/verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__ == '__main__': main()
