---
attempt: A007
status: promising
---
# A007 - Targeted 22-bit primary extension

## Idea

Use candidate-complete target-edge algorithms to push the fixed degree-12
space two more bits without materializing irrelevant discriminants or
triangles.

## Plan

1. Validate targeted 2-cycle rows against 16-, 18-, and 20-bit ledgers.
2. Run both targeted searches below 2^22.
3. Diff full hits and near-misses against 20 bits.
4. Compute exact missing degrees for all new near-misses.
5. Explicitly construct and count every newly appearing full hit.

## Predeclared outcome criteria

[CONJECTURE] Only MNT-pattern 2-cycle hits will be added, and no directed
3-cycle hit will be added. Any exceptional full hit refutes the prediction.

## Execution log

- [EMPIRICAL: primes below 2^22, exact degrees 3 through 12] The targeted
  2-cycle search checked 43,791,573,540 unordered pairs and 54,092,289
  Hasse-valid pairs. It retained 895 candidate rows: 76 hits and 819
  one-sided near-misses
  (`data/search_two_cycles_targeted_p5-4194303_k3-12_20260708_summary.json`).
- [EMPIRICAL: same range] The 76 hits comprise 40 degree-(6,4), 31
  degree-(4,6), and the five already known tiny exceptional pairs. Thus all
  29 hits newly appearing above the 20-bit bound have an MNT degree pattern.
- [EMPIRICAL: all 29 new 22-bit hits] All 58 explicit curves passed BSGS and
  direct equation enumeration with zero order mismatches. The largest field
  was 4,137,157 and the largest successful coefficient-trial count was 43,462
  (`data/construct_hit_cycles_n29_s7207_20260708.csv`).
- [EMPIRICAL: three distinct primes below 2^22, exact degrees 3 through 12]
  The target-edge join checked 108,184,578 directed Hasse edges and retained
  971 target edges. It found five hits and 42 two-of-three near-misses
  (`data/search_three_cycles_targeted_p5-4194303_k3-12_20260708_summary.json`).
- [EMPIRICAL: two new 22-bit near-misses] Both use the fields 3,894,703,
  3,896,677, and 3,898,651. Their missing exact degrees are 556,386 and
  1,949,325 (`data/analyze_three_cycle_near_misses_min1048576_n2_20260718.csv`).

## Outcome

The prediction matched. Every new 2-cycle hit has degree pair (6,4) or (4,6),
and no new directed 3-cycle hit appeared. Two new near-misses appeared, as the
predeclared criterion allowed.
