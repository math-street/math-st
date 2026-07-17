---
attempt: A006
status: folded-into-A007
---
# A006 — Consolidated prime-field failure pattern

## Evidence being consolidated

- [EMPIRICAL: p=65519 through 1048571] Candidate A has the intended
  square-root-scale density but is indistinguishable from random under generic
  decomposition search.
- [EMPIRICAL: same curves] Candidate B's symmetric rational-height bounds
  select essentially the entire curve.
- [PROVED] Candidate C's rational-map subclass is constant, while a distinct
  low-degree auxiliary plane curve is degree-bounded and too sparse.
- [EMPIRICAL: same curves] Candidate D's integral-lift proxy is empty or nearly
  empty; the full canonical-height predicate remains unspecified.
- [EMPIRICAL: q=5,7,11] The extension-field positive control recovers planted
  logarithms, so the shared relation machinery is operational.

## Pattern

[CONJECTURE] A one-coordinate prime-field predicate with a short description
falls into one of three regimes: it is too sparse for constant-term
decomposition, it has the desired density but leaves decomposition looking
generic, or it becomes so permissive that the factor base is essentially the
whole curve. A predicate that yields a small base together with a
polylogarithmic decomposition algorithm on a growing prime-field family would
refute this trichotomy.

[CONJECTURE] The missing ingredient is not point count but an effective
dimension drop in the decomposition equations. The extension-field subfield
predicate supplies such a drop through base-field coordinates; the interval,
rational-height, plane-intersection, and integral-lift predicates tested here
do not. A prime-field predicate whose summation-polynomial system admits a
proved polylogarithmic solver would refute this explanation.

## Outcome

[PROVED] None of A001, A003, A004, or A005 supplies a pair
$(\mathcal F,\mathcal D)$ meeting all three formal conditions. A002 is only an
extension-field correctness control and is outside the target regime.

[EMPIRICAL: all recorded prime-field experiments] No tested prime-field
candidate improves both factor-base size and finder work over the random
baseline.

[PROVED] A007 supersedes this empirical trichotomy for the formal statement:
under standard L-notation, any fixed-$m$ factor base satisfying condition (1)
is information-theoretically too small to satisfy condition (3), regardless
of its predicate or finder.
