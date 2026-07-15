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

## Session 3 — 2026-07-15

**Goal:** Extend exact norm validation to every implemented family, audit the authors' public sampling code, and report any irreducible reproduction discrepancy instead of ending at the BLS12 row.

**Protocol note:** [EMPIRICAL] The goal was stated in the live work commentary before the exploratory 512-sample runs, but a numeric prediction was not first written to this log. The forward prediction below is therefore reserved for a new independent-seed confirmation run rather than being retroactively attached to the completed samples.

**Prediction (written before independent-seed confirmation):** [HEURISTIC] With the public-code bound convention `randint(-A,A+1)`, a fresh 128-sample KSS16 run will remain within 1.0 cost bit of the printed 139.0 row, while BLS24 will remain at least 1.0 bit below the printed 203.72 row. The prediction is falsified if either inequality reverses. All shared and P4.1 tests should still pass after replacing binary64 Dickman integration with the 80-decimal-digit evaluator.

**Did:**
- [EMPIRICAL: independent RNG seed 20260723, 128 samples] Confirmed the prediction: KSS16 was 0.542 bits below its printed row and BLS24 was 1.800 bits below its printed row.
- Inspected the authors' public sampler and found its inclusive `randint(-A,A+1)` bound differs from the paper's stated `[-A,A]` domain.
- Replaced binary64 Dickman integration with a cached 80-decimal-digit, degree-30 interval evaluator and added finite-row regressions through BLS24 `u=1460/109.8`.
- Added deterministic exact samplers for the published BN, KSS16, and BLS24 constructions, retained both coefficient domains, and combined eight checked-in runs into one CSV/JSON audit.

**Next experiment prediction (written before execution):** [HEURISTIC] If the BLS24 discrepancy comes from applying both an integer ceiling to an internal coefficient bound near 10 and the public sampler's extra `+1`, then sampling the profile with nominal bound 10 under the public-code convention will place the mean `f` norm within 10 bits of 1295. Failure leaves the historical norm row under-specified by the surviving public artifacts.

**Found:**
- [EMPIRICAL: 512 samples per convention, RNG seed 20260722] BN sampled costs differ from the printed 131.3 row by 0.026/0.035 bits; KSS16 differs by -0.847 bits on `[-A,A]` and -0.120 bits under the public-code bound.
- [EMPIRICAL: same BLS24 runs] Printed `A=9` gives 201.255 bits on `[-A,A]` and 201.803 bits under the public-code convention, respectively 2.465 and 1.917 bits below 203.72.
- [EMPIRICAL: preregistered RNG seed 20260724, 128 samples] The sampling-bound-10 public-code run gives mean integer bit lengths 1295.867/1461.000, with both printed norms inside the normal 95% intervals, and cost 203.171 bits.
- [PROVED] The paper's printed domain and public source cannot denote the same discrete distribution because Python `randint` includes both endpoints.

**Prediction vs. outcome:** [EMPIRICAL: session 3] Both forward predictions matched. The independent seed kept KSS16 within 1 bit and BLS24 more than 1 bit low at printed `A=9`. The bound-10 sensitivity put the `f` norm only 0.867 bits above 1295, well inside the preregistered 10-bit threshold, and also reproduced the `g` norm within one bit. The final suite passed all 70 shared and 10 P4.1 tests, plus `compileall` and the stale-tag scan.

**Did not work:** [EMPIRICAL] Direct downloads of the paper PDF through ePrint and HAL were blocked by anti-bot interstitials. Primary-source text extraction, the authors' public Python source, and their published parameter archive nevertheless independently fixed the relevant formulas. The printed `A=9` BLS24 row did not reproduce under either literal coefficient-domain interpretation. The first combined P4.1 test run exposed one indentation error in the newly changed comparison-test assertion; correcting it and rerunning the entire suite resolved the failure.

**Changed my mind about:** [HEURISTIC] The BLS24 gap is unlikely to be a polynomial-selection error: a one-unit sampling-bound change explains the printed norms on both sides simultaneously. The strongest surviving explanation is an unrecorded internal rounding step, but it remains an inference rather than a recovered historical fact.

**Next:** None for the declared deliverable. Historical BLS24 setting recovery is isolated as non-blocking Q027; expanding the taxonomy or generating production primes is new scope.
