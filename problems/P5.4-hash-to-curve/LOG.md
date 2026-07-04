# Log - P5.4

## Session 1 - 2026-07-04

**Goal:** Complete SG-01a through SG-01c at toy scale: implement the RFC 9380
straight-line SSWU and Elligator 2 maps, validate them exhaustively against
independent direct-formula oracles, and record exact applicability failures.

**Prediction (written before running anything):**

- [CONJECTURE] For valid toy parameters, both implementations will return an on-curve point for every field input, including the specified exceptional inputs. A refuting test is any input on any preregistered curve for which the implementation raises, disagrees with the direct-formula oracle, or returns an off-curve point.
- [CONJECTURE] SSWU will require $A B\ne0$, whereas Elligator 2 will require a Montgomery presentation with rational 2-torsion and the RFC parameter predicates. A refuting test is a valid invocation outside these predicates or a failure inside them after exhaustive input testing.

**Timing addendum prediction (written before timing measurements):**

- [CONJECTURE] On the fixed $p=11$ fixtures, the exceptional-input/ordinary-input mean-time ratio will remain within 10% of one for both maps after batching at least 100 calls per observation. A refuting test is a bootstrap 95% confidence interval lying entirely below 0.9 or above 1.1. This prediction concerns only the recorded Python process and says nothing about compiled constant-time behavior.

**Did:**

- Initialized the problem record and selected exhaustive toy-field validation as the smallest unresolved sub-goal.
- [CITED] Recorded RFC 9380 as the algorithm specification and test-vector source (Faz-Hernandez et al. 2023, RFC 9380).
- [PROVED] Ran the environment baseline before implementation: all 41 pre-existing shared tests passed under Python 3.13.4; Sage, Singular, and msolve were unavailable.
- [PROVED] Added prime-field constant-schedule building blocks, direct SSWU, a Montgomery curve model, and Elligator 2 to `lib/curves.py`.
- [PROVED] Added independently structured branch-using formula oracles, fixed known outputs, exhaustive tests, invalid-parameter tests, an AST source audit, and deterministic CSV generation under `code/`.
- [CITED] Built `COVERAGE.md` from the exact applicability conditions in RFC 9380 Sections 6.1 and 6.6-6.8.
- [PROVED] Added a randomized-block timing script with a paired-round percentile bootstrap and preregistered its 10% effect threshold before execution.
- [PROVED] The end-of-session validation passed all 53 then-present shared tests, all 10 P5.4 tests, both smoke paths, the full exhaustive validator, and bytecode compilation.

**Found:**

- [EMPIRICAL: $p\in\{11,13,29,37\}$, all 180 map inputs] Every straight-line output was on-curve and exactly matched its independent oracle (`code/validate_rfc_maps.py`, `data/validate_rfc_maps_p11-13-29-37_20260704.csv`).
- [EMPIRICAL: same range] Each fixed public curve and modulus produced exactly one recorded high-level schedule across all inputs; 6 SSWU exceptional inputs and 2 Elligator 2 exceptional inputs were included (same script and data).
- [PROVED] The audited mapping paths contain no source-level branch or indexed memory access depending on the field input; `code/tests/test_rfc_maps.py` checks the relevant ASTs. This does not imply that the Python runtime is constant-time.
- [PROVED] RFC 9380 Appendix F.2.1.1 misclassifies a zero numerator as non-square on the admissible fixture $p=11$, $E:y^2=x^3+x+1$, $Z=6$, causing unmodified Appendix F.2 to return an off-curve pair for $u\in\{0,3,8\}$. `NOTES.md` gives the complete modular calculation, and Q012 records the external confirmation gap.
- [PROVED] The direct-SSWU coefficient precondition excludes exactly $j=0$ and $j=1728$ in characteristic greater than three; the independent predicates on $Z$ remain, and `COVERAGE.md` derives the coefficient statement from the short-Weierstrass $j$ formula.
- [EMPIRICAL: Python 3.13.4, $p=11$, 240 randomized rounds, batch 100, seed 5402] Elligator 2's exceptional/ordinary mean-time ratio was $1.01162$ with paired-bootstrap 95% CI $[0.99911,1.02450]$; SSWU's ratio was $0.99121$ with CI $[0.98059,1.00210]$ (`code/measure_map_timing.py`, `data/measure_map_timing_p11_s240_b100_seed5402_20260704_summary.csv`).

**Prediction vs. outcome:** [EMPIRICAL: session 1] The on-curve/oracle prediction matched only after the zero-numerator correction; the verbatim generic RFC helper falsified it first. The applicability prediction matched the RFC predicates and the exhaustive fixtures, but the session did not test extension fields or characteristics two and three. The timing addendum matched its preregistered 10% threshold for both maps, and both paired-bootstrap intervals included one.

**Did not work:** [PROVED] A verbatim transcription of RFC 9380 F.2.1.1 returned `isQR = False` at numerator zero and made SSWU fail on three inputs of the $p=11$ fixture. The local arithmetic-OR correction restores the stated helper contract and passes the exhaustive regression.

**Changed my mind about:** [CITED] The prompt's obstruction summary underplays RFC's generic SvdW fallback: RFC 9380 explicitly recommends SvdW when a generic map is required (RFC 9380, Section 6.1). [PROVED] The remaining implementation gaps are uniform transport, low-level constant-time realization, exceptional target presentations, subgroup handling, and the scope beyond RFC's field assumptions; `COVERAGE.md` inventories them.

**Next:** Implement the RFC Appendix F.1 SvdW straight-line fallback and exhaust it on toy $j=0$ and $j=1728$ curves; use that result to decide whether isogeny work or a generic fallback is the better unification route.
