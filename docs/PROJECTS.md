# Project definitions and coverage

`projects/catalog.json` records FRETish inputs, project identity, rationale, assumptions, signal dictionaries, independent checker predicates and complete compiler semantics. Import JSON excludes checker metadata.

## Door product and five decision workflows

The source intent is a hinged room-door mechanism usable with one hand without undue effort. The illustrative target is binary package **1011**:

| Field | 0 | 1 | Selected |
|---|---|---|---|
| A: scope | 8–12 years | 6–12 years | 1 |
| B: fixture | P0 | P1 | 0 |
| C: force target | 15 N | 10 N | 1 |
| D: operation | latch only | full opening/closing | 1 |

These are study inputs, not standards. The eight clauses decompose the available intent. A Boolean input such as `fixture_approved` is a claim requiring external evidence.

Methods 1–5 observe steps 0, 11, 22, 33, 44, 55. Ten symbolic exploration steps separate gates. Positive support counts are:

| Method | L1 | L2 | L3 | L4 | L5 | L6 |
|---|---:|---:|---:|---:|---:|---:|
| Sequential | 16 | 16 | 8 | 4 | 2 | 1 |
| Parallel | 16 | 16 | 4 | 4 | 2 | 1 |
| Constraint propagation | 16 | 16 | 8 | 4 | 2 | 1 |
| Evidence updates | 16 | 16 | 16 | 16 | 16 | 1 |
| Prototype elimination | 16 | 12 | 8 | 4 | 2 | 1 |

The existing generator supplies weights as well as counts. FRET checks selected snapshot properties; these clauses do not specify or prove the full probability-update algorithm. Identical counts can hide different weights and candidate identities.

Each method has a final commitment to package 11 (binary 1011), plus an acceptance guard requiring four distinct, current, matching, passing records. Selection and acceptance are distinct.

## Truss

Available intent: 1000 kgf vertically at 2 m from a wall; fixed-section solid circular steel bars of 1 m and sqrt(2) m; available grid nodes; yielding/buckling; displacement strictly below 2 cm; minimum mass.

Project 02 selects total displacement magnitude. Project 03 is the vertical-only alternative, containing only the differing requirement. It is not a complete standalone structural specification. Choose the interpretation before combining it with shared constraints.

`enumerated_min_mass_kg` is an independent minimum over a declared finite feasible set. The equality clause is a contract on a certificate, not an optimizer or global-optimality proof. Original geometry is missing.

## Request/response

`RESP-EDGE` reproduces the tutorial's `when`; `RESP-LEVEL` reproduces `whenever`. They are alternatives for comparison, not a declaration that both are stakeholder-approved. Requests are Boolean signals; correlation IDs, queues and concurrent responses are out of scope.

## HTTP HEAD

The existing stable-resource HTTP/1.1 experiment implements the scoped RFC 9110 conditions. `HTTP-01` checks no raw content; `HTTP-02` checks a present Content-Length against GET. Header absence is permitted. Raw sockets avoid clients hiding an illegal HEAD body.

## Research context

CA rules, observer resolutions and research plans are study choices rather than additional product requirements. Their source lineage is preserved under `research/` without inventing FRET behavior for each.
