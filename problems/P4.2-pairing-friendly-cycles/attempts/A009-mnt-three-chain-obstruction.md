---
attempt: A009
status: promising
---
# A009 - Rule out closure of the consecutive MNT 3-chain

## Idea

Reduce the closing base \(\pm4x\) by its quadratic relation and bound every
degree-at-most-12 power remainder by a linear function of \(x\).

## Plan

1. Derive and tabulate the recurrence through degree 12.
2. Prove a uniform non-divisibility bound for \(x\ge1026\).
3. Exhaust \(1\le x\le1025\), retaining every all-prime triple and computing
   both exact closing degrees.

## Predeclared outcome criteria

[CONJECTURE] No all-prime triple closes in either orientation with remaining
degree at most 12. A single finite hit refutes the class-level claim.

## Execution log

- [PROVED] Reducing the closing base modulo either outer prime gives
  (y^2\equiv2y-4). The resulting degree-12 remainder table has coefficients
  bounded by 1,024 and 4,096.
- [PROVED] For every (x\ge1026), the absolute closing remainder is smaller
  than the relevant outer prime and is nonzero, so neither closing exact
  degree is at most 12.
- [EMPIRICAL: deterministic enumeration of 1 <= x <= 1025] Four values make
  all three MNT polynomials prime: 3, 45, 480, and 987. Their two closing
  degree pairs are respectively (30,21), (445,78), (2055,115320), and
  (556386,1949325); none closes at degree at most 12
  (`data/analyze_mnt_three_chains_x1-1025_20260627.csv`).

## Outcome

The prediction matched. The proof and finite certificate in
`MNT_THREE_CHAIN_OBSTRUCTION.md` exclude the entire stated MNT 3-chain class
in both orientations.
