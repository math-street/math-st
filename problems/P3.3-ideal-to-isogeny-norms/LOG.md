# Log

## Session 1 - 2026-07-01

**Goal:** Establish the KLPT-independent target line by implementing validated
rank-4 maximal-order ideals, then compare norm-aware LLL with exact shortest
vectors over at least 100 seeded toy instances.

**Prediction (written before running anything):** [HEURISTIC] The exact
equivalent-ideal norm will usually be within a small constant factor of
$\sqrt p$, and norm-aware LLL will recover the exact shortest norm on more
than 80% of instances below $p=2^10$. This prediction is refuted in the
sample if the median ratio $N(J)/\sqrt p$ exceeds 4 or the exact-hit rate is at
most 80%.

**Did:**

- Initialized the problem packet after confirming that `lib/quaternion.py`,
  `lib/isogeny.py`, and a KLPT implementation were absent.

**Found:** Pending experiment.

**Prediction vs. outcome:** Pending experiment.

**Did not work:** Pending experiment.

**Changed my mind about:** Pending experiment.

**Next:** Run environment checks and validate the order arithmetic before
sampling ideals.

### Session 1 completion

**Did:**

- Ran `env/check_env.py`; Python 3.13.4, SymPy 1.14.0, and Matplotlib 3.11.1
  were available, while SageMath was unavailable.
- Ran the 34 pre-existing shared tests before implementation; all passed.
- Added `lib/quaternion.py` and five algebra/ideal/SVP regressions.
- Added `code/measure_norm_gap.py`, three script tests, deterministic CSV
  summaries, and SVG/PNG plots.
- Corrected a row/column HNF transposition bug found by smoke-mode closure
  checks.
- Superseded an all-$3\bmod8$ pilot with a balanced 140-instance run.
- Checked the 2014 KLPT paper and the 2025 maximal-order parametrization paper
  against primary texts.

**Found:**

- [EMPIRICAL: 140 prime-neighbor ideals, $7\le p\le223$] LLL hit the certified
  exact shortest norm on 140/140 instances; the median
  $N(J)/\sqrt p$ was 0.35921 and the maximum exponent was 0.42357.
- [EMPIRICAL: same range] Mean exponents were 0.19905 for
  $p\equiv3\pmod8$ and 0.19283 for $p\equiv7\pmod8$; no congruence effect was
  detected.
- [CITED] Basic KLPT's complete ideal-norm estimate is $p^{7/2}$ under its
  optimistic heuristics; the prompt's $p^3$ figure describes the intermediate
  lifted quaternion. [Kohel--Lauter--Petit--Tignol 2014, Theorem 7]

**Prediction vs. outcome:** [EMPIRICAL: 140 prime-neighbor ideals,
$7\le p\le223$] Matched. The median exact ratio was below the pre-registered
cutoff 4, and the 100% LLL exact-hit rate exceeded the predicted 80% threshold.

**Did not work:** The first canonical HNF basis used the rows of a column HNF
and could fail left-ideal closure. Transposing the result fixed the lattice;
the failure is now covered by seeded randomized tests. The first sample frame
could not test $p\bmod8$ because every prime was $3\bmod8$; a balanced rerun
fixed the design.

**Changed my mind about:** [EMPIRICAL: same range] At this scale, plain exact
norm-aware LLL is stronger than expected: no reduction-to-SVP gap was visible.
The interesting obstruction is more likely the prescribed norm shape or
larger-parameter behavior, neither of which this run measures.

**Next:** Run three separated bit-size bands to locate the first LLL miss or
exact-search crossover, then compare the same ideals with a validated KLPT
implementation.

## Session 2 - 2026-07-13

**Goal:** Extend the exact optimum/LLL comparison to 30 ideals in each of three
balanced size bands near 12, 20, and 28 bits, fit the observed search and
runtime growth, and use the result to choose the next constrained-norm
experiment.

**Prediction (written before running anything):** [HEURISTIC] Norm-aware LLL
will retain at least a 95% exact-hit rate in every band, but the exact
coefficient-box size and end-to-end runtime will grow with bit length. This is
refuted as a stable exact-LLL phenomenon if the 28-bit hit rate is below 95%,
or as a cheap exact certificate if any search requires more than 10,000
coefficient tuples.

**Did:** Pending experiment.

**Found:** Pending experiment.

**Prediction vs. outcome:** Pending experiment.

**Did not work:** Pending experiment.

**Changed my mind about:** Pending experiment.

**Next:** Run environment/shared tests, generate a balanced prime grid, and
execute the three-band experiment.

### Session 2 completion

**Did:**

- Re-ran 53 shared and three original P3.3 tests before new experiments; all
  passed.
- Generated balanced 12/20/28-bit prime grids.
- Detected that fixed $\ell\le31$ forces the trivial upper bound
  $q_I(\ell)=\ell$, invalidating Session 1's distributional interpretation.
- Added Tonelli--Shanks isotropic sampling and a `near-p` input-norm policy.
- Ran the corrected 108-instance unconstrained experiment and stored a
  three-band timing fit with residuals.
- Added exact normalized-norm spectrum enumeration, int64 overflow checks,
  adaptive cutoffs, and `measure_shape_gap.py`.
- Ran 70 exact shape instances and validated every selected equivalent ideal.
- Visually inspected the corrected norm-gap and shape-gap PNGs.

**Found:**

- [PROVED] The Session 1 small-$\ell$ distribution is unsuitable for a
  Minkowski-scale target line because every row has $N(J)\le\ell\le31$.
- [EMPIRICAL: 108 near-$p$ ideals, 12/20/28-bit $p$] LLL hit exact SVP on
  108/108 rows; mean $N(J)/\sqrt p$ stayed in $[0.35809,0.37189]$ across the
  three bands and the maximum exponent was 0.47016.
- [EMPIRICAL: same range] Maximum exact certificate size was 80 nonzero
  tuples; mean exact-search times were 0.00281, 0.00464, and 0.00615 seconds.
- [EMPIRICAL: 70 near-$p$ ideals, $7\le p\le223$] Powers of 2, powers of 3,
  and 5-smooth norms all appeared by normalized norm $p$. Median penalties
  were 1, 1.5, and 1; maximum penalties were 21.33, 20.25, and 1.43.

**Prediction vs. outcome:** [EMPIRICAL: 108 near-$p$ ideals] Matched. Every
band exceeded the predicted 95% exact-hit threshold, no certificate exceeded
10,000 tuples, and mean exact-search time increased mildly with bit length.

**Did not work:** The first scaling run reused small $\ell$ and was
mathematically confounded. Its 28-bit process also timed out while comparing a
long theta prefix for an artificially easy class. Near-$p$ sampling removed
both issues. The first exact spectrum implementation took 104 seconds for
three tiny tests because it materialized every point as Python/Fraction
objects; overflow-checked NumPy blocks plus adaptive cutoffs reduced the same
tests to 0.37 seconds.

**Changed my mind about:** [EMPIRICAL: measured ranges] The earlier perfect
LLL result was supported by a bad sampler, but the corrected result survives
through 28 bits. More importantly, exact pure-power representatives also
exist by norm $p$ in every small instance, so the basic KLPT $p^{7/2}$ gap
looks less like a structural absence of shaped representatives and more like
the cost of its particular lifting and norm-equation search.

**Next:** Implement a target-specific exact solver for
$q_I(x)=2^e$ and $q_I(x)=3^e$ so the shape optimum can be measured in the
12/20/28-bit bands without enumerating every smaller norm; then put a validated
KLPT implementation on the same instances.

### Session 2 continuation - sparse pure-power targets

**Did:** Implemented increasing-target exact scans, added a quadratic
coordinate-elimination fallback for boxes above $10^9$ tuples, validated both
paths against full spectrum enumeration, and replayed all 108 A002 ideals for
powers of 2 and 3 through $4p$. Reconstructed and closure-checked every output
ideal, then visually inspected the new plot.

**Found:**

- [EMPIRICAL: 108 near-$p$ ideals, 12/20/28-bit $p$] Both optima were found
  on all rows. Mean exponents were 0.78713 for $2^e$ and 0.77643 for $3^e$,
  versus 0.40731 unconstrained.
- [EMPIRICAL: same range] Overall median penalties were 222.64 and 168.23;
  the 28-bit medians were 2476.82 and 2622.49.
- [EMPIRICAL: same range] Only one optimum exceeded $p$: a $2^e$ target with
  exponent 1.01280. The maximum $3^e$ exponent was 0.97585.
- [EMPIRICAL: same run] Runtime was 43.53 seconds. Two rows used exact
  coordinate elimination; there were no errors or censored outputs.

**Did not work:** The first full run treated a $10^9$ box-size guard as a hard
censor, leaving two computationally censored rows, while a third row exhausted
targets at $p$. Recasting the guard as a switch to exact coordinate elimination
and extending targets through $4p$ removed all three censored outputs.

**Changed my mind about:** [EMPIRICAL: measured ranges] The small-$p$ finding
that pure-power penalties rarely exceed 20 was a finite-size effect. Exact
shape constraints are already costly at 28 bits, though their optima remain
far below the basic KLPT output scale.

**Next:** Implement and validate basic KLPT on these same instances, then
measure its overhead relative to A004's exact shaped optimum.

**Protocol note and prediction-vs-outcome:** No numerical A004 prediction was
written into `LOG.md` before execution, so a numerical prediction must not be
backfilled. The operational expectation stated during implementation was that
exact coordinate elimination would remove the two computation-censored rows;
it did, and extending the target list through $4p$ also resolved the sole
range-censored row. This protocol miss should be corrected by preregistering
the first matched-KLPT success-rate and norm-ratio thresholds before SG-09.
