# Idea 3 — Information-guided clarification

Run `python entropy/03_active_clarification/run.py --horizon 6` from the repository root. Read [results.json](results.json) or open [index.html](index.html).

This independently executable analysis consumes the shared compiled candidates; it does not require Idea 1's result file. It enumerates distinguishing traces, deduplicates answer partitions, and ranks expected information gain under the declared illustrative priors. The best initial gain is 1 bit for REQ-001 and approximately 0.811278 bits for REQ-002.

Use the interactive page to answer questions and export an answer ledger. Yes/no updates the posterior and question ranking; unsure preserves it; neither reopens the candidate set. Initial reports contain no fabricated stakeholder answers. Zero entropy is not acceptance evidence. See the [parent README](../README.md) for the complete methods and limitations. Run `python entropy/run_all.py` to refresh HTML after changing inputs.
