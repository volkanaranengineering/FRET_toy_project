# Critical literature survey: FRET requirement entropy

Read the [19-page PDF report](FRET_Entropy_Literature_Survey.pdf) or its [editable Markdown version](FRET_Entropy_Literature_Survey.md).

**Review date:** 27 September 2026. **Window:** 27 September 2006 through 27 September 2026. **Corpus:** 18 journal papers and one explicitly supplementary conference paper. This is a scoped critical review, not an exhaustive systematic review or meta-analysis.

The report surveys the three entropy modules at implementation baseline `6443ce8`, with tutorial baseline `16a78ad`. It distinguishes supporting methodological literature from challenges to novelty, assumptions and empirical validity. The closest overlap is ARTEMIS (ICSE 2026), which already uses FRETish and balanced distinguishing traces. The proposed research gap concerns calibrated probabilities, incomplete candidate sets, uncertain answers and independently measured human accuracy and effort. It does not claim that entropy or trace-based clarification is new.

## Included files

- `FRET_Entropy_Literature_Survey.pdf`: formatted report, evidence profiles, gap and proposed study protocol.
- `FRET_Entropy_Literature_Survey.md`: editable full text.
- `evidence_ledger.json`: 19 records, DOI and primary links, access depth, supporting/challenging interpretations.
- `references.bib`: bibliography; J09 intentionally uses an abbreviated author list.
- `search_log.md`: search-method record and limitations.
- `build_report.py`: report source and deterministic content checks; requires `reportlab` and `pypdf`.
- `report_validation.json`: structural checks and visual-review status.

Run `python build_report.py` here to regenerate the PDF and companion text/data. A rebuild resets visual-review status to pending: render and inspect the new PDF before delivery. PDF byte hashes may change because of creation timestamps. Source text is in the builder; edits to generated Markdown do not feed back into the PDF.

No publisher full texts are redistributed. Abstract-only inspection is labelled and does not support detailed effect-size claims. Proposed experiments have not been conducted. The synthesis was prepared with OpenAI Codex under the user's direction and requires author verification and a fuller search before journal submission.
