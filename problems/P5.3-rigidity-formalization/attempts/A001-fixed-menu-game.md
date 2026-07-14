---
attempt: A001
status: complete
---
# A001 — Fixed-menu selective-generation game

## Idea

Model unexplained designer freedom as a finite, precommitted menu of generator
executions. The designer may screen the menu using a hidden weak predicate and
publish any safe weak result. Count distinct screenable candidate outcomes,
not the length of the prose specification.

## Prior art

[CITED] The audited standards and construction sources are recorded under
`refs/`. They describe several parameter-generation mechanisms, but none
provides this exact fixed-menu probability game.

## Plan

1. Fix the curve universe, reference probability kernel, safety predicate,
   weak-set density bound, and menu before fresh randomness is sampled.
2. Prove a union bound for arbitrary dependence between menu entries.
3. Identify equality cases and counterexamples when quantifiers are reordered.
4. Separate observable replay rigidity from unobservable historical provenance.

## Execution log

The accounting contract, game, theorem, tightness construction, quantifier
failures, and minimal generator are written in `DEFINITIONS.md`. The audit in
`AUDIT.md` exposed a distinction between reproducible constants and
identifiable provenance menus.

## Outcome

[PROVED] The union bound is complete under explicit source-domination and
quantifier hypotheses. [CITED] Three standards admit numeric conditional
caps under A256; secp256k1 and BLS12-381 do not expose finite source menus in
the audited documents. [PROVED] A003 closes the apparent provenance gap with a
non-identifiability theorem and a sufficient certificate criterion rather than
an unsupported numerical estimate.
