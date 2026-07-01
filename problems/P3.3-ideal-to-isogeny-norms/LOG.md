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
