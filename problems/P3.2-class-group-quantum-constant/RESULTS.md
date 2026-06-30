# Results

## SG-01 — explicit toy action

- [EMPIRICAL: (p=59), degrees (3,5)] Reduced-form enumeration gives (h(-236)=9); the explicit Vélu orbit has 9 prime-field isomorphism classes and its generated permutation group is abelian and regular.
- [EMPIRICAL: (p=419), degrees (3,5,7)] Reduced-form enumeration gives (h(-1676)=27); the explicit Vélu orbit has 27 prime-field isomorphism classes and its generated permutation group is abelian and regular.
- [PROVED] For either serialized transition table, `regular=true` means the computed group is transitive and the base-state stabilizer contains only the identity, by the checks in `verify_toy_action.py`.

## SG-02/03 — one specified sieve schedule

- [EMPIRICAL: (N=2^n), (24\le n\le96), 10 sizes, 100 trials per size, seed 20260722] The fixed-batch low-bit-collision simulator produced 1,000 query-count and combination-count observations in `data/simulate_sieve_n24-96_seed20260722_20260630.csv`.
- [EMPIRICAL: same range and trials, 2,000 within-size bootstrap replicates] Fitting `ln Q = c sqrt(ln N) + d ln(ln N) + k` gives (c=2.68677) with trial-bootstrap 95% CI ([2.65454,2.71923]), (d=-0.93996), (k=4.85231), and log-cost residual RMSE (0.36454).
- [EMPIRICAL: same ten geometric means] The square-root-log-plus-log-log model has in-sample RMSE 0.3645, compared with 0.3667 for square-root-log alone, 0.4485 for a linear-log model, and 0.4988 for a log-log model.
- [PROVED] The reported CI quantifies seeded occupancy/measurement variation only and excludes schedule discretization, block-width rounding, alternative sieve designs, and extrapolation error; those effects are absent from the resampling procedure.
- [PROVED] The fitted (c) belongs to this simplified fixed-batch schedule and is not a new constant for Kuperberg's collimation sieve or for CSIDH as a whole.

## SG-04/05/06 — calculator and sensitivity

- [PROVED] Every logical-operation, architecture, QRACM, and phenomenological surface-code number consumed by `calculate_cost` is serialized under `assumptions` in its output.
- [EMPIRICAL: illustrative (n=64) configuration on 2026-06-30] The calculator reports 27.477 abstract query bits, distance 45, 90,679,500 physical qubits, and (1.05097\times10^{13}) seconds; none of these physical values is calibrated to a published CSIDH oracle.
- [EMPIRICAL: configured one-at-a-time ranges on 2026-06-30] Parallel workers have the largest absolute effect on physical qubit-seconds over the deliberately broad supplied endpoints (1\) to (1024), moving the metric by 5.350 bits; oracle logical depth ranks second at 3.510 bits.
- [PROVED] This ranking is conditional on the endpoint ranges and is not an intrinsic global ordering of hardware importance; the sensitivity method varies one named parameter at a time.
- [EMPIRICAL: published logical fixtures on 2026-06-30] The calculator reproduces the (2^{71.6}) Bonnetain–Schrottenloher row and the rounded (2^{56}) Peikert optimistic endpoint exactly in base-two logical T-gate exponent.

## SG-07 — query lower bound

- [CONDITIONAL: independent standard phase-state query interface] The dimension proof in `LOWER_BOUND.md` gives (m\ge\log_2N+\log_2\varepsilon) queries for success probability `epsilon`.
- [CITED] This logarithmic scale matches the dihedral hidden-subgroup-state threshold of Bacon, Childs, and van Dam (2006) and the known logarithmic-query/exponential-postprocessing regime summarized by Remaud, Schrottenloher, and Tillich (2022).
- [PROVED] The unrestricted structured-action-oracle lower bound remains open in this repository because the proved query interface is weaker and no interface-preserving reduction has been supplied.

## Bottom line

- [PROVED] **Overall outcome: FAILED.** Neither formal task was completed: the physical constant remains uncalibrated for the full algorithm, and the lower bound does not cover an unrestricted coherent structured-action oracle.
- [PROVED] The formal request for a unique physically meaningful constant is not solved: the experiment determines a finite-range constant only for one named combinatorial schedule, while the physical layer remains parameterized.
- [PROVED] The retained partial artifacts are explicit toy actions, serialized sieve data and fitted terms, a named cost calculator, two logical endpoint reproductions, sensitivity ranking, and a conditional query lower bound with an unresolved interface gap.
- [EMPIRICAL: final validation on 2026-06-30] The repository passed 63 shared tests, 10 P3.2 tests, all five script smoke modes, bytecode compilation, JSON parsing, and the principal CSV row/schema audit.
