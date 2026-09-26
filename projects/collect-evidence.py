"""Reuse the project's existing executable examples; save fresh observations here."""
from pathlib import Path
import importlib.util
import sys
import json

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
old = WORKSPACE / 'research/revision_v3/artifact'
sys.path.insert(0, str(old))
import http_case

http_rows, raw = [], []
for mode in ('correct', 'omit_length', 'body_bug', 'length_bug'):
    pairs, wire = http_case.collect(mode)
    http_rows.extend(pairs)
    raw.extend(wire)
(ROOT / 'http-observations.json').write_text(json.dumps(http_rows, indent=2), encoding='utf-8')
(ROOT / 'http-raw-responses.json').write_text(json.dumps(raw, indent=2), encoding='utf-8')

schedule_path = WORKSPACE / 'research/decision_workflows/ledger_schedules.py'
spec = importlib.util.spec_from_file_location('existing_schedules', schedule_path)
schedule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schedule)
rows = []
for method in range(1, 6):
    for gate in range(6):
        weights = schedule.distribution(method, gate)
        rows.append(dict(method=method, level=gate+1, step=gate*11,
                         candidate_count=sum(w > 0 for w in weights), weights=weights,
                         selected_package=11 if gate == 5 else -1,
                         gate_observed=True, open_topics=0 if gate == 5 else 4))
(ROOT / 'workflow-observations.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
print(json.dumps(dict(http_requests=len(raw), http_pairs=len(http_rows), workflow_snapshots=len(rows))))
