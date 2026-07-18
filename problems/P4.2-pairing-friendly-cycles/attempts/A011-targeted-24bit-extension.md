---
attempt: A011
status: promising
---
# A011 - Targeted 24-bit primary extension

## Idea

Use the already validated candidate-complete algorithms to test whether the
unique high residual from A010 repeats and whether any full-hit pattern changes
over the next factor-four prime interval.

## Plan

1. Freeze the unchanged space in `EXTENSION_24BIT.md`.
2. Run both targeted searches below \(2^{24}\).
3. Diff every hit and near-miss against the 22-bit ledgers.
4. Canonicalize all new near-misses and compute their exact closing degrees.
5. Explicitly construct and independently count every new full hit.

## Predeclared outcome criteria

[CONJECTURE] New 2-cycle hits are all MNT-pattern, no new directed 3-cycle hit
appears, and the degree-(5,11) residual either remains isolated or is exposed
as a repeated class by a new row. Any exceptional full hit refutes the primary
prediction.

## Execution log

- [EMPIRICAL: primes below 2^24, exact degrees 3 through 12] The 2-cycle
  search found 130 hits and 1,364 one-sided near-misses. Only the original five
  hits are non-{(6,4),(4,6)}.
- [EMPIRICAL: same bound for directed 3-cycles] Five full hits and 48
  two-of-three near-misses occur. All six new near-misses are MNT-chain
  orientations at \(x=1215,1365,1368\).
- [EMPIRICAL: all 54 newly appearing 2-cycle hits] All 108 explicit equations
  have matching BSGS orders and independent prime-point Hasse certificates
  (`data/construct_hit_cycles_n54_s8207_20260708.csv`).

## Outcome

The full-hit prediction matched. The degree-(5,11) residual did not repeat,
and the non-MNT residual ledger stayed at 34 rows.
