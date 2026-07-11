---
attempt: A001
status: promising
---
# A001 - Explicit-unit quotient rho

## Idea

Use the explicit automorphisms on the $j=0$ and $j=1728$ families to walk on canonical unit orbits while tracking the corresponding coefficients of $P$ and $Q=[k]P$.

## Prior art

- [CITED] Wiener and Zuccherato (SAC 1998) and Duursma, Gaudry, and Morain (ASIACRYPT 1999) develop automorphism-class rho speedups.
- [CITED] Wang and Zhang (IACR ePrint 2011/008) document fruitless cycles in equivalence-class walks and cycle-handling strategies.

## Plan

1. Validate each explicit map and its finite orbit on known-answer curves.
2. Add a shared, callback-driven quotient-rho implementation to `lib/dlog.py`.
3. Validate recovered logs before measuring collision counts.
4. Measure the baseline and quotient with seeded, paired trials.

## Execution log

- [EMPIRICAL: eight curves, p=4057..261673] The explicit $D=-3$ and $D=-4$ maps passed two independent point counters, 32 seeded characteristic-equation checks per curve, and known-log recovery.
- [EMPIRICAL: same curves, 200 trials per size] The naive Floyd walk exposed severe zero-denominator fruitless cycles at the largest size.
- [PROVED] A collision-table variant retains the orbit walk and coefficient equations while detecting exact-state cycles immediately.

## Outcome

- [EMPIRICAL: 3,200 recovered DLPs; r=2053..262519] The collision-table ratios matched $\sqrt6$ and $2$ within every 95% interval; full results are in `data/measure_unit_rho_table_r20_b12-14-16-18_t200_s52022026_20260707_summary.csv`.
- [PROVED] The experiment establishes only a fixed unit-orbit factor in its tested model; it does not address non-unit CM endomorphisms or prove security.
