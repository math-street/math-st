# Log — P5.2

## Session 1 — 2026-06-25

**Goal:** Complete SG-01a and SG-02a for the explicit (D=-3) and (D=-4) families, then obtain a small preregistered measurement toward SG-03a.

**Prediction (written before running anything):**

- [CONJECTURE] Canonicalizing a well-mixed rho walk under the six units for (D=-3) and four units for (D=-4) will reduce the median collision count by factors near (sqrt 6) and (2), respectively, relative to the same walk without quotienting. A refuting test is a 95% bootstrap interval for the step ratio that excludes those values after at least 200 successful seeded trials at each of four subgroup sizes.
- [CONJECTURE] No tested speedup will grow with subgroup order once orbit size is fixed. A refuting test is a log-log fit over at least four bit sizes whose positive slope has a 95% confidence interval excluding zero and persists under a second walk partition.

**Did:**

- Initialized the problem record and selected the smallest explicit-CM construction route.

**Found:** pending.

**Prediction vs. outcome:** pending.

**Did not work:** pending.

**Changed my mind about:** pending.

**Next:** implement and validate the explicit endomorphisms and quotient walk.

### Session 1 completion

**Did:**

- Added `pollard_rho_orbits` to `lib/dlog.py` with baseline, finite-orbit, Floyd, and collision-table modes plus auditable counters.
- Added explicit $D=-3$ and $D=-4$ construction and validation code, two independent point-count checks, known-answer tests, a seeded measurement script, raw data, bootstrap intervals, fits, and residuals.
- Ran 200 paired trials at each of four field sizes for each discriminant and preserved both failed cycle-handling designs.

**Found:**

- [EMPIRICAL: eight curves over p=4057..261673] Exhaustive and Hasse-interval/BSGS counts agreed, and 32 seeded endomorphism checks passed per curve; see the validation CSV.
- [EMPIRICAL: 3,200 recovered collision-table DLPs, r=2053..262519] Mean transition speedups were 2.424-2.664 for $D=-3$ and 1.853-2.186 for $D=-4$; all eight 95% intervals contain $\sqrt6$ or $2$, respectively.
- [EMPIRICAL: four sizes, 200 trials each] The log-log speedup slope was $-0.0109$ with interval $[-0.0420,0.0209]$ for $D=-3$, and $-0.0385$ with interval $[-0.0731,-0.0027]$ for $D=-4$.
- [PROVED] For a fixed unit action of order $m$, the nonzero subgroup points form free size-$m$ orbits, so the ideal-random-mapping quotient speedup tends to $\sqrt m$.
- [PROVED] Imaginary quadratic units have order at most six, giving a unit-action ceiling $\sqrt6$; this does not cover non-unit CM endomorphisms.

**Prediction vs. outcome:** [EMPIRICAL: collision-table mode over the recorded range] The constant-factor prediction matched: every interval contains the predicted orbit factor and no positive scaling slope was observed. The original wording implicitly assumed a well-mixed walk; the naive Floyd implementation violated that assumption through fruitless cycles.

**Did not work:**

- [EMPIRICAL: naive Floyd mode, same range] Zero-denominator fruitless cycles erased the largest-size gain, reducing the mean-work ratio to 0.916 for $D=-3$ and 0.617 for $D=-4$.
- [EMPIRICAL: local-doubling escape, same range] The attempted escape rule recurred hundreds of times and was substantially slower; A002 records the post-mortem.

**Changed my mind about:** [PROVED] Reporting only the quotient cardinality is insufficient for a practical rho speedup claim; cycle handling and the memory model are part of the algorithmic statement.

**Next:** Implement the GLV $D=-7$ non-unit example, measure eigenvalue orders, and attack Q020.
