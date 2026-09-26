# Idea 2 — Behavioral freedom

Run `python entropy/02_behavioral_freedom/run.py --horizon 6` from the repository root. Read [results.json](results.json) or open [index.html](index.html).

Counts refer only to the two original setup statements. All 4,096 six-tick Boolean traces are enumerated against actual FRET finite formulas: `when` permits 3,848 and `whenever` permits 3,784. The conjunction also permits 3,784. This quantifies restriction of a fixed uniform behavioral universe, not ambiguity or quality.

Marginal information is conditional on the other requirement. Empty sets are inconsistent, with undefined entropy. See the [parent README](../README.md) for formulas, boundary semantics, reproduction and validation. Run `python entropy/run_all.py` to refresh HTML after changing inputs.
