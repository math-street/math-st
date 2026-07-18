---
attempt: A013
status: promising
---
# A013 - Extend the root-generated census to 28 bits

## Idea

Spend the speedup from A012 on one further factor-four interval and test
whether the newly exposed degree-(8,9) residual repeats or any full-hit pattern
changes.

## Predeclared outcome criteria

[CONJECTURE] No exceptional 2-cycle and no new full directed 3-cycle appears.
All new near-misses are retained and assigned exact closing degrees.

## Execution log

- [EMPIRICAL: primes below 2^28, exact degrees 3 through 12] The 2-cycle
  ledger has 333 hits and 3,714 one-sided near-misses. Exactly the original
  five hits are non-{(6,4),(4,6)}.
- [EMPIRICAL: same bound for directed 3-cycles] Five full hits and 61
  two-of-three near-misses occur.
- [EMPIRICAL: four new directed near-misses] They are the two orientations of
  the consecutive MNT chains at \(x=5967\) and \(x=7095\). The residual
  ledger remains unchanged at 35 rows.
- [EMPIRICAL: all 328 degree-{4,6} 2-cycle hits] Every row matches the proved
  MNT parameterization
  (`data/verify_mnt_parameterization_n328_20260627.csv`).

## Outcome

The prediction matched. No new exceptional 2-cycle, directed 3-cycle hit, or
non-MNT residual near-miss appeared.
