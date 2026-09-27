# Step-by-step entropy class notes

Read [FRET_Entropy_Class_Notes.pdf](FRET_Entropy_Class_Notes.pdf), a 15-page LaTeX document with 14 lessons and worked solutions.

The notes explain the setup requirements, finite-trace boundary semantics, Shannon entropy, candidate grouping, behavioral freedom, hand derivations of the 3,848/3,784 trace counts, Bayesian clarification updates, and the 1/0.811278-bit question gains. They include reproduction commands, limitations, exercises, and references.

The analysis baseline is commit `6443ce8`; the numerical results are those of the six-tick experiment. No new stakeholder evidence or inferred engineering acceptance is introduced.

## Build and check

From this directory, with a LaTeX distribution installed:

```sh
pdflatex -interaction=nonstopmode -halt-on-error FRET_Entropy_Class_Notes.tex
python check_notes.py
```

The check script needs `pypdf` and a repository checkout with the existing entropy result files. It checks the hand-derived failure intersections independently, compares the headline values with saved outputs, checks PDF text/page count, and rejects LaTeX overflow or missing-character warnings. It does not replace visual review. The final 15 rendered pages were visually inspected before delivery; the source compiled without overfull boxes or missing-character warnings. PDF byte hashes can differ between builds because LaTeX embeds timestamps.

The editable source is [FRET_Entropy_Class_Notes.tex](FRET_Entropy_Class_Notes.tex). Numerical validation is recorded in [notes_validation.json](notes_validation.json). Authorship and research scope are stated in the PDF.
