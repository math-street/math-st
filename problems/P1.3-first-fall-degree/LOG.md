# Log

## Session 1 — 2026-06-23

**Goal:** Complete SG-01: fix the four degree conventions, verify a separating
toy example, and establish an observable route to intermediate degrees.

**Prediction (written before running anything):** The four notions will require
explicit choices of quotient ring, homogenization, monomial order, and
algorithm. A hand-built exact Macaulay computation should expose first degree
falls and the Macaulay solving degree for tiny systems, while an instrumented
Buchberger implementation should demonstrate that an algorithm's traced
maximum degree is a separate implementation statistic.

**Positive result criterion:** Exact row-space or Gröbner-basis calculations
reproduce every number in the toy example and a smoke test finishes in under
10 seconds.

**Negative result criterion:** No toy system can be validated with the locally
available exact-arithmetic tools, or the proposed definitions cannot be made
compatible with the primary sources without leaving an unresolved ambiguity.

**Did:**
- Fixed the first fall, Hilbert-function regularity, solving-degree, and concrete algorithm-trace conventions in `NOTES.md`.
- Checked four primary sources and added per-paper notes plus global bibliography entries.
- Implemented `code/measure_toy_degrees.py` with exact finite-field row reduction, closed Macaulay spaces, a toy first-fall check, monomial regularity, and a traceable Buchberger run.
- Ran `env/check_env.py`, the 13 shared-library tests, the 2 P1.3 tests, and bytecode compilation.

**Found:**
- [PROVED] For the worked system over $\mathbb F_5$, $d_{\mathrm{ff}}=3$, $\operatorname{sd}_{\mathrm{grevlex}}=4$, $d_{\mathrm{reg}}=8$, and the specified naïve Buchberger trace reaches degree 9.
- [PROVED] The problem prompt's parenthetical identification of degree of regularity with solving degree is false without extra hypotheses; the worked system separates them by 4.
- [EMPIRICAL: q=5, one deterministic system] The script reproduces $3,4,8,9$, SymPy 1.14.0 returns the expected Gröbner basis, and both P1.3 regression tests pass in under one second.
- [EMPIRICAL: local environment on 2026-06-23] Sage, Singular, and msolve are unavailable; all 13 shared-library tests pass under Python 3.13.4.

**Prediction vs. outcome:** Matched. Explicit quotient/order/algorithm choices were necessary, and exact Macaulay closure exposed the degree-3 fall and degree-4 Gröbner-basis containment.

**Did not work:** Preferred Gröbner executables were unavailable. The prescribed exact Python fallback was sufficient for SG-01.

**Changed my mind about:** A single quantity called “degree of regularity” cannot safely be copied from the experimental literature. Kousidis–Wiemers' highest Magma step degree belongs in the algorithm-trace column under the conventions fixed here.

**Next:** Start SG-02 by auditing the existing shared Semaev implementation, adding $f_6$, and producing validated degree and term counts.
