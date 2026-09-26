# Request/response — edge versus sustained trigger

## Sources
- Task Gereksinim anlama görselleştirmesi, 24 September 2026; NASA-FRET/prepare-example.cjs and tutorial/verified-semantics.json.

## Assumptions and unresolved inputs
- The original phrase “short time” is ambiguous. The three-tick bound is the existing tutorial’s example choice, not an elicited service-level agreement.
- request/response meaning (send vs receive; acknowledgement vs completed result) and load conditions remain open.
- when and whenever are alternative interpretations shown side by side. Each request is a Boolean event; concurrent request identity/matching is outside this toy abstraction.
- FRET counts discrete timepoints and does not convert units. The finite semantics permits a trace to end before the deadline without a response. Independent examples report that situation as INCOMPLETE.

## Signals
- `request`: bool: request signal
- `response`: bool: response signal
- `tick`: integer: abstract discrete timepoint; no physical duration assigned

### RESP-EDGE

when request the ResponseSystem shall within 3 ticks satisfy response

Existing tutorial: first true point and false-to-true edges trigger obligations.

FRET infinite-trace formula:

```text
((G (((! request) & (X request)) -> (X (F[0,3] response)))) & (request -> (F[0,3] response)))
```

### RESP-LEVEL

whenever request the ResponseSystem shall within 3 ticks satisfy response

Existing tutorial: every true request sample triggers an obligation.

FRET infinite-trace formula:

```text
(G (request -> (F[0,3] response)))
```
