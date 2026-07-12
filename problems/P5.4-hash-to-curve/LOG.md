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

## Session 2 - 2026-07-12

**Goal:** Complete SG-08a, then connect the generic exceptional-invariant path to subgroup-cleared two-map hashing and determine precisely which formal requirements remain outside the characteristic-greater-than-three prime-field model.

**Prediction (written before implementation or new experiments):**

- [CONJECTURE] RFC 9380 Appendix F.1 SvdW will map every input to an on-curve point on valid toy $j=0$ and $j=1728$ fixtures with one recorded schedule per fixed fixture. A refuting test is any exhaustive oracle mismatch, off-curve output, or second schedule variant.
- [CONJECTURE] A compile-time suite descriptor can unify dispatch, cofactor clearing, and the two-map sum across direct SSWU, SvdW, and Elligator 2, but it will still contain distinct map formulas and therefore will meet only the problem's stated partial-credit criterion. A refuting construction is one parameter substitution that makes the three implemented formulas identical without changing their target presentations.
- [CONJECTURE] Exhaustive search below $p=100$ will find at least one rational odd-degree isogeny into a toy $j=0$ target and one into a toy $j=1728$ target from source curves with nonzero short-Weierstrass coefficients. A refuting test is exhaustive failure over all nonsingular source curves, degrees 3 and 5, and primes $5\le p<100$.

**Did:**

- [PROVED] Reconciled session 1 and reran the baseline: all 55 then-present shared tests and all 10 P5.4 tests passed under Python 3.13.4.
- [PROVED] Implemented RFC Appendix F.1 SvdW, its public-parameter finder, an independent branch-using oracle, exhaustive fixtures, fixed outputs, and source/schedule tests.
- [PROVED] Added an exhaustive odd-degree Vélu search and selected SSWU-to-3-isogeny workarounds whose source-map ranges avoid their kernels and whose target groups admit nontrivial prime-subgroup cofactor clearing.
- [PROVED] Implemented RFC-shaped SHA-256 XMD, prime-field `hash_to_field`, six short-Weierstrass compile-time suites, two-map addition, and cofactor clearing.
- [PROVED] Added Montgomery/Weierstrass and Montgomery/twisted-Edwards rational transports, a toy Edwards group model, Montgomery and Edwards two-map suites, and exhaustive transport/group-law checks.
- [PROVED] Added `INDIFFERENTIABILITY.md` and `UNIFICATION.md` to separate the cited conditional theorem, empirical checks, and the unsatisfied universal requirements.
- [PROVED] Added and ran the extended randomized timing experiment after recording its detector band below.

**Extended timing prediction (written before the extended measurements):**

- [CONJECTURE] For SvdW, both exceptional-invariant SSWU-isogeny paths, the generic Montgomery transport, and the Elligator-to-Edwards transport, the fixed-input class-A/class-B mean-time ratio will have a paired-bootstrap 95% interval intersecting $[0.8,1.25]$ after 160 randomized rounds of batches of 80 calls. A refuting result is an interval wholly below $0.8$ or wholly above $1.25$. This deliberately broad detector concerns the recorded Python process only and is not a constant-time certificate.

**Found:**

- [EMPIRICAL: $p\in\{11,13,29,37\}$, 12 fixtures, all 270 inputs] SvdW returned on-curve points equal to the independent oracle with one schedule per fixed fixture; the data include 30 exceptional denominators and use all three candidate positions (`code/validate_svdw.py`).
- [EMPIRICAL: all nonsingular $AB\ne0$ curves over primes $5\le p<100$, all rational 3/5-subgroups] The search tested 62,664 curves and 45,166 kernels and found 1,492 $j=0$ or $j=1728$ quotients (`code/search_exceptional_isogenies.py`).
- [EMPIRICAL: fixed $p=29$ and $p=59$ paths] Both SSWU ranges avoid the selected kernels; all 88 map inputs and 4,500 homomorphism pairs pass (`code/validate_isogeny_workarounds.py`).
- [PROVED] The empty-message and `abc` outputs of SHA-256 XMD equal RFC 9380 Appendix K.1; these official byte-level vectors do not violate the field-size ceiling.
- [EMPIRICAL: six short-Weierstrass suites, all 8,982 field pairs] Every two-map sum followed by cofactor multiplication lies in the declared prime-order subgroup, and every subgroup point occurs (`code/validate_hash_pipeline.py`).
- [EMPIRICAL: $p=7$ Montgomery and twisted-Edwards suites, all 98 field pairs] Both form-specific pipelines land in the declared order-three subgroups; 3,744 group-law checks pass (`code/validate_curve_transports.py`).
- [EMPIRICAL: Python 3.13.4, 160 rounds, batch 80, seed 5408] The six extended timing ratios range from $0.965472$ to $0.995130$ and every 95% interval intersects the preregistered $[0.8,1.25]$ band. Elligator-to-Edwards and $j=0$ SvdW have unadjusted intervals just below one (`code/measure_extended_timing.py`).
- [PROVED] The common suite interface retains three distinct core formulas; it is a compile-time family and not a single uniform construction (`UNIFICATION.md`).
- [PROVED] Characteristics two and three, extension fields, production curve-suite vectors, and a compiled constant-time field/complete group backend remain outside the achieved result. Q021 records this blocking gap.

**Prediction vs. outcome:** [EMPIRICAL: session 2] All three main predictions matched within their registered toy ranges: every SvdW fixture passed; both exceptional isogeny families were found abundantly; and the common wrapper still dispatches among distinct formulas. [EMPIRICAL: same session] The extended timing prediction also matched its broad detector, although two small intervals excluded one and were recorded as runtime differences rather than suppressed.

**Did not work:** [PROVED] The first safe-range isogeny fixtures had target orders 27 and 36. Multiplication by the naive cofactors 9 and 12 collapsed the whole rational group to the identity because the target groups had too much rational 3-torsion. Requiring a prime factor $r$ with $r\nmid h$ and exhaustively checking the cofactor image produced the replacement order-30 and order-60 fixtures over $p=29$ and $p=59$.

**Changed my mind about:** [CITED] RFC Appendix D makes SvdW plus model transport a more useful generic fallback than the prompt's obstruction summary suggests (Faz-Hernandez et al. 2023). [EMPIRICAL: one $p=7$ curve] A valid SvdW $Z$ is not automatic on every tiny field, so this fallback must still be a suite construction with verified parameters, not an unqualified universal formula.

**Next:** Treat SG-10a and SG-11a as separate research tasks: first add extension-field and characteristic-two/three constructions with independent toy oracles, then move the surviving compile-time family to a compiled constant-time field and complete group backend. Production curve vectors remain deferred unless the shared ceiling is explicitly lifted.
