# Log — P2.3

## Session 1 — 2026-07-13

**Goal:** Complete SG-01 and obtain a reproducible first SG-02 operation-count fit over at least four sizes.

**Prediction (written before running anything):** [CONJECTURE] For deliberately chosen prime orders with a divisor \(d\) within a constant factor of \(\sqrt n\), the median counted group operations of the two-stage implementation will fit a log-log slope in \([0.20,0.30]\). This prediction is refuted if the 95% confidence interval from the predeclared fit does not intersect that interval or if any recovery fails validation.

**Positive result criterion:** [CONJECTURE] Every tested recovery verifies against its seeded ground truth, the exhaustive tiny test passes, and the fitted slope interval intersects \([0.20,0.30]\).

**Negative result criterion:** [CONJECTURE] A verified implementation produces a fitted slope interval disjoint from \([0.20,0.30]\), or the operation-count residuals show a systematic size trend that invalidates a single power-law interpretation over the tested range.

**Did:**
- Initialized the P2.3 persistent session files and A001.
- Ran `env/check_env.py`; Python 3.13.4 was available while Sage, Singular,
  and msolve were unavailable.
- Ran all 18 shared-library tests successfully.
- Implemented the two-stage divisor-case recovery in `code/cheon.py` and an
  opaque prime-order group simulator with separate exponentiation-call and
  primitive-group-operation counters.
- Added four tests and exhaustively validated all secrets in simulated groups
  of orders 17, 19, and 31, plus all secrets for \(d=3,6\) on the concrete
  order-19 elliptic-curve group.
- Ran the predeclared scaling experiment at eight sizes with 41 seeded trials
  per size and 2,000 within-size bootstrap resamples.
- Re-ran the repository after final documentation: all 34 then-current shared
  tests and all four P2.3 tests passed.

**Found:**
- [CITED] Cheon's Theorem 1 recovers \(x\) from \(g,g^x,g^{x^d}\) when
  \(d\mid n-1\) using
  \(O(\log n(\sqrt{(n-1)/d}+\sqrt d))\) primitive group operations and
  \(O(\max\{\sqrt{(n-1)/d},\sqrt d\})\) memory (Cheon, EUROCRYPT 2006,
  LNCS 4004, Theorem 1; `refs/cheon2006.md`).
- [EMPIRICAL: 328 trials, 70913 <= n <= 17592207015937] Every recovery
  matched its seeded ground truth; the log-log slope of median
  scalar-multiplication calls was 0.25001 with a 95% within-size bootstrap
  interval of [0.24610, 0.25351] (`code/run_scaling.py`,
  `data/run_scaling_fit_hb8-22_t41_s2303_20260713.json`).
- [EMPIRICAL: exhaustive n in {17,19,31}] The implementation recovered every
  scalar in the three simulated groups and every scalar for \(d=3,6\) in the
  concrete order-19 elliptic-curve group (`code/tests/test_cheon.py`).

**Prediction vs. outcome:** The SG-02 prediction matched: the confidence
interval lies inside the predeclared [0.20, 0.30] target interval.

**Did not work:** The main requested result was not reached. No invariant for
general polynomial families, non-divisor speedup, or matching generic-group
lower bound was obtained. At the user's direction, the overall target is
recorded as **failed**, despite the successful known-case reproduction.

**Changed my mind about:** [CITED] The omitted \(\log n\) factor matters when naming
the metric: the quarter-power fit applies directly to exponentiation calls,
while primitive double-and-add operations retain the published logarithmic
factor (Cheon 2006, Theorem 1).

**Next:** If resumed, run SG-03's divisor sweep and use it as the live control
for a precisely specified SG-04 non-divisor experiment.
