---
attempt: A001
status: dead
---
# A001 — Derive a checklist from published attack hypotheses

## Idea

Normalize each attack into (1) transcript observables, (2) arithmetic
inequalities, (3) an efficiently computable auxiliary witness, and (4) a
recovery algorithm. Use those normalized records to build a conservative
three-valued decision procedure.

## Prior art

[CITED] Castryck--Decru 2023 and Maino--Martindale 2023 give surface templates;
Robert 2023 gives the dimension-8 template and direct-recovery boundary.

## Plan

1. Extract the exact inputs and success hypotheses of the three 2022 attacks.
2. Separate theorem requirements from implementation conveniences.
3. Define the parameter record and classify real protocols.
4. Stress-test with synthetic transcripts near each boundary.
5. Search for counterexamples to any claim of necessity.

## Execution log

Workspace initialized on 2026-06-30.

Primary-source hypotheses were normalized in `CHECKLIST.md` Sections 1--2.
Five real protocols and eight synthetic boundary profiles were encoded and
tested in `code/`.

The necessity audit isolated Q011: no completeness theorem covers arbitrary
dimension, polarization, derived leakage, or future recovery algorithms.

## Outcome

[PROVED] Promising partial result: the checklist is necessary and sufficient
for invocation of the three encoded published templates, relative to supplied
profile and auxiliary-witness facts.

[PROVED] The original universal criterion is not solved; the procedure returns
`WITNESS_DEPENDENT` or `NO_PUBLISHED_ROUTE` without claiming security outside
its model.

## Post-mortem

**Why it failed:** [PROVED] Normalizing a finite list of published templates
can prove an invocation criterion for that list, but it cannot prove necessity
against arbitrary higher-dimensional embeddings, derived leakage, or future
recovery algorithms. The missing completeness theorem is Q011.

**What transfers:** [PROVED] The sourced requirement table, protocol matrix,
scoped decision tree, and regression fixtures remain valid as a conservative
published-template audit.

**Would it work under different assumptions?** [PROVED] Yes: after restricting
the quantifier to R8, K2-CD, and K2-MM, the checklist is sound and complete
relative to a supplied profile and construction witness.
