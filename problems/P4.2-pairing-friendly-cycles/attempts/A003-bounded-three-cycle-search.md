---
attempt: A003
status: promising
---
# A003 - Exhaustive bounded length-3 search

## Idea

Treat Hasse-valid prime transitions as a directed graph. Directed triangles are
exactly the arithmetic parameter triples for prime-order 3-cycles.

## Prior art

[CITED] Chiesa--Chua--Weidner 2019 state that pairing-friendly cycles of
arbitrary length are not known and show that MNT-only cycles have length 2 or
4. This does not exclude arbitrary length-3 cycles outside MNT families.

## Plan

1. Build every Hasse-valid directed prime transition below \(2^{16}\).
2. Enumerate directed triangles once up to cyclic rotation.
3. Compute the three exact embedding degrees through 12.
4. Persist all two-of-three near-misses and every full hit.
5. Construct and independently count all full hits, if any.

## Predeclared outcome criteria

[CONJECTURE] No full hit will occur. One directed triple with all three exact
degrees in 3 through 12 refutes the prediction.

## Execution log

- [EMPIRICAL: 5 <= p_i < 128, 3 <= k_i <= 12] The smoke run found five full
  hits and refuted the no-hit prediction
  (`data/search_three_cycles_p5-127_k3-12_20260708_summary.json`).
- [EMPIRICAL: 5 <= p_i < 65536, 3 <= k_i <= 12] The full search enumerated
  6,922,890 directed 3-cycles, finding the same five full hits and 37
  two-of-three near-misses
  (`data/search_three_cycles_p5-65535_k3-12_20260708_summary.json`).

### Explicit-construction follow-up declared before running

[CONJECTURE] Seeded model search will instantiate all 15 curves within 20,000
coefficient trials each, after which BSGS and direct enumeration will agree on
all target orders.

- [EMPIRICAL: all five full hits] All 15 explicit curves were found within 98
  coefficient trials each. Both exact counters matched every target order
  (`data/construct_three_cycle_hits_n5_s4303_20260708.csv`).

## Outcome

The no-hit prediction was false, while the construction prediction matched.
The result proves toy existence in the covered range and a negative result
above field 43 within that same range and degree ceiling; it does not produce a
scalable family.
