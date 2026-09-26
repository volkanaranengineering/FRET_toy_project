# Door workflow 1 — Sequential decision gates

## Sources
- output/pdf/conference_revision_v2/artifact/ledger_schedules.py (existing six-level schedule).
- Boran chat, 26–27 August 2026: hinged room door; stakeholder/system/subsystem requirements; no sharp edges.
- report_build/build_project_report.py: target package 1011; ages 6–12, P0, 10 N, full opening/closing.

## Assumptions and unresolved inputs
- The physical door contract is project 01. These are workflow-observation requirements, not five different physical products.
- Six levels: steps 0, 11, 22, 33, 44, 55. Ten exploration steps occur between gates.
- Candidate counts and target package 1011 come from the existing stipulated schedule; prototype ranks and evidence likelihoods are synthetic.
- Added formalization: closure requires all four current matching acceptance records. A unique candidate and zero entropy alone never imply acceptance.

## Signals
- `gate_observed`: bool: a level/gate record is available
- `level`: integer 1..6
- `step`: integer: model step
- `candidate_count`: integer: strictly positive support count
- `selected_package`: integer: ABCD binary interpreted as integer; target 1011 = 11
- `accepted`: bool: workflow claims implementation accepted
- `open_topics`: integer: unresolved decisions
- `current_evidence_count`: integer: distinct passing criteria matching requirement and implementation versions
- `evidence_valid`: bool: record identities, versions, sources and results are valid
- `test_failed`: bool: any current criterion failed

### M1-L1

whenever (gate_observed & level = 1) the DecisionLedger shall immediately satisfy (step = 0 & candidate_count = 16)

Existing method 1, level 1 schedule snapshot.

FRET infinite-trace formula:

```text
(G ((gate_observed & (level = 1)) -> ((step = 0) & (candidate_count = 16))))
```

### M1-L2

whenever (gate_observed & level = 2) the DecisionLedger shall immediately satisfy (step = 11 & candidate_count = 16)

Existing method 1, level 2 schedule snapshot.

FRET infinite-trace formula:

```text
(G ((gate_observed & (level = 2)) -> ((step = 11) & (candidate_count = 16))))
```

### M1-L3

whenever (gate_observed & level = 3) the DecisionLedger shall immediately satisfy (step = 22 & candidate_count = 8)

Existing method 1, level 3 schedule snapshot.

FRET infinite-trace formula:

```text
(G ((gate_observed & (level = 3)) -> ((step = 22) & (candidate_count = 8))))
```

### M1-L4

whenever (gate_observed & level = 4) the DecisionLedger shall immediately satisfy (step = 33 & candidate_count = 4)

Existing method 1, level 4 schedule snapshot.

FRET infinite-trace formula:

```text
(G ((gate_observed & (level = 4)) -> ((step = 33) & (candidate_count = 4))))
```

### M1-L5

whenever (gate_observed & level = 5) the DecisionLedger shall immediately satisfy (step = 44 & candidate_count = 2)

Existing method 1, level 5 schedule snapshot.

FRET infinite-trace formula:

```text
(G ((gate_observed & (level = 5)) -> ((step = 44) & (candidate_count = 2))))
```

### M1-L6

whenever (gate_observed & level = 6) the DecisionLedger shall immediately satisfy (step = 55 & candidate_count = 1)

Existing method 1, level 6 schedule snapshot.

FRET infinite-trace formula:

```text
(G ((gate_observed & (level = 6)) -> ((step = 55) & (candidate_count = 1))))
```

### M1-FINAL

whenever (gate_observed & level = 6) the DecisionLedger shall immediately satisfy (selected_package = 11 & open_topics = 0)

Final design commitment is package 1011, without claiming acceptance.

FRET infinite-trace formula:

```text
(G ((gate_observed & (level = 6)) -> ((selected_package = 11) & (open_topics = 0))))
```

### M1-ACCEPT

whenever accepted the DecisionLedger shall immediately satisfy (current_evidence_count = 4 & evidence_valid & !test_failed)

Added acceptance guard, consistent with later paper revisions. Four distinct, current, matching passing records are required.

FRET infinite-trace formula:

```text
(G (accepted -> (((current_evidence_count = 4) & evidence_valid) & (! test_failed))))
```
