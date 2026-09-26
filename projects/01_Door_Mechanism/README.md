# Door mechanism — clarified toy baseline

## Sources
- Boran chat, 26–27 August 2026: hinged room door; stakeholder/system/subsystem requirements; no sharp edges.
- report_build/build_project_report.py: target package 1011; ages 6–12, P0, 10 N, full opening/closing.

## Assumptions and unresolved inputs
- The original nine-requirement attachment is absent. These are traceable decompositions of the available text, not a recovered verbatim list.
- 10 N, ages 6–12, P0 and 90 degrees come from the illustrative project report, not a child-safety standard.
- P0 geometry, operating speed, environment and edge criteria remain unspecified. p0_active/test_active are test-harness signals, not evidence that a real test took place.
- Open and close requests are separate phases; no maximum duration was supplied. Eventually therefore has no invented deadline.
- sharp_edges_present needs an agreed inspection method. No unprovided edge radius is invented.

## Signals
- `test_active`: bool: active, correctly configured P0 trial
- `p0_active`: bool: P0 fixture in use
- `force_n`: nonnegative real: measured instantaneous operating force, N
- `hands_used`: integer: number of hands used
- `scope_approved`: bool: approved scope record
- `minimum_age`: integer: lower age in approved scope
- `maximum_age`: integer: upper age in approved scope
- `fixture_approved`: bool: fixture/procedure approval
- `open_requested`: bool: rising edge begins an opening operation
- `close_requested`: bool: rising edge begins closing
- `latch_released`: bool: latch disengaged
- `opened_90`: bool: observed opening from 0 to 90 degrees
- `closed_and_latched`: bool: observed closed and engaged
- `inspection_active`: bool: agreed edge inspection in progress
- `sharp_edges_present`: bool: inspection result; criterion unresolved

### DOOR-01

whenever scope_approved the DoorSystem shall immediately satisfy (minimum_age = 6 & maximum_age = 12)

Approved user scope follows target A=1.

FRET infinite-trace formula:

```text
(G (scope_approved -> ((minimum_age = 6) & (maximum_age = 12))))
```

### DOOR-02

whenever test_active the DoorSystem shall immediately satisfy (p0_active & fixture_approved)

P0 and its approved procedure are required during the trial.

FRET infinite-trace formula:

```text
(G (test_active -> (p0_active & fixture_approved)))
```

### DOOR-03

whenever test_active the DoorSystem shall immediately satisfy (force_n <= 10)

The 10 N peak limit is expressed at every sampled trial point; sampling must capture the true peak.

FRET infinite-trace formula:

```text
(G (test_active -> (force_n <= 10)))
```

### DOOR-04

whenever test_active the DoorSystem shall immediately satisfy (hands_used = 1)

One-handed operation at every active trial sample.

FRET infinite-trace formula:

```text
(G (test_active -> (hands_used = 1)))
```

### DOOR-05

when open_requested the DoorSystem shall eventually satisfy latch_released

Opening requires eventual latch release. Added decomposition of the stated full function.

FRET infinite-trace formula:

```text
((G (((! open_requested) & (X open_requested)) -> (X (F latch_released)))) & (open_requested -> (F latch_released)))
```

### DOOR-06

when open_requested the DoorSystem shall eventually satisfy opened_90

Opening reaches the report’s 90-degree target.

FRET infinite-trace formula:

```text
((G (((! open_requested) & (X open_requested)) -> (X (F opened_90)))) & (open_requested -> (F opened_90)))
```

### DOOR-07

when close_requested the DoorSystem shall eventually satisfy closed_and_latched

Closing completes and latch engages; no deadline was supplied.

FRET infinite-trace formula:

```text
((G (((! close_requested) & (X close_requested)) -> (X (F closed_and_latched)))) & (close_requested -> (F closed_and_latched)))
```

### DOOR-08

whenever inspection_active the DoorSystem shall immediately satisfy !sharp_edges_present

Preserves the no-sharp-edges concern, with inspection criterion explicitly unresolved.

FRET infinite-trace formula:

```text
(G (inspection_active -> (! sharp_edges_present)))
```
