# Log — P5.1

## Session 1 — 2026-06-24

**Goal:** Complete SG-01 and the explicit, supported part of SG-02; obtain a first three-curve convergence table and map the GRH dependency.

**Prediction (written before running anything):**

- [HEURISTIC] The trivial-torsion Serre curve will yield a nonzero prime-order count and a measured/predicted ratio compatible with 1 at the largest toy cutoff; this prediction is refuted if the ratio's heuristic 95% interval excludes 1.
- [PROVED] The rational 2- and 3-torsion curves will yield no prime orders beyond finitely many tiny exceptions, because their good reductions contain the corresponding rational torsion point.
- [CITED] The truncated universal product will approach $0.505166168239435774$, and the explicit Serre correction will approach $0.561295742488261971$. (Zywina 2011, equations (2.3) and (5.1), arXiv:0909.5280.)

**Environment preflight:**

- [EMPIRICAL: Python 3.13.4 on Windows 11] `env/check_env.py` found SageMath, PARI/GP, Singular, and msolve unavailable.
- [EMPIRICAL: 34 shared tests] After installing pytest 9.1.1, `python -m pytest -q lib/tests` passed 34/34 tests in 0.94 seconds.

**Did:**

- Implemented `code/measure_density.py` with a deterministic prime sieve, the shared exact Hasse-interval BSGS/twist counter, an explicit exhaustive fallback, CSV output, convergence plots, and a sub-10-second smoke mode.
- Added four P5.1 tests: published constants, LMFDB point counts for 1728.w1, rational torsion certificates, and an end-to-end smoke measurement.
- Ran checkpoints from $2^{10}$ through $2^{17}$ for a trivial-torsion Serre curve and non-CM curves with rational 2- and 3-torsion.
- Audited Zywina's corrected constant and David--Wu's effective-Chebotarev/sieve dependency.

**Found:**

- [EMPIRICAL: 57 tests] `python -m pytest -q problems/P5.1-koblitz-conjecture/code/tests lib/tests` passed 57/57 tests in 1.18 seconds.
- [EMPIRICAL: 67 reductions through $p=97$] The production counter matched exhaustive point counts on every validation case; 66 cases used BSGS/twist and one used the declared exhaustive fallback.
- [EMPIRICAL: Euler factors $\ell\le10^6$] The universal product was $0.505166202477432$ and the corrected Serre constant was $0.561295780530480$, each within $4\mathbin{\cdot}10^{-8}$ of Zywina's published value.
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] Curve 1728.w1 had 683 prime-order reductions among 12,249 tested; the refined prediction was 654.886 and observed/predicted was $1.04293$.
- [HEURISTIC] A Poisson-style 95% interval for the final observed/predicted ratio is $[0.9647,1.1211]$; this interval ignores cross-prime dependence and finite-cutoff bias.
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] The raw $C_{E,1}x/(\log x)^2$ prediction was 529.85, giving observed/predicted $1.2890$, while the refined prime-sum ratio was $1.0429$.
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] Both rational-torsion curves had zero prime-order reductions, matching the corrected $C_{E,1}=0$ obstruction.
- [CITED] David and Wu use the theta-zero-free hypothesis in effective Chebotarev error terms for division-field Frobenius counts; these errors set the sieve level $D=x^{(2/5)(1-\theta)(1-\varepsilon)}$. GRH is $\theta=1/2$, but $\theta<11/21$ already suffices for their eight-almost-prime corollary. (David and Wu 2012, Theorem 3.9, Theorem 1.1, and Corollary 1.2, arXiv:0812.2860.)

**Prediction vs. outcome:** matched. [EMPIRICAL: $p\le2^{17}$] The Serre ratio interval contains 1, both rational-torsion prime-order counts are zero, and the implemented constants reproduce the published targets.

**Did not work:**

- [EMPIRICAL: validation curve 112.b4 at $p=11$] Point-order congruences did not isolate the group order within 64 samples; the production path used the declared exhaustive exact fallback and matched the independent exhaustive fixture.

**Changed my mind about:**

- [EMPIRICAL: $p\le2^{17}$] The asymptotic $x/(\log x)^2$ expression is too biased for a useful toy-range comparison; the refined prime sum is not merely cosmetic at this scale.

**Next:** Implement the corrected quotient constant $C_{E,3}$ for the 3-torsion curve, then compare it with the already recorded 661 prime quotient orders.
