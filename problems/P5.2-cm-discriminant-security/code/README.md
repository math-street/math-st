# P5.2 code

## Files

- `cm_units.py` constructs paired $D=-3$ and $D=-4$ curves over one prime field, binds their explicit unit maps, and validates full orders, subgroup orders, eigenvalues, characteristic equations, and unit exponents.
- `measure_unit_rho.py` runs seeded paired baseline/quotient trials, writes raw and summary CSV files, computes paired-bootstrap confidence intervals, and stores log-log fits and residuals.
- `cm_nonunit.py` reconstructs the GLV discriminant-$-7$ norm-two endomorphism, validates its characteristic equation, and computes its scalar eigenvalue order on invariant prime-order subgroups.
- `measure_nonunit_orbits.py` sweeps toy sizes and records exact eigenvalue orders plus the cost of exhaustive orbit normalization.
- `tests/test_cm_units.py` contains known-family, independent-count, and known-log checks.
- `tests/test_measure_unit_rho.py` validates the statistics helpers against hand-computable values.

## Reproduce

```powershell
python problems/P5.2-cm-discriminant-security/code/measure_unit_rho.py --smoke --collision-table
python problems/P5.2-cm-discriminant-security/code/measure_unit_rho.py --bits 12,14,16,18 --trials 200 --seed 52022026 --partitions 20 --max-restarts 128 --bootstrap-resamples 2000 --collision-table
python problems/P5.2-cm-discriminant-security/code/measure_nonunit_orbits.py --smoke
python problems/P5.2-cm-discriminant-security/code/measure_nonunit_orbits.py --bits 10,12,14,16,18 --samples 16 --seed 72022026
```

- [EMPIRICAL: Windows 11, Python 3.13.4] The full collision-table command completed in 18.54 seconds and recovered all 3,200 DLPs.
- [EMPIRICAL: same environment] The naive Floyd dataset completed in 38.95 seconds; the failed local-doubling escape dataset completed in 136.63 seconds.
- [EMPIRICAL: Windows 11, Python 3.13.4] The full non-unit command completed in 2.96 seconds, validated five curves, and normalized 80 nonzero points.
- [PROVED] The collision-table mode stores visited states and therefore uses $O(\sqrt r)$ expected memory in the ideal-random-mapping model; it is intended to isolate collision-space size, not to claim a constant-memory implementation.

## Principal outputs

- `data/measure_unit_rho_table_r20_b12-14-16-18_t200_s52022026_20260707_{raw,summary,validation,residuals}.csv`
- `data/measure_unit_rho_table_r20_b12-14-16-18_t200_s52022026_20260707_fit.json`
- `data/measure_unit_rho_b12-14-16-18_t200_s52022026_20260702_{raw,summary,validation,residuals}.csv` (naive Floyd)
- `data/measure_unit_rho_escape_b12-14-16-18_t200_s52022026_20260707_{raw,summary,validation,residuals}.csv` (dead A002)
- `data/measure_nonunit_orbits_b10-12-14-16-18_n16_s72022026_20260711_{raw,summary,validation}.csv`
