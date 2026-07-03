# Log

## Session 1 - 2026-07-03

**Goal:** Audit the literal lower bound, validate a height implementation, and
complete the smallest reproducible one- and multi-point measurement matrix.

**Prediction (written before running anything):** [CONJECTURE] The literal
uniform lower bound is false because bounded-coordinate rational curves and
points can be reduced at arbitrarily large good primes; a random-target or
genericity condition will be necessary. This prediction is refuted if every
valid low-coordinate construction fails one of the formal lifting conditions.

**Positive result criterion:** [EMPIRICAL: pre-registered] A tested construction
produces valid reductions for $k=1,2,3,4$, a validated height routine reports
finite values, and regression fits plus row-level residuals are stored.

**Negative result criterion:** [EMPIRICAL: pre-registered] A declared search or
runtime ceiling is reached; censored cases are retained and no exponent is
reported for them.

**Did:**
- Ran `env/check_env.py` and all 14 pre-existing shared tests before adding new mathematics.
- Implemented exact rational generalized-Weierstrass arithmetic and a finite-doubling canonical-height estimator in `lib/heights.py`.
- Added four shared height tests and three P1.6 tests.
- Implemented direct single-point and linear $k=1,2,3,4$ simultaneous lifts, exact reduction checks, seeded nullspace variants, summaries, fits, residuals, and a figure.
- Checked the primary 2000 failure analysis and exactly enumerated its $p=257$ small-relation probability.
- Ran the full matrix at six primes, three input trials, three lift variants, and five exact doublings.

**Found:**
- [PROVED] Every single affine target point has a short-Weierstrass lift with canonical height $O(\log p)$, so the literal $\Omega(p^c)$ target is false for every $c>0$.
- [PROVED] For $k\leq4$, full row rank of the five-column coordinate constraint matrix modulo $p$ gives a simultaneous generalized-Weierstrass lift with every selected height $O_k(\log p)$.
- [PROVED] The multi-point construction does not control Mordell-Weil rank or rational dependence, which is the precise remaining attack-relevant obstruction.
- [EMPIRICAL: p in {31,127,503,2039,8191,32719}; three trials per p] Logarithmic-fit slopes for the maximum height were $4.543$, $6.983$, $8.643$, and $10.308$ for $k=1,2,3,4$; the stored 95% intervals are respectively $[3.752,5.334]$, $[6.033,7.933]$, $[7.346,9.940]$, and $[9.144,11.472]$.
- [EMPIRICAL: same range] For $k=2,3,4$, logarithmic fits had smaller original-height RMSE than power fits: $4.259<5.849$, $5.818<8.275$, and $5.219<8.828$.
- [EMPIRICAL: 216 random general-model variants] The maximum final-iteration change was $0.4723$ and the maximum relative change for a positive group height was $0.362\%$.
- [CITED] Jacobson et al. (2000) make xedni fail through a conditional absolute bound on rational relation coefficients and finite-group counting, not through a proved $p^c$ lower bound on selected point heights.
- [EMPIRICAL: exact enumeration at p=257] The published Experiment C count was reproduced: group order 263, 260 eligible second points, four favorable points, and probability $1/65$.
- [EMPIRICAL: local environment on 2026-07-03] The completed output contains 678 point rows, 282 curve/group rows, 102 summary rows, 30 fit rows, and 393 row-level residuals.

**Prediction vs. outcome:** [PROVED] The literal prediction matched: fixed
small curves and the constructive upper bounds defeat a positive power lower
bound. [CITED] The predicted historical framing diverged from the primary
source because the 2000 analysis is about rare dependence and bounded relation
coefficients, not selected lifts behaving as random points of height $p^c$.

**Did not work:** [EMPIRICAL: local environment on 2026-07-03] Sage, PARI/GP,
Singular, and msolve were unavailable. The exact rational doubling fallback
passed independent database checks; total Mordell-Weil ranks of random lifted
curves remain unmeasured and are explicitly marked unavailable.

**Changed my mind about:** [PROVED] Height growth alone is not the right formal
obstruction. The missing theorem must combine a no-small-relation finite-field
input distribution with rational dependence or rank below $k$.

**Next:** Add an exact small-relation search for the random rational lifts at bits $5,7,9,11$, stratify height and discriminant by detected relation size, and compare that conditional sample with Section 5 of Jacobson et al. (2000).
