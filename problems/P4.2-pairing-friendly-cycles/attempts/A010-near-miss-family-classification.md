---
attempt: A010
status: promising
---
# A010 - Classify the surviving two-target-edge 3-cycle near-misses

## Idea

Rotate every near-miss so its two target-degree edges are consecutive, then
classify the resulting field path by degree pair, signed Hasse gaps, and exact
cyclotomic divisibilities. Separate parameter-uniform families from isolated
toy rows before increasing the prime bound.

## Plan

1. Canonicalize all 42 verified 22-bit near-miss rows at the missing edge.
2. Tabulate target-degree pairs, signed gaps, maximum fields, and repeated
   field triples.
3. Identify every equal-gap degree-(4,6) or degree-(6,4) path and prove its
   parameterization rather than inferring it from data.
4. Record exact closing degrees and isolate every row outside the proved
   class.
5. Decide from the residual ledger whether a 24-bit extension measures
   anything new.

## Predeclared outcome criteria

[CONJECTURE] Every near-miss first appearing above the 16-bit bound is an
orientation of the consecutive MNT triple already excluded by A009. A row
with maximum field at least \(2^{16}\) outside that class refutes the
prediction.

## Execution log

- [EMPIRICAL: all 42 two-target-edge near-misses below 2^22] Canonical
  rotation preserved every source row exactly once. Eight are consecutive
  MNT-chain orientations and 34 are residual rows
  (`data/classify_three_cycle_near_misses_n42_20260718.csv`).
- [PROVED] Every equal-signed-gap degree-(4,6) path is necessarily a
  consecutive MNT chain (`MNT_PATH_CLASSIFICATION.md`).
- [EMPIRICAL: fields at least 2^16 in the same ledger] Five MNT-chain rows and
  one residual row occur. The residual canonical path is
  \((483883,483481,482659)\), has target degrees (5,11), signed gaps
  \((-402,-822)\), and closing degree 483,882.
- [EMPIRICAL: residual ledger below 2^22] The other 33 residual rows all have
  maximum field at most 10,691. No other residual has target-degree pair
  (5,11).

## Outcome

The prediction was refuted by the unique degree-(5,11) high residual. The
repeated MNT structure is now proved rather than inferred, while the isolated
high residual makes a 24-bit extension informative: it can test whether that
degree pair begins a second family.
