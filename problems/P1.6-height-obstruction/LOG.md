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

## Session 2 - 2026-07-14

**Goal:** Complete SG-08 by exactly classifying bounded relations in the
existing random lifts, then use the result to decide whether a faithful
$p=17$ xedni reproduction is the next useful experiment.

**Prediction (written before implementing or running the relation search):**
[CONJECTURE] Most finite-field tuples will already have no relation with
$\ell_\infty$ coefficient bound eight, and no rational relation will occur
unless the finite tuple first passes that necessary filter. This prediction is
refuted if at least 10% of the random general-model lifts have a rational
relation of bound at most eight.

**Positive result criterion:** [EMPIRICAL: pre-registered] Every row is checked
by exact arithmetic, relation witnesses re-evaluate to the identity, and a CSV
separates finite-field no-small-relation cases from rationally dependent cases
by $k$, bit size, variant, height, and discriminant height.

**Negative result criterion:** [EMPIRICAL: pre-registered] If exact rational
coordinates exceed a 60-second per-matrix ceiling, retain the finite-field
filter and mark the affected rational rows as censored rather than independent.

**Did:**
- Implemented an exact meet-in-the-middle minimal-$\ell_\infty$ relation search and exact witness re-evaluation.
- Audited all stored variants at bits 5,7,9,11 for $k=1,2,3,4$ through coefficient bound eight and wrote row-level and stratified CSV files.
- Implemented a diagnostic $p=17$ projective-lattice prototype, validated its reusable algebraic components, and stopped before accepting any dependency-rate output.
- Marked the $p=17$ reproduction as failed dead attempt A002 at the user's direction.

**Found:**
- [EMPIRICAL: 144 curve variants, coefficient bound 8] A finite-field relation existed in 99 variants, while a rational relation existed in only two variants.
- [EMPIRICAL: the same 144 variants] The rational statuses were 97 `no-relation-through-bound`, 45 `skipped-no-finite-relation`, and two `relation`, with no timeout-censored rows.
- [EMPIRICAL: 108 variants with k in {2,3,4}] No rational relation through coefficient bound eight was found.
- [EMPIRICAL: two rational-relation variants] Both witnesses were coefficient $-2$ on the same $p=31$, $k=1$, $y=0$ two-torsion input, under two different lift variants.

**Prediction vs. outcome:** [EMPIRICAL: 144 curve variants] The prediction that
most finite tuples would lack a relation through bound eight was wrong because
99 of 144 had one, especially every tested $k=3,4$ tuple. The registered 10%
rational-relation falsifier was not reached: the observed bounded rational rate
was $2/144$.

**Did not work:** [PROVED] A002 is not a reproduction of the published $p=17$
experiment. The paper does not specify the sampling/tie-breaking distribution
needed to match the reported rate, and a bound-eight relation search cannot
replace the paper's 2-descent test of dependence.

**Changed my mind about:** [EMPIRICAL: this bounded audit] Small finite-field
relations are common for the tested $k=3,4$ samples, but they almost never lift
to equally small rational relations. Finite relation incidence alone is
therefore a weak proxy for useful lifted dependence.

**Next:** Keep A002 closed unless the original sampling implementation or a
complete distribution and equivalent 2-descent pipeline becomes available;
this reopening condition is Q018. Use the exact SG-08 data only for
bounded-relation claims.
