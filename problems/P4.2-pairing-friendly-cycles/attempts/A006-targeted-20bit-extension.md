---
attempt: A006
status: promising
---
# A006 - Targeted 20-bit primary extension

## Idea

Avoid enumerating irrelevant directed triangles. Enumerate all Hasse edges,
retain exact-degree-3-through-12 edges, and join pairs of retained edges before
testing cycle closure.

## Plan

1. Implement the targeted 3-cycle enumerator with the coverage proof in
   `EXTENSION_20BIT.md`.
2. Compare every candidate row with the exhaustive enumerator below 16 bits
   and 18 bits.
3. Run the unchanged 2-cycle search and targeted 3-cycle search below 2^20.
4. Diff against the verified 18-bit ledgers and construct every new full hit.

## Predeclared outcome criteria

[CONJECTURE] Validation produces identical candidate rows at both prior bounds.
At 20 bits, only MNT-pattern 2-cycle hits are new and no 3-cycle candidate row
is new. Any validation mismatch or exceptional new row refutes the prediction.

## Execution log

- [EMPIRICAL: 16-bit and 18-bit primary spaces] The targeted 3-cycle candidate
  CSVs are row-for-row identical to the exhaustive CSVs. At 18 bits runtime
  fell from 88.28 seconds to the low single digits while preserving all 42
  rows.
- [EMPIRICAL: primes below 2^20, exact degrees 3 through 12] The 2-cycle
  search checked 3,363,845,253 unordered prime pairs and 8,242,847 Hasse-valid
  pairs. It found 47 hits, adding 13 MNT-pattern hits and no exceptional hit
  (`data/search_two_cycles_p5-1048575_k3-12_20260708_summary.json`).
- [EMPIRICAL: three distinct primes below 2^20, exact degrees 3 through 12]
  The targeted search checked 16,485,694 directed Hasse edges and 609 target
  edges. It found the same five full hits plus 40 two-of-three near-misses,
  adding three near-miss rows but no hit
  (`data/search_three_cycles_targeted_p5-1048575_k3-12_20260708_summary.json`).
- [EMPIRICAL: three new 20-bit near-misses] The missing exact degrees are
  483882, 2055, and 115320; none is a near-boundary degree-13 case.
- [EMPIRICAL: 13 new 20-bit 2-cycle hits] The first 20,000-trial construction
  run failed on one curve. After adding explicit twist-complement search and
  raising the declared cap to 100,000, all 26 new curves passed both point
  counters; the largest successful trial count was 21,825
  (`data/construct_hit_cycles_n13_s6207_20260708.csv`).

## Outcome

The full-hit prediction matched: only MNT-pattern 2-cycles were added and no
3-cycle hit appeared. The stronger no-new-candidate prediction failed because
three two-of-three near-misses appeared. The targeted algorithm and recovery
construction are validated.

