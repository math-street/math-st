---
attempt: A002
status: promising
---
# A002 - Exhaustive bounded 2-cycle isogeny search

## Idea

Enumerate prime field/order pairs directly. This avoids making CM class-number
or curve-model choices before the arithmetic cycle and embedding constraints
have been tested.

## Prior art

[CITED] Chiesa--Chua--Weidner 2019 classify MNT-only cycles and rule out three
specific embedding-degree pairs, but do not exhaust the bounded prime space in
`SEARCH_SPACE.md`.

## Plan

1. Sieve all primes below \(2^{16}\).
2. Enumerate every pair in the Hasse window and check both traces.
3. Compute exact embedding degrees up to 12.
4. Record every pair for which at least one degree is in 3 through 12.
5. Validate the enumeration against the published pairs \((5,7)\) and
   \((37,43)\), both with degree pair \((6,4)\).

## Predeclared outcome criteria

[CONJECTURE] The search will reproduce the known \((6,4)\) pairs and find no
hit with a different degree pair. This is refuted by any row labeled `hit`
whose degree pair differs from \((6,4)\), or by failure to recover
\((37,43,6,4)\).

## Execution log

- [EMPIRICAL: 5 <= p < q < 128, 3 <= k_i <= 12] The smoke search already
  refuted the predeclared prediction by finding seven non-(6,4) arithmetic
  hits (`data/search_two_cycles_p5-127_k3-12_20260708_summary.json`).
- [EMPIRICAL: 5 <= p < q < 65536, 3 <= k_i <= 12] The full enumeration checked
  204,074 Hasse-valid pairs and returned 26 full arithmetic hits plus 219
  one-sided near-misses. Thirteen full hits have degree pair (6,4), eight have
  (4,6), and five have other degree pairs
  (`data/search_two_cycles_p5-65535_k3-12_20260708_summary.json`).

### Explicit-construction follow-up declared before running

[CONJECTURE] Seeded Hasse/BSGS model search will find an explicit curve for
both sides of every arithmetic hit within 20,000 coefficient trials per curve;
direct equation enumeration will independently confirm every target order.

- [EMPIRICAL: all 26 full arithmetic hits] Seeded coefficient search
  instantiated all 52 curves. Both exact counters returned the target order
  on every curve; the largest construction took 2,411 coefficient trials
  (`data/construct_hit_cycles_n26_s4203_20260708.csv`).
- [EMPIRICAL: 5 <= p < q < 65536, 3 <= k_i <= 12] Exactly five hits have
  degree pairs outside {(6,4),(4,6)}: (10,3), (12,10), (9,8), (7,11), and
  (10,11). Their larger field primes are 11, 13, 19, 29, and 31.
- [CITED] The (10,3) arithmetic pair over fields 7 and 11 also appears as the
  exceptional MNT3 instance x=1 in Belles-Munoz--Jimenez Urroz--Silva,
  IACR ePrint 2022/1662, Table 2
  (`refs/belles-munoz-jimenez-urroz-silva2022.md`).

## Outcome

The arithmetic prediction was false, while the follow-up construction
prediction matched. The full candidate ledger, including all 219 one-sided
near-misses, is reproducible and all 26 full hits have independently counted
explicit models.

