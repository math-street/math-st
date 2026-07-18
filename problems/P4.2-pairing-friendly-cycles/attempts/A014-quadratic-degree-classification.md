---
attempt: A014
status: promising
---
# A014 - Classify all 2-cycle degree pairs in {3,4,6}

## Idea

For \(p<q\), put \(c=q-p\). Each degree in {3,4,6} gives a quadratic
cyclotomic divisibility in \(c\). Hasse bounds restrict the two quotient
multipliers to \(m\le3\) and \(n\le6\), leaving a finite table unless the
quadratic coefficients cancel identically.

## Plan

1. Derive the multiplier equation for all nine ordered degree pairs.
2. Enumerate every bounded multiplier pair and every positive even integral
   root, retaining rejection reasons.
3. Treat the coefficient-cancelling cases symbolically.
4. Verify the resulting prime cases by exact multiplicative orders.

## Predeclared outcome criteria

[CONJECTURE] The only prime-order 2-cycles with both exact degrees in
{3,4,6} have ordered degree pair (6,4) or (4,6) and are the MNT families.
An exact finite row in any other pair refutes the prediction.

## Execution log

- [PROVED] Hasse bounds force the cyclotomic quotient multipliers into
  \(1\le m\le3\) and \(1\le n\le6\).
- [PROVED] Eliminating the fields gives one quadratic integer equation in the
  even gap \(c=q-p\).
- [EMPIRICAL: complete 9-by-3-by-6 multiplier box] Eleven identity or
  positive-root rows remain. Two are the MNT identities, one (6,6) identity
  fails parity, and eight finite roots fail parity, integrality, or the
  minimum-prime condition
  (`data/classify_quadratic_degree_pairs_k3-4-6_20260718.csv`).

## Outcome

[PROVED] The prediction matched. The full proof and finite certificate are in
`QUADRATIC_DEGREE_CLASSIFICATION.md`.
