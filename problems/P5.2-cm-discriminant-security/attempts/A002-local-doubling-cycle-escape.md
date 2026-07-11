---
attempt: A002
status: dead
---
# A002 - Double a detected fruitless-cycle collision

## Idea

When Floyd detects a zero-denominator collision, double that collision point,
canonicalize it, and continue under the same adding table instead of restarting.

## Prior art

- [CITED] Wang and Zhang (IACR ePrint 2011/008) analyze deterministic cycle detection and doubling from a carefully selected escape point for the negation map.
- [CITED] Bos, Kleinjung, and Lenstra (ANTS 2010) warn that earlier countermeasures can enter recurring cycles.

## Plan

Count the doubling as an online transition and compare the complete recovery
cost with the baseline on the preregistered curves and seeds.

## Execution log

- [EMPIRICAL: 3,200 recovered DLPs; r=2053..262519] Every logarithm was eventually recovered, but the largest $D=-3$ and $D=-4$ cases averaged 172.1 and 211.0 escape doublings and 36,878 and 32,470 total transitions.
- [EMPIRICAL: same range] Individual trials reached more than 1,500 repeated escapes.

## Outcome

Dead. Data: `data/measure_unit_rho_escape_b12-14-16-18_t200_s52022026_20260707_raw.csv`.

## Post-mortem

**Why it failed:** [PROVED] The chosen escape rule was history-local rather than a globally specified iteration rule with a canonical escape point. Doubling is a permutation on the odd prime-order subgroup, so it does not by itself prevent the escaped state from entering the same or another fruitless component; the data show that recurrence dominates.

**What transfers:** [PROVED] Zero-denominator collisions must be counted, and any claimed orbit speedup must specify its cycle-handling and memory model. The collision-table variant gives a clean toy baseline by detecting exact-state recurrence directly.

**Would it work under different assumptions?** [CITED] Literature algorithms using block minima, distinguished points, or branchless negation-map formulations can make the overhead small for order-two negation (Bos-Kleinjung-Lenstra 2010; Bernstein-Lange-Schwabe 2011; Wang-Zhang 2011). Extending those exact constructions to the order-four and order-six unit actions was not attempted here.
