# Truss — vertical-only displacement interpretation

## Sources
- Boran chat, 29 August 2026 11:24 and 11:32: 2 m wall offset; solid circular fixed-section steel bars; 1 m/sqrt(2) m lengths; 1000 kgf; displacement below 2 cm; yielding/buckling; minimum mass.

## Assumptions and unresolved inputs
- This is the unresolved alternative meaning of displacement, not an additional constraint on project 02.
- Only the differing requirement is included; all other constraints are shared with project 02.

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

### TRUSS-V-05

whenever assessment_active the TrussSystem shall immediately satisfy (vertical_displacement_m < 0.02)

Alternative interpretation retained for stakeholder clarification.

FRET infinite-trace formula:

```text
(G (assessment_active -> (vertical_displacement_m < 0.02)))
```
