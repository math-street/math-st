# Handoff -- P4.1 -- complete after session 3

## State in five lines

[EMPIRICAL: published fixtures and checked-in samples] The fixed finite model reproduces BN and BLS12 within 0.04 cost bits and KSS16 within 0.13 bits under the authors' public coefficient-bound convention.
[PROVED] BN, BLS12, BLS24, and KSS16 family evaluators, exact nested-resultant samplers, and least-embedding-degree checks are implemented.
[PROVED] The search returns the rho optimum inside the stated four-family leading-term model at 128, 192, and 256 bits.
[PROVED] No KSS16 prime pair exists below the scaffold's `p<2^60` ceiling.
[EMPIRICAL: BLS24 audit] Printed `A=9` settings leave a 1.92-bit cost discrepancy; a preregistered sampling-bound-10 sensitivity reproduces both printed norms within one bit and leaves only non-blocking historical-setting ambiguity Q027.

## What is established

- [PROVED] The 80-decimal-digit interval Dickman evaluator is validated through `u=16` and matches the printed BN, BLS12, KSS16, and BLS24 smoothness probabilities used by the finite rows.
- [EMPIRICAL: 1,024 BLS12 samples] Exact nested resultants give mean bit lengths 791.083/584.756 and total cost 131.789 bits versus 131.8 published.
- [EMPIRICAL: 512 samples per recorded convention] BN costs are within 0.04 bits; the KSS16 public-code-bound run is within 0.13 bits.
- [EMPIRICAL: every seed -10,000 through 10,000, `p<2^60`] Accepted counts are 273/24/5/0 for BN/BLS12/BLS24/KSS16.
- [PROVED] BN uniquely minimizes the implemented rho objective for all three targets and three sensitivity scenarios.

## Reproducibility finding

[CITED] The paper states coefficient draws on `[-A,A]`, while the authors' public Python source calls inclusive `randint(-A,A+1)` and therefore draws on `[-A,A+1]`.

[EMPIRICAL] The checked-in BLS24 `A=9` runs produce costs 201.255 and 201.803 under the two conventions versus 203.72 printed. A separate seeded `A=10` draw-bound sensitivity produces norms 1295.867/1461.000 and cost 203.171. This strongly supports an internal-rounding explanation but does not prove which setting the unavailable historical execution used.

## Invariants

- Experimental curve generation stays under the scaffold's toy ceiling.
- Every modelling and coefficient-domain choice remains named in data and reports.
- Calibration, validation, and sensitivity experiments are not conflated.
- Production target rows never claim concrete prime seeds.

## Files that matter

`lib/tnfs_cost.py`, `lib/curves.py`, `code/search_families.py`, `code/sample_bls12_norms.py`, `code/sample_family_norms.py`, `code/compare_norm_regressions.py`, `code/certify_kss16_ceiling.py`, `RESULTS.md`, and the dated artifacts in `data/`.

## Replacement note

[PROVED] P4.1 needs no continuation for its declared deliverable. A follow-on should explicitly choose one of: recover the historical BLS24 execution setting (Q027), expand the family taxonomy, replace the cost model, or generate concrete production seeds.
