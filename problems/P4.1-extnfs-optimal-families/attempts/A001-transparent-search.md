---
attempt: A001
status: complete
---
# A001 — Transparent exTNFS model and bounded family search

## Idea

Implement family polynomials and exact embedding-degree checks independently of a serializable cost-model object, then optimize only after the model reproduces a declared anchor.

## Prior art

[CITED] Kim and Barbulescu introduce exTNFS and derive improved medium-prime asymptotics, including special-form variants relevant to polynomial pairing families (CRYPTO 2016, LNCS 9814, 543–571, doi:10.1007/978-3-662-53018-4_20).

## Plan

1. Verify the literature and write down a complete cost equation.
2. Add known-answer tests before any parameter sweep.
3. Sweep bounded toy seeds and store deterministic records.
4. Generate separately labelled extrapolation tables and sensitivity scenarios.

## Execution log

- Initialized before baseline checks.
- [EMPIRICAL: final verification suite] Implemented and validated the cost model, family arithmetic, search CLI, exact norm samplers, comparison report, and ceiling certificate.
- [EMPIRICAL: stated seed interval] Enumerated 302 accepted toy candidates and wrote deterministic CSV/JSON artifacts.
- [HEURISTIC] Generated the three-target, three-model leading-term sensitivity table; Q009 subsequently validated the finite equation on BLS12 but does not turn the leading-term rows into concrete prime seeds.
- [PROVED] Added exact nested-resultant sampling for the published BLS12 SexTNFS polynomials and a numerically stable interval-Chebyshev Dickman evaluator.
- [EMPIRICAL: 1,024 samples, RNG seed 20260722] Reproduced the published BLS12 norm-size inputs and obtained 131.789 bits without recalibration.
- [PROVED] Reduced all KSS16 seeds below the $2^{60}$ field ceiling to a 511-seed interval and certified that none of the eight integral candidates has both $p$ and $r$ prime.
- [PROVED] Added exact BN, KSS16, and BLS24 nested-resultant samplers under both the stated and public-code coefficient domains.
- [EMPIRICAL: 512 samples per convention] Reproduced BN within 0.04 cost bits and KSS16 within 0.13 bits under the public-code convention; retained the BLS24 `A=9` discrepancy without calibration.
- [EMPIRICAL: preregistered 128-sample sensitivity] Sampling BLS24 with bound 10 reproduces the printed 1295/1460 norms within one bit, supporting but not proving an unrecorded historical rounding step.

## Outcome

[EMPIRICAL: final artifacts] Complete within scope: the requested pipeline is reproducible, finite-size audits cover all four families, the BLS24 historical-setting ambiguity is isolated as Q027, and every extrapolated production row remains explicitly labelled rather than being presented as a concrete prime seed.
