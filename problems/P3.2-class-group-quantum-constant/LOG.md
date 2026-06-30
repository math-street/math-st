# Experimental log

## Session 1 — 2026-06-30

**Goal:** Build a verified toy class-group action, then implement the sieve simulator, fit, cost calculator, sensitivity analysis, and lower-bound literature record.

**Prediction (written before running anything):** [CONJECTURE] The instance (p=419=4\cdot3\cdot5\cdot7-1) will be small enough for exhaustive verification, but the rational (3)-, (5)-, and (7)-isogeny steps may generate a proper subgroup of the class group; a refuting test is an orbit whose cardinality equals the reduced-form class number and whose generator maps are permutations.

**Did:**
- Ran `env/check_env.py` and all pre-existing tests in `lib/tests/` before mathematical work.
- Created the P3.2 session structure and attempt A001.
- Added shared reduced-form, curve canonicalization, Vélu quotient, rational-isogeny orbit, and permutation-group routines.
- Ran the explicit toy action at (p=59) and (p=419).
- Simulated 1,000 fixed-batch sieve trials over ten sizes and fitted leading plus lower-order terms with 2,000 bootstrap replicates.
- Built a JSON-driven logical and phenomenological surface-code calculator, published logical endpoint fixtures, and one-at-a-time sensitivity analysis.
- Checked primary literature and wrote a conditional phase-state query lower-bound proof.

**Found:**
- [EMPIRICAL: Python 3.13.4 on Windows 11, 2026-06-30] All 34 pre-existing shared-library tests passed; SageMath, Singular, and msolve were unavailable.
- [EMPIRICAL: (p=59,419)] Class numbers and explicit rational-isogeny orbit sizes match at 9 and 27, respectively, and both generated actions are regular.
- [EMPIRICAL: (N=2^n), (24\le n\le96), 100 trials per size] The fitted simplified-schedule constant is (c=2.68677) with trial-bootstrap 95% CI ([2.65454,2.71923]); the residual RMSE is 0.36454.
- [EMPIRICAL: published logical fixtures] The calculator reproduces base-two logical T-gate exponents 71.6 and 56.0.
- [CONDITIONAL: independent standard phase-state query interface] The proved success bound is (P_{\mathrm{succ}}\le2^m/N), yielding (m=\Omega(\log N)) queries for constant success.
- [EMPIRICAL: final validation on 2026-06-30] All 63 shared tests and all 10 P3.2 tests passed; five script smoke modes passed; 16 JSON files parsed; and the principal CSV has 1,000 rows, 10 sizes, and the required recorded-parameter columns.

**Prediction vs. outcome:** [EMPIRICAL: (p=419)] The prediction diverged: degrees (3,5,7) generate the full 27-element computed action rather than a proper subgroup.

**Did not work:** [EMPIRICAL: first (p=419) twist fixture] A (j=1728) twist-separation test used an exceptional automorphism class and therefore did not separate the nominal twist; using a generic Vélu quotient fixed the fixture.

**Correction during Session 1:** [EMPIRICAL: p=419] A twist-separation fixture based on the (j=1728) start curve was invalid because the chosen twist was prime-field isomorphic at this exceptional automorphism class; the test now uses a generic Vélu quotient.

**Changed my mind about:** [PROVED] Query lower bounds and time lower bounds must be treated as different tasks here, because the phase-state model already has logarithmic-query upper and lower scales while known efficient-time algorithms use subexponential resources.

**Next:** Implement the full Peikert phase-vector collimation simulator and reproduce a Figure 1 row before extending the physical model.

**Final disposition:** [PROVED] FAILED relative to the formal statement; the session produced validated partial artifacts but neither a full physically calibrated constant nor an unrestricted group-action-inversion query lower bound.
