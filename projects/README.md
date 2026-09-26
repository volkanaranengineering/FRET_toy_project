# Separate toy requirements in NASA FRET

Open **index.html** for the readable output, or run **Show-Toy-Projects.cmd** for the native FRET interface with a dedicated database.

The package contains 10 separate projects and 61 formalized requirements. The five decision workflows are variants of the same door project. The vertical-only truss interpretation is separate from total displacement. The request/response project retains both tutorial interpretations as alternatives for comparison.

The native dashboard reports 11 projects because it includes the empty built-in Default project. It reports 61 requirements and 100% formalized. Actual screenshots are saved in `screenshots/`.

## What is actual FRET output?

`build.cjs` calls the installed NASA FRET 3.0 compiler. Each project folder contains:

- `fret-project.json`: importable requirements with compiled semantics.
- `fret-output.json`: full, unmodified compiler semantics, including formulas.
- `*.svg`: original FRET semantic templates selected by the compiler.
- `README.md`: source mapping, assumptions, signals and infinite-trace formulas.

`all-projects.json` can be imported using FRET’s downward-arrow import button. Select JSON, not CSV. CSV import may quote the text as unformalized natural language. The dedicated desktop database is already populated; it is separate from the existing tutorial database in `the original workspace NASA-FRET/data`.

## What was tested?

`collect-evidence.py` reuses the existing project’s HTTP servers and six-level ledger schedules without modifying them. It records 40 new localhost requests and 30 schedule snapshots here.

`check-examples.cjs` checks 177 examples, covering all 61 requirements: boundary values, counterexamples, missing/stale acceptance evidence, finite observations, and the fresh HTTP/schedule observations. All expected outcomes matched. This is an independently authored checker for the stated subset, **not FRET/LTLSIM simulation, realizability analysis or a proof of system correctness**. Synthetic door and truss snapshots are explicitly identified.

For unbounded eventual responses and truncated bounded observations, the checker reports `INCOMPLETE` rather than claiming evidence of satisfaction. FRET’s exact finite-trace formulas can have weaker end-of-trace semantics; both are shown transparently. `NOT_TRIGGERED` never counts as positive behavioral evidence.

## Reproduce

From this repository root, after installing the locked compiler dependencies (see ../docs/REPRODUCIBILITY.md):

```powershell
node './projects/build.cjs'
python './projects/collect-evidence.py'
node './projects/check-examples.cjs'
node './projects/report.cjs'
```

`seed-database.cjs` is a one-time initializer. It refuses to overwrite a nonempty database. After editing/rebuilding requirements, import the updated JSON through FRET rather than claiming the old database has automatically changed.

## Source coverage and limitations

Recovered sources: the two project tasks, the supplied Boran chat ZIP, the existing door/decision reports, the original FRET tutorial, and the latest HTTP paper artifact. The chat ZIP omits the original nine door requirements, grid image, and structural report. Available statements are decomposed here; missing lists are not claimed recovered.

The original “effortless” phrase remains a stakeholder intent. The 10 N target, ages 6–12, P0 and 90° come from the later illustrative project report; they are not evidence of actual child usability or compliance. Fixture, edge inspection and physical trial details remain unresolved.

The truss geometry, section, material properties and solver are absent. FRET formalizes constraints on solver outputs; it does not perform structural analysis or find a minimum-mass structure. Its optimality requirement is explicitly conditional on a declared finite exhaustive search.

Native FRET variables may appear as untyped until signal types and model mapping are configured. The JSON catalog and each README define their intended types and units. No external verification export is claimed complete.

The cellular automaton rules remain separate visualization experiments in the existing MATLAB project; no artificial FRET product requirement was invented for each rule. Similarly, research-plan alternatives and survey suggestions are not product behavior requirements.

References: [NASA FRET](https://github.com/NASA-SW-VnV/fret), [HTTP HEAD](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.2), [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#section-8.6).
