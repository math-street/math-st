---
attempt: A015
status: promising
---
# A015 - Classify mixed quadratic/quartic degree pairs

## Idea

When one exact degree lies in {3,4,6} and the other in {5,8,10,12}, the
quadratic side has a Hasse-bounded multiplier. Substituting that field into the
quartic divisibility leaves a linear polynomial remainder modulo a monic
quadratic. A coefficient bound then reduces every case to finitely many even
gaps.

## Predeclared outcome criteria

[CONJECTURE] Across all 24 ordered mixed degree pairs, the only exact
prime-order 2-cycle is the fields (7,11) with degree pair (10,3). Any other
exact row refutes the prediction.

## Execution log

- [PROVED] The bounded quadratic side produces 108 multiplier cases. In every
  case the quartic divisibility reduces to a linear remainder modulo a monic
  quadratic.
- [PROVED] The coefficient bound makes every nonidentity case finite; the
  largest required even-gap bound is 2,649.
- [EMPIRICAL: all 108 cases and every even gap through its proved bound] The
  certificate has 116 rows, no identity remainder, and one exact cycle:
  fields (7,11) with degree pair (10,3)
  (`data/classify_mixed_degree_pairs_20260718.csv`).

## Outcome

[PROVED] The prediction matched. The global proof is in
`MIXED_DEGREE_CLASSIFICATION.md`.
