"""Record reviewed, Git-indexed archive bytes. Never call just to silence a mismatch."""
from pathlib import Path
import csv
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'docs/DATA_CATALOG.csv', 'docs/verification.json'}


def tracked_paths():
    data = subprocess.check_output(['git', '-C', str(ROOT), 'ls-files', '-z'])
    return sorted(p.decode('utf-8') for p in data.split(b'\0') if p)


def category(name):
    if name.startswith('vendor/'): return 'NASA FRET upstream source snapshot'
    if name.startswith('research/'): return 'Historical research context and executable dependencies'
    if name.startswith('tutorial/'): return 'Original tutorial and supporting sources'
    if name.startswith('projects/'): return 'Toy project specification, output, evidence or adapter'
    return 'Repository documentation and reproduction tools'


def main():
    paths = [p for p in tracked_paths() if p not in EXCLUDED]
    if not paths: raise SystemExit('Stage the reviewed source files before creating a catalog.')
    rows = []
    for name in paths:
        content = (ROOT / name).read_bytes()
        rows.append(dict(path=name, bytes=len(content), sha256=hashlib.sha256(content).hexdigest(), category=category(name)))
    with (ROOT / 'docs/DATA_CATALOG.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['path', 'bytes', 'sha256', 'category'], lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    print(f'Recorded {len(rows)} indexed files; {sum(r["bytes"] for r in rows):,} bytes.')


if __name__ == '__main__': main()
