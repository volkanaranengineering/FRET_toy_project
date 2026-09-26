# Steel truss — feasibility and bounded optimality contract

## Sources
- Boran chat, 29 August 2026 11:24 and 11:32: 2 m wall offset; solid circular fixed-section steel bars; 1 m/sqrt(2) m lengths; 1000 kgf; displacement below 2 cm; yielding/buckling; minimum mass.

## Assumptions and unresolved inputs
- The original grid image and structural report are absent. Grid nodes, diameter, steel properties, support/joint model, safety factors and tolerances remain open.
- Displacement is interpreted as total displacement magnitude. Vertical-only is retained as a separate alternative requirement, not conjoined with the selected interpretation.
- FRET does not solve statics or optimization. Geometry/stability/utilizations are inputs from a separate solver. No structural design is claimed verified.
- Yield/buckling utilization <=1 means the demand/capacity ratio with the chosen safety factor already included. Capacity model and factor must be agreed.
- enumerated_min_mass_kg refers only to a declared finite, exhaustively checked candidate set. It is not a global continuous-design optimum.

## Signals
- `assessment_active`: bool: evaluate one declared candidate/load case
- `load_kgf`: real: downward vertical load magnitude, kgf
- `offset_m`: real: loaded node distance from wall, m
- `steel_only`: bool: all bars are specified steel
- `solid_circular`: bool: all bars solid circular
- `fixed_section`: bool: common specified cross-section
- `allowed_lengths`: bool: every bar has length 1 m or sqrt(2) m within agreed tolerance
- `available_grid_only`: bool: endpoints belong to the provided grid
- `connected_to_wall`: bool: loaded node connected to wall supports
- `stable`: bool: solver establishes a stable supported structure
- `joints_rigid_enough`: bool: joint deformation neglected under source assumption
- `displacement_m`: nonnegative real: loaded-node displacement magnitude, m
- `vertical_displacement_m`: nonnegative real: absolute vertical displacement, m
- `yield_utilization`: nonnegative real: maximum yielding demand/capacity across bars
- `buckling_utilization`: nonnegative real: maximum compressive demand/buckling capacity across bars
- `selection_complete`: bool: candidate selection complete
- `feasible`: bool: conjunction of all feasibility checks for this load case
- `enumeration_complete`: bool: declared finite set exhaustively checked
- `mass_kg`: nonnegative real: selected candidate mass
- `enumerated_min_mass_kg`: nonnegative real: independently computed minimum feasible mass in the declared set

### TRUSS-01

whenever assessment_active the TrussSystem shall immediately satisfy (load_kgf = 1000 & offset_m = 2)

The specified load case and wall offset.

FRET infinite-trace formula:

```text
(G (assessment_active -> ((load_kgf = 1000) & (offset_m = 2))))
```

### TRUSS-02

whenever assessment_active the TrussSystem shall immediately satisfy (steel_only & solid_circular & fixed_section)

Source material and cross-section restrictions.

FRET infinite-trace formula:

```text
(G (assessment_active -> ((steel_only & solid_circular) & fixed_section)))
```

### TRUSS-03

whenever assessment_active the TrussSystem shall immediately satisfy (allowed_lengths & available_grid_only)

Allowed bar lengths and grid membership; upstream geometry checks.

FRET infinite-trace formula:

```text
(G (assessment_active -> (allowed_lengths & available_grid_only)))
```

### TRUSS-04

whenever assessment_active the TrussSystem shall immediately satisfy (connected_to_wall & stable & joints_rigid_enough)

Connection, stability and the source joint idealization.

FRET infinite-trace formula:

```text
(G (assessment_active -> ((connected_to_wall & stable) & joints_rigid_enough)))
```

### TRUSS-05

whenever assessment_active the TrussSystem shall immediately satisfy (displacement_m < 0.02)

Strictly below 2 cm; total magnitude interpretation.

FRET infinite-trace formula:

```text
(G (assessment_active -> (displacement_m < 0.02)))
```

### TRUSS-06

whenever assessment_active the TrussSystem shall immediately satisfy (yield_utilization <= 1)

Every member satisfies the chosen yield criterion.

FRET infinite-trace formula:

```text
(G (assessment_active -> (yield_utilization <= 1)))
```

### TRUSS-07

whenever assessment_active the TrussSystem shall immediately satisfy (buckling_utilization <= 1)

Every compressed member satisfies the chosen buckling criterion.

FRET infinite-trace formula:

```text
(G (assessment_active -> (buckling_utilization <= 1)))
```

### TRUSS-08

whenever selection_complete the TrussSystem shall immediately satisfy (feasible & enumeration_complete & mass_kg = enumerated_min_mass_kg)

Bounded optimality certificate from an external enumerator; no global-optimality proof is produced by FRET.

FRET infinite-trace formula:

```text
(G (selection_complete -> ((feasible & enumeration_complete) & (mass_kg = enumerated_min_mass_kg))))
```
