# Provenance and source mapping

## NASA FRET snapshot

Source: https://github.com/NASA-SW-VnV/fret, downloaded 25 September 2026 (Europe/Istanbul), version 3.0.

Archive SHA-256:

```text
44f8095b595f8de9a045a4bdcd2d8300dc22573534b6c32672d95bc550773716
```

The source ZIP has 2,095 entries including directories and expands to 46,472,077 file bytes. Files are preserved in `vendor/fret/` without installed dependencies. No commit SHA is asserted: acquisition used a master-branch archive. Its archive hash and per-file catalog identify the exact snapshot. See `environment/upstream-provenance.json`.

Compiler SHA-256:

```text
a0cda458b5e64352c591adc517046fa79066639426765896a71642bc23bbb784
```

The adapter invokes NASA's `FretSemantics.compile`. Original upstream package and lockfiles are retained.

## Source locations

Historical paths embedded in descriptions map as follows:

| Historical source | Repository location |
|---|---|
| `NASA-FRET/toy-projects/` | `projects/` |
| `NASA-FRET/tutorial/` | `tutorial/` |
| `NASA-FRET/prepare-example.cjs` | `tutorial/prepare-example.cjs` |
| `output/pdf/research_revision_v3/` | `research/revision_v3/` |
| `output/pdf/conference_revision_v2/artifact/ledger_schedules.py` | `research/decision_workflows/ledger_schedules.py` |
| `output/pdf/proje_bes_yontem/` | `research/proje_bes_yontem/` |
| `output/pdf/alti_seviye/` | `research/alti_seviye/` |
| `matlab_stage/` | `research/matlab/` |

Available discussion statements established the door and truss intent. Later papers supplied illustrative door values and decision schedules. The FRET tutorial supplied the request/response examples; RFC 9110 supplied the scoped HEAD conditions.

Private chat exports, missing attachments, downloaded third-party literature, profiles and credentials are excluded. Omitted door lists and truss geometry are not claimed recovered.

## Repository adaptations

- Compiler/database/tutorial adapters use vendored FRET by default, with `FRET_HOME` override.
- HTTP/schedule dependencies resolve inside this repository.
- Tutorial PDF output is placed beside its sources.
- Desktop launch checks initialization and uses local ignored state.
- Catalog hashes preserve traceability across copies and fresh runs.
- Native screenshots document the initial FRET run; they are not claimed to depict a newly built binary in this checkout.
