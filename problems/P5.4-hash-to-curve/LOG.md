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

## Session 3 - 2026-07-20

**Goal:** Extend the construction beyond prime characteristic greater than three: first validate one true extension-field SvdW instance, then determine by construction or a precise obstruction what survives in characteristics three and two. If that boundary is stable, start the compiled fixed-width backend rather than stopping at Python.

**Prediction (written before new literature searches or experiments):**

- [CONJECTURE] A polynomial-basis implementation of $\mathbb F_{7^3}$ with fixed-loop inversion, square test, and square root will support the same SvdW straight-line formula on at least one nonsingular curve and valid $Z$, with exhaustive oracle agreement and one schedule over all 343 inputs. A refuting test is exhaustive failure to find a valid curve/$Z$ or any oracle, curve-membership, or schedule mismatch.
- [CONJECTURE] The Appendix F.1 SvdW formula will remain algebraically correct on at least one characteristic-three curve with $A\ne0$, despite RFC 9380 excluding this characteristic. A refuting test is exhaustive failure over all nonsingular short-Weierstrass curves over $\mathbb F_3$ and every candidate $Z$.
- [CONJECTURE] For characteristic two, the current map family will not transport verbatim because its divisions by two and sign/square-root conventions fail. The session will either locate and implement a cited bounded-operation binary-field map or record that the only locally constructed fallback is a fixed exhaustive selector with $\Theta(q)$ field work. A refuting construction is a validated bounded-operation map derived without an unverified literature step.

**Did:**

- [PROVED] Reconciled session 2 and reran the baseline: all 65 then-present shared tests and all 26 P5.4 tests passed under Python 3.13.4; Sage, PARI/GP, Singular, and msolve remained unavailable.
- [CITED] Located the full version of Brier--Coron--Icart--Madore--Randriam--Tibouchi, *Efficient Indifferentiable Hashing into Ordinary Elliptic Curves* (CRYPTO 2010; IACR ePrint 2009/340). Sections 8.1 and E supply the characteristic-three square-discriminant and odd-degree binary SvdW formulas used below.
- [PROVED] Added fixed-degree polynomial-basis arithmetic, extension-field sign, total inversion, fixed-exponent square root, generic-field SvdW, and a branch-using exhaustive oracle. The original operator-friendly extension-field API was retained and all its pre-existing tests pass.
- [PROVED] Added fixed-loop binary multiplication, total inversion, absolute half trace, masked element selection, the characteristic-three Section-8.1 map, and the odd-degree binary Appendix-E map with an explicit $x=0$ ordinate correction.
- [PROVED] Added deterministic validators, fixed vectors, schedule checks, source audits, and CSV output for the extension and small-characteristic branches.

**Found:**

- [EMPIRICAL: $\mathbb F_{7^3}=\mathbb F_7[X]/(X^3+2)$, all 343 inputs] On $y^2=x^3+X^2x+X^2$ with $Z=3X^2$, generic SvdW matched the independent candidate/root oracle, returned on-curve points, and produced one recorded high-level schedule (`code/validate_extension_svdw.py`). All 342 nonzero field elements passed the inversion check.
- [EMPIRICAL: $\mathbb F_3$, all 3 inputs] The cited square-discriminant formula on the ordinary curve $y^2=x^3+x^2+2$ matched its direct oracle, remained on-curve, and used one schedule (`code/validate_small_characteristic.py`).
- [EMPIRICAL: $\mathbb F_3$, all 3 inputs] The RFC F.1 algebra also happens to remain on-curve on the out-of-scope $j=0$ short model $y^2=x^3+2x+1$ with $Z=1$ and one schedule. This is only an algebraic toy probe, not an extension of RFC's cited characteristic assumptions (same script).
- [EMPIRICAL: $\mathbb F_{2^n}$ for $n\in\{3,5,7\}$, all 168 inputs and all 17,472 fixed-multiplication pairs] The Appendix-E map returned on-curve points accepted by exhaustive ordinate oracles with one schedule. Its observed maximum preimage size was six, and all three candidate positions occurred by degree five (`code/validate_small_characteristic.py`).
- [PROVED] The binary formula's published $g(x)=(x^3+a x^2+b)/x^2$ is undefined at $x=0$. Selecting the unique point $(0,\sqrt b)$ by a mask makes the formula total on the tested fixtures; without this correction, $t=0$ returns $(0,0)$ off-curve.

**Prediction vs. outcome:** [EMPIRICAL: session 3 to this point] The extension-field prediction matched exactly: the first registered $\mathbb F_{7^3}$ fixture passed all 343 inputs. The characteristic-three SvdW prediction also matched on one $j=0$ short model, but literature review changed the main ordinary-curve route to the correct $x^2$ model and its cited Section-8.1 formula. The characteristic-two prediction selected its constructive branch: a cited bounded-operation odd-degree binary map was found and exhaustively validated, so the anticipated $\Theta(q)$ fallback was unnecessary.

**Did not work:** [PROVED] Applying the odd-characteristic short-Weierstrass model as the only characteristic-three normal form would miss ordinary curves: the cited paper uses $y^2=x^3+a x^2+b$ with discriminant $-a^3b$. The implementation therefore keeps the RFC-F.1 $j=0$ probe separate from the ordinary Section-8.1 construction.

**Changed my mind about:** [CITED] Characteristic two does not force an exhaustive table selector. For odd extension degree, the binary SvdW construction uses three rational candidates plus trace and half trace, so its field-operation count is bounded independently of $q$ (Brier et al., Appendix E). [PROVED] This still does not yield one formula across all characteristics; it expands the compile-time family.

**Next:** connect the new encodings to two-map group pipelines where a complete schedule is available, then start the compiled fixed-width backend and report the exact residual universal gap.

**Compiled-backend prediction (written before implementation or compilation):**

- [CONJECTURE] A Rust `u64` backend specialized to $p=11$, $E:y^2=x^3+1$, SvdW $Z=1$, can implement field inversion/square testing/square root, the map, exception-complete masked affine addition, and cofactor-four clearing without source-level branches or indexed memory depending on either field input. A refuting test is any source-audit violation, any disagreement with the Python oracle over all 121 input pairs, or any invalid/non-subgroup output.
- [CONJECTURE] Optimized assembly for the exported map and complete-add functions will contain no integer divide instruction. A refuting test is `div` or `idiv` in either delimited function body; this is a code-generation audit for this compiler/target only, not a cross-platform constant-time proof.

**Compiled-timing prediction (written before adding or running the harness):**

- [CONJECTURE] For the compiled $p=11$ two-map/cofactor pipeline, the fixed pair $(0,0)$ to fixed pair $(1,2)$ mean-time ratio will have a paired-bootstrap 95% interval intersecting $[0.9,1.1]$ over at least 300 randomized-order rounds, and a paired sign-permutation test will not reject equal means at $p<0.01$. Either an interval disjoint from that band or permutation $p<0.01$ refutes this detector prediction. It remains a platform-specific leakage screen, not a constant-time proof.

**Compiled-backend outcome:**

- [PROVED] `code/ct_backend_p11.rs` contains a compile-time $p=11$, $j=0$ SvdW suite using `u64` field elements, masked candidate selection, exception-complete masked affine addition, two-map addition, and fixed cofactor-four clearing. The exported secret paths contain no Rust `if`, `match`, `while`, or indexed access; exponentiation uses a public fixed 64-round loop.
- [EMPIRICAL: rustc 1.93.1 on the recorded x86-64 Windows target] All 11 map outputs, all 144 ordered group pairs (including the identity, inverse pairs, doubling, and the order-two point), and all 121 two-map/cofactor pairs match the Python oracle. Every final output is killed by subgroup order three and all three subgroup points occur (`code/validate_compiled_backend.py`).
- [EMPIRICAL: same compiler/target] The delimited optimized assembly for the map, complete addition, and pipeline contains zero integer divides and zero non-loop conditional jumps. Eight conditional jumps remain; the combined source/assembly audit identifies them as fixed-count exponentiation-loop back edges. This is not a microarchitectural constant-time certificate.
- [EMPIRICAL: same process, 400 randomized-order rounds, batch 1,000, seed 5409] The $(0,0)$ to $(1,2)$ mean-time ratio was $1.000555$ with paired-bootstrap 95% interval $[0.998811,1.002232]$ and paired sign-permutation $p=0.524248$ (`code/measure_compiled_timing.py`). Both preregistered timing criteria passed.

**Compiled prediction vs. outcome:** [EMPIRICAL: registered compiler and toy suite] Both predictions matched: exhaustive correctness/source checks passed, optimized assembly used no divide instruction, and the timing interval/permutation detector did not distinguish the registered input classes. [PROVED] The result is one compiled toy suite, not a portable certified backend for every field/model.

**Small-characteristic pipeline prediction (written before group-law implementation or pair exhaustion):**

- [CONJECTURE] The registered characteristic-three curve has order three, and the registered binary curves for odd degrees $3,5,7$ have orders $14,22,142$ respectively; masked exception-complete affine laws will agree with branch-using group oracles on every ordered group pair. A refuting test is any order mismatch or group-law mismatch.
- [CONJECTURE] Two independent map evaluations followed by complete addition and public cofactor clearing (cofactor one in characteristic three, cofactor two in the binary cases) will land in prime-order subgroups of orders $3,7,11,71$ for every one of the $3^2+8^2+32^2+128^2=17,481$ field pairs, with one recorded schedule per fixture and complete subgroup support. Any failed annihilation, second schedule, or missing subgroup point refutes this prediction.

**Small-characteristic pipeline outcome:**

- [EMPIRICAL: four registered groups, all 20,853 ordered group pairs] Masked complete addition agreed with independent branch-using laws on the order-$3$, order-$14$, order-$22$, and order-$142$ groups, including identities, inverse pairs, and doubling (`code/validate_small_characteristic_pipelines.py`).
- [EMPIRICAL: all 17,481 field pairs] Two maps, complete addition, and cofactor clearing matched the branch-using pipeline oracle and were annihilated by subgroup orders $3,7,11,71$. Every subgroup point occurred and each fixed fixture produced one recorded schedule (same script).
- [EMPIRICAL: full run on Python 3.13.4] The four-fixture exhaustion took 13.831443 seconds; smoke mode (characteristic three and $\mathbb F_{2^3}$) took 0.016523 seconds.

**Small-characteristic prediction vs. outcome:** [EMPIRICAL: registered fields] Both predictions matched exactly, including the preregistered group orders, prime subgroup orders, complete support, and schedule count. [PROVED] This closes the two-map/group/cofactor obligation for these four toy fixtures but not for all curves or extension degrees.

**Extension-pipeline addendum:**

- [EMPIRICAL: preliminary exhaustive $x$ count before group implementation] The registered $\mathbb F_{7^3}$ curve has 320 rational points, factoring as $64\cdot5$.
- [CONJECTURE] A masked complete extension-field affine law will match a branch-using oracle on all $320^2=102,400$ ordered group pairs. A refuting test is any mismatch, including an identity, inverse, doubling, or order-two case.
- [CONJECTURE] For all $343^2=117,649$ SvdW input pairs, two maps, complete addition, and six fixed doublings (cofactor 64) will agree with the branch-using pipeline oracle, be annihilated by subgroup order five, reach all five subgroup points, and use one schedule. Any failed equality, annihilation, support, or schedule check refutes this prediction.

**Extension-pipeline outcome:**

- [EMPIRICAL: all $320^2=102,400$ ordered group pairs] Masked extension-field complete addition matched the branch-using oracle, including every exceptional group-law case (`code/validate_extension_pipeline.py`).
- [EMPIRICAL: all $343^2=117,649$ field pairs] Two SvdW maps, complete addition, and cofactor 64 matched the oracle, every output was killed by subgroup order five, all five subgroup points occurred, and the composed schedule had one variant (same script).
- [EMPIRICAL: Python 3.13.4] The full cached-Cayley-table exhaustion took 11.145540 seconds; the 1,024-pair smoke check took 0.076104 seconds.

**Extension prediction vs. outcome:** [EMPIRICAL: registered cubic suite] Both predictions matched, so the cubic extension now has the same toy two-map/group/cofactor evidence as the prime and small-characteristic fixtures. [PROVED] This is one extension degree and curve, not arbitrary extension-field coverage.

**End-of-session audit:**

- [PROVED] All 70 shared library tests and all 37 P5.4 tests pass under Python 3.13.4; bytecode compilation and every new smoke path pass.
- [PROVED] Full data files exist for the cubic extension maps/pipeline, small-characteristic maps/pipelines, compiled correctness/assembly audit, and compiled timing screen. `SPEC.md` and `TOY_VECTORS.md` give the requested RFC-style partial specification and toy vectors.
- [PROVED] No `[UNVERIFIED]` marker or unfinished placeholder remains in the P5.4 record. Q021, SG-11b, and the ceiling-conditional SG-12a state the residual boundary without calling the formal universal problem solved.

**Next:** The next non-redundant research step is either an all-curves/all-degrees small-characteristic and extension construction plus a portable compiled realization of every route, or an impossibility theorem in a precisely defined bounded-operation model. Production RFC curve-suite vectors remain conditional on lifting the shared ceiling.
