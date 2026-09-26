# Idea 1 — Semantic interpretation entropy

Run `python entropy/01_semantic_interpretation/run.py --horizon 6` from the repository root. Read [results.json](results.json) or open [index.html](index.html).

Each setup requirement has its own experimental candidate set. Exact bounded truth vectors group equivalent candidates before calculating Shannon entropy. The original/punctuation-alias pair shares probability 0.5; tighter-deadline and alternate-trigger meanings have probability 0.25 each. At six ticks, this gives 1.5 bits over meaning classes versus 2 bits over spellings. Original-only entropy is 0 bits. Priors are illustrative, not measured.

The HTML lets you vary class weights. All scientific assumptions, reproduction instructions, and limitations are in the [parent README](../README.md). Run `python entropy/run_all.py` to refresh HTML after changing inputs.
