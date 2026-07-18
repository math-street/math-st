---
attempt: A004
status: promising
---
# A004 - Raise the embedding-degree ceiling to 18

## Idea

Keep every prime, Hasse, ordinarity, and cycle condition fixed, but replace
\(K=\{3,\ldots,12\}\) by \(K=\{3,\ldots,18\}\). Run both the length-2 and
length-3 searches so the change has exactly one axis.

## Prior art

[CITED] Belles-Munoz--Jimenez Urroz--Silva 2022 study partner degrees at least
through 22 for curves drawn from the known polynomial families. A004 instead
keeps an arbitrary bounded prime census and uses 18 only as a controlled
extension of the primary local ceiling.

## Plan

1. Re-run the unchanged 2-cycle enumerator with `--max-degree 18`.
2. Re-run the unchanged 3-cycle enumerator with `--max-degree 18`.
3. Compare hit counts and largest field primes with the degree-12 baseline.
4. Explicitly construct and independently count every newly admitted hit.

## Predeclared outcome criteria

[CONJECTURE] At least one degree-12 near-miss will become a full hit when the
ceiling is raised to 18. This is refuted if both hit ledgers are unchanged.

## Execution log

- [EMPIRICAL: 5 <= p_i < 65536, exact degrees 3 through 18] The 2-cycle hit
  count increased from 26 to 36; the directed 3-cycle hit count increased from
  5 to 12 (`data/search_two_cycles_p5-65535_k3-18_20260708_summary.json`,
  `data/search_three_cycles_p5-65535_k3-18_20260708_summary.json`).
- [EMPIRICAL: all relaxed hits] Both exact point counters verified all 72
  2-cycle equations and all 36 3-cycle equations
  (`data/construct_hit_cycles_n36_s4502_20260708.csv`,
  `data/construct_three_cycle_hits_n12_s4503_20260708.csv`).

## Outcome

The prediction matched. Raising only the embedding-degree ceiling admits ten
additional 2-cycles and seven additional directed 3-cycles, but all new
exceptions remain below fields 272 and 674, respectively.
