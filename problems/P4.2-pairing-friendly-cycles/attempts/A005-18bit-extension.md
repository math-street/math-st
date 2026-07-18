---
attempt: A005
status: promising
---
# A005 - Extend the primary census to 18-bit primes

## Idea

Raise only the prime bound to \(2^{18}\), keeping exact embedding degrees at
3 through 12. Compare the strict extension with the verified 16-bit ledgers.

## Plan

1. Run the full 2-cycle search below \(2^{18}\).
2. Run the full directed 3-cycle search below \(2^{18}\).
3. Diff full hits against the 16-bit ledgers by their directed field tuples.
4. Explicitly construct and count every new full hit.
5. Update the scoped negative thresholds and decide the next viable boundary.

## Predeclared outcome criteria

[CONJECTURE] New 2-cycle hits will all have degree pair (6,4) or (4,6), and no
new full directed 3-cycle will occur. Any new hit outside these cases refutes
the prediction.

## Execution log

- [EMPIRICAL: primes below 2^18, exact degrees 3 through 12] The 2-cycle
  census checked 264,442,503 unordered prime pairs and 1,281,301 Hasse-valid
  pairs. It found 34 hits: the original 26 plus eight new MNT-pattern hits
  (`data/search_two_cycles_p5-262143_k3-12_20260708_summary.json`).
- [EMPIRICAL: same range] None of the eight new 2-cycle hits has a degree pair
  outside {(6,4),(4,6)}.
- [EMPIRICAL: three distinct primes below 2^18, exact degrees 3 through 12]
  The directed search checked 2,562,602 Hasse edges and 78,388,968 directed
  triangles in 88.28 seconds. Its 42 candidate rows are byte-for-field
  identical to the 16-bit candidate set: five hits and 37 two-of-three
  near-misses (`data/search_three_cycles_p5-262143_k3-12_20260708_summary.json`).
- [EMPIRICAL: all 34 extended 2-cycle hits] All 68 explicit curves passed BSGS
  and direct equation enumeration, with zero order mismatches
  (`data/construct_hit_cycles_n34_s5205_20260708.csv`).

## Outcome

The prediction matched. The larger range added eight MNT-pattern 2-cycles, no
exceptional 2-cycle, and no 3-cycle candidate row of any kind.

