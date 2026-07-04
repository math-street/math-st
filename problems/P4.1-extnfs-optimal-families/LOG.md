# P4.1 research log

## Session 1 — 2026-06-26

**Goal:** Build a validated first version of the cost model, family generators, deterministic search, and sensitivity report.

**Prediction (written before running anything):** [HEURISTIC] A single calibrated $L_{p^k}(1/3,c)$ model will reproduce its BN254 anchor by construction but will not justify a unique cross-family optimum because special-form and tower advantages require family-dependent assumptions. This prediction is falsified if one literature-derived, fully specified constant independently matches multiple published estimates across the required families without recalibration.

**Did:**
- Initialized the problem record and attempt A001.
- Added `lib/tnfs_cost.py`, four exact family evaluators in `lib/curves.py`, and seven shared known-answer tests.
- Added the deterministic search/extrapolation CLI and its subprocess smoke test.
- Verified primary literature and recorded six references.
- Generated the bounded-search CSV, 36-row sensitivity CSV, and JSON proof-scope summary.

**Found:**
- [EMPIRICAL: BD19 BN fixture, final stable evaluator] The finite model returns 99.573 bits against 99.69 published, a 0.117-bit difference within the declared 0.2-bit tolerance.
- [EMPIRICAL: published BLS12-381 constants] The generated $p$ and $r$ match exactly and the least embedding degree is 12.
- [EMPIRICAL: every integer seed $-10{,}000\le u\le10{,}000$, $p<2^{60}$] The accepted counts are BN 273, BLS12 24, BLS24 5, and KSS16 0; no accepted row meets any production target.
- [PROVED] In the implemented four-family leading-term objective, BN is the unique minimum estimated $\rho$ at 128, 192, and 256 bits under every sensitivity scenario.
- [EMPIRICAL: three named scenarios] The selected family is stable, while the estimated BN field size changes by roughly 45–47% between calibrated special-form and composite-exTNFS scenarios.

**Prediction vs. outcome:** [EMPIRICAL: session 1] Partly matched. The explicit finite-size equation reproduced the BN anchor without a fitted overhead, which was better than predicted; cross-family finite-size validation still remains Q009, and the practical recommendation differs once operation cost is made an objective.

**Did not work:** [EMPIRICAL: stated toy interval] No prime KSS16 fixture was found in the original bounded scan. Treating the raw BN factor base as the relation target also appeared to miss sufficiency by about 0.03 bits; the final implementation distinguishes the raw factor base from the Galois-reduced target required by the paper.

**Changed my mind about:** [PROVED] The formal minimum-$\rho$ objective is too narrow to reproduce practical family recommendations; it selects BN even when higher-$\rho$ families have far smaller base fields and pairing proxies.

**Next:** Implement the published norm sampling process for BLS12 and attempt an independent finite-size match without recalibration.

## Session 2 — 2026-07-04

**Goal:** Close Q009 with a tested exact toy norm sampler and a non-BN finite-size cost regression, then resolve Q010 by exhausting every integral KSS16 seed whose generated field stays below $2^{60}$.

**Prediction (written before the new experiments):** [HEURISTIC] The finite cost equation will reproduce a published BLS12 result within 0.5 bits when supplied the paper's norm averages, but a toy sampler will not reproduce those production averages without implementing the exact tower and polynomial-selection choices. This prediction is falsified if the same sampler and fixed settings match both published BN and BLS12 norm averages within their printed precision. [CONJECTURE] No KSS16 prime pair exists below the 60-bit $p$ ceiling; a concrete accepted seed refutes this immediately.

**Did:**
- Re-read `STATE.md`, `SUBGOALS.md`, and A001; all 54 baseline tests passed.
- Recovered the exact BLS12 `h,f,g` construction and nested-resultant norm equation from Barbulescu--Duquesne Sections 3, 4, and 7.1.2.
- Replaced cumulative trapezoidal Dickman integration with stable interval-Chebyshev integration after the former became negative at the BLS12 `u=791.2/73.5` input.
- Added a deterministic exact-integer BLS12 sampler, hand-resultant tests, a 1,024-sample production run, and an end-to-end finite-cost regression.
- Added an analytic KSS16 seed cutoff, exhaustive 511-seed certificate, exact candidate factorizations, and certificate tests.

**Found:**
- [EMPIRICAL: published BLS12 norm inputs] The stable Dickman evaluator returns smoothness log-probabilities -39.171 and -24.671, matching the printed -39.17 and -24.67.
- [EMPIRICAL: 1,024 exact samples, RNG seed 20260722] Mean integer bit lengths are 791.083 and 584.756 versus the paper's 791.2 and 584.8; the resulting finite cost is 131.789 versus 131.8.
- [EMPIRICAL: same samples] Mean real logarithms are about half a bit smaller, exposing a bit-length convention hidden by the paper's wording.
- [PROVED] Every KSS16 seed with `p<2^60` lies in `[-255,255]`; eight seeds give integral positive parameters and exact factorization rules out a prime pair in every row.

**Prediction vs. outcome:** [EMPIRICAL: session 2] The cost-equation prediction matched more strongly than the 0.5-bit tolerance: exact sampled norms produced a 0.011-bit difference. The expectation that the exact tower would be difficult was wrong because the nested resultants were practical in SymPy. The KSS16 conjecture was upgraded to a proof within the ceiling.

**Did not work:** [EMPIRICAL] The original step-`1e-4` trapezoidal Dickman table suffered catastrophic cancellation and became non-positive near argument 10.76. A first comparison using mean `log2(N)` also appeared low by roughly half a bit until both real-logarithm and integer-bit-length conventions were reported separately.

**Changed my mind about:** [PROVED] A second family regression did not require tuning a new asymptotic prefactor; the finite equation was adequate once the exact norm construction, Galois quotient, and stable Dickman evaluation were combined.

**Next:** None for P4.1's stated scope. Treat a larger family taxonomy or concrete production prime-seed generation as a new task rather than silently expanding this search space.
