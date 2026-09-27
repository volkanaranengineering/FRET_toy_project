# Three separate entropy experiments on the FRET setup requirements

**[Step-by-step class notes (15-page PDF)](tutorial/FRET_Entropy_Class_Notes.pdf)** explain every measure, the hand calculations, and how to use the outputs. [Editable LaTeX and build instructions](tutorial/README.md).

Open **[the interactive report](index.html)** locally. Each implementation also has its own script, JSON results, and HTML page:

| Idea | Implementation | Output |
|---|---|---|
| 1. Semantic interpretation entropy | [01_semantic_interpretation/run.py](01_semantic_interpretation/run.py) | [Interactive page](01_semantic_interpretation/index.html), [JSON](01_semantic_interpretation/results.json) |
| 2. Behavioral freedom | [02_behavioral_freedom/run.py](02_behavioral_freedom/run.py) | [Interactive page](02_behavioral_freedom/index.html), [JSON](02_behavioral_freedom/results.json) |
| 3. Active clarification | [03_active_clarification/run.py](03_active_clarification/run.py) | [Interactive page](03_active_clarification/index.html), [JSON](03_active_clarification/results.json) |

This is an executable **research companion**, not a modification of NASA's native FRET UI. The upstream source remains intact. The JSON export can be imported into FRET; the interactive entropy panels run in a browser, including offline. Shared input compilation and finite-formula evaluation avoid three inconsistent semantic implementations.

Each idea also has a separate native FRET import file: [Idea 1](01_semantic_interpretation/fret-project.json), [Idea 2](02_behavioral_freedom/fret-project.json), [Idea 3](03_active_clarification/fret-project.json). Import these with FRET's import button to obtain three separate projects. Ideas 1 and 3 contain eight experimental candidates each; Idea 2 contains the two originals. IDs are prefixed to avoid collisions. Computed snapshots appear in each requirement's rationale; interactive analysis remains in the companion browser page. These are duplicated analysis views of two source requirements, not 18 independent requirements.

## Exact scope and source

The user selected the **two setup/tutorial examples**, not all bundled NASA case studies. FRET's built-in `Default` project itself is empty in this setup. The source is the repository's [original setup export](../tutorial/FRET_Tutorial_TR.json):

1. `REQ-001`: `when request the ResponseSystem shall within 3 ticks satisfy response`
2. `REQ-002`: `whenever request the ResponseSystem shall within 3 ticks satisfy response`

These are already precise FRETish statements. We do not claim NASA assigned ambiguity, priors, or entropy numbers to them. The analyses use original statements for behavioral counting and explicitly constructed alternatives for interpretation and clarification experiments.

For each original, `compile.cjs` creates four candidates: original statement (mass 0.25), a punctuation-equivalent spelling (mass 0.25), a two-tick deadline (mass 0.25), and the other trigger type (mass 0.25). Thus the original meaning has mass 0.5. This is an illustrative analyst prior, not measured stakeholder data or LLM confidence. Candidate completeness is unassessed. Original requirements are never overwritten.

## Reproduce

Requires Python 3.10+ (standard library only) and the existing FRET dependencies for recompilation. Run from the repository root:

```powershell
# First install FRET dependencies if needed; see ../docs/REPRODUCIBILITY.md.
node entropy/compile.cjs
python entropy/run_all.py --horizon 6
python entropy/test_entropy.py
```

`FRET_HOME` can select a compatible local `fret-electron` installation. The default is `vendor/fret/fret-electron`. The checked-in compiled inputs let the Python analyses run without Node or a fresh FRET installation. `inputs/analysis.json` records source and compiler SHA-256; every result records the compiled project hash.

Each analysis can also run independently:

```powershell
python entropy/01_semantic_interpretation/run.py --horizon 6
python entropy/02_behavioral_freedom/run.py --horizon 6
python entropy/03_active_clarification/run.py --horizon 6
```

Individual scripts regenerate their own JSON only. `run_all.py` regenerates the HTML pages as well. Horizons 1–8 are supported; enumeration grows as `4^h`, so this is deliberately bounded. Checked-in reports use horizon 6. Restore that horizon after sensitivity experiments to reproduce the published outputs.

## Semantic contract

`common.py` parses and evaluates the **actual FRET-generated `ftExpanded` formulas**, rather than inventing formulas. Supported operators are Boolean connectives, strong next `X`, bounded eventually `F[a,b]`, finite release `V`, and `LAST`, over `request` and `response`. Unsupported syntax fails explicitly. This is not a general-purpose FRET/LTL solver.

For these requirements, a trigger at tick `t` may be satisfied at `t` through `t+deadline`, inclusive. If the finite trace ends before the deadline expires, FRET permits the unfinished obligation. `when` triggers on a rising edge (including an initially true request); `whenever` triggers at every true request tick. No terminal completion assumption or physical time unit is invented.

All `4^6 = 4,096` assignments to the two Boolean signals across six ticks are enumerated. There are no environmental restrictions. Semantic equivalence means identical truth vectors **at this fixed horizon only**. Short horizons can hide differences: at two ticks all experimental candidates accept every trace because all deadlines remain unfinished.

## 1. Semantic interpretation entropy

Candidates are grouped by bounded truth-vector equality. Entropy is `-sum(p * log2(p))` over grouped masses. Duplicating a spelling while splitting its original probability mass leaves semantic entropy unchanged. Duplicating and assigning a fresh uniform prior does not have that guarantee.

At six ticks, each requirement has four candidates but three meaning classes: ungrouped entropy is **2 bits**, semantic entropy **1.5 bits**. With only its original formalization, the baseline is **0 bits**. These are different candidate-set assumptions, not before/after evidence of improved quality. The browser supports exploratory class weights and flags invalid inputs.

## 2. Behavioral freedom and marginal information

For a fixed uniform trace universe, `H_behavior(R) = log2(number of satisfying traces)`. The contribution of an added requirement is `log2(count_before / count_after)`. This is behavioral freedom, not uncertainty about stakeholder intent.

| Requirement | Satisfying traces | Behavioral entropy | Information vs unrestricted |
|---|---:|---:|---:|
| REQ-001: when | 3,848 | 11.909893 bits | 0.090107 bits |
| REQ-002: whenever | 3,784 | 11.885696 bits | 0.114304 bits |

The conjunction admits 3,784 traces. Adding `when` after `whenever` contributes **0 bits**; adding `whenever` after `when` contributes approximately **0.024197 bits**. Redundancy here is conditional on the other requirement and the chosen universe. Empty satisfying sets are labeled inconsistent with undefined entropy, never assigned zero entropy. Nonuniform distributions would require a different calculation; these results must not be reused as general entropy-reduction claims.

## 3. Active clarification

Every six-tick trace is considered as a possible question: “Should this complete finite execution be permitted by the intended requirement?” Equivalent answer partitions are deduplicated. Questions are ranked by `H(prior) - sum(P(answer) * H(posterior))`, under reliable binary answers and equal cost.

The best first question yields **1 bit** for REQ-001 and **0.811278 bits** for REQ-002. The difference follows from candidate structure: for REQ-002, the tighter holding requirement implies the original holding requirement, which implies the rising-edge alternative. A single trace cannot isolate the middle meaning from both extremes. Equal initial entropy therefore does not imply equal available information gain.

The interactive page recomputes the best question after each answer. Yes/no performs a Bayesian elimination update. Unsure retains the distribution; neither reopens the candidate set and blocks further questions until reset/revision. Export saves the local session, trace, before/after probabilities, and analysis context as JSON. No answers are pre-filled, authenticated, uploaded, or persisted automatically. No acceptance decision follows from zero entropy.

## Validation and research limitations

`test_entropy.py` compares the generated-formula evaluator against an independent trigger/deadline obligation implementation for all eight candidates at horizons 1–6: **43,680 formula/trace comparisons**. Additional tests check malformed probabilities, unsupported syntax, finite boundaries, mass-preserving aliases, bounded equivalence, inconsistency, implication/redundancy, generated witnesses, and posterior normalization. [Machine-readable validation](validation.json).

This evidence establishes a small reproducible computational experiment. It is not unbounded equivalence checking, realizability analysis, native LTLSIM execution, a stakeholder study, calibrated intent inference, or journal validation. No physical safety, engineering correctness, or requirement acceptance is inferred. Actual FRET compilation and independent bounded checks are reported separately. Future generalization requires additional syntax support, independent solver comparison, real elicitation data, noisy-answer models, and larger independent case studies.

## Research basis and authorship

- [FRETish formal semantics](https://arxiv.org/abs/2201.03641)
- [Requirements Entropy Framework](https://doi.org/10.1111/sys.21283)
- [Semantic uncertainty and linguistic invariance](https://arxiv.org/abs/2302.09664)
- [Information-guided temporal logic inference](https://arxiv.org/abs/1811.08846)
- [A Weakness Measure for GR(1) Formulae](https://d-nb.info/1223522601/34)
- [Active Learning of Signal Temporal Logic Specifications](https://people.kth.se/~linard/publications/active_learn_stl.pdf)

Implementation and documentation developed by OpenAI Codex under Volkan Aran's direction. Existing mathematics and related work are acknowledged; no claim that entropy, model counting, or active learning itself is novel is made.
