# Notes - P5.4

## Stable facts

- [EMPIRICAL: $p\in\{11,13,29,37\}$, all inputs] Direct SSWU and Montgomery Elligator 2 matched independent direct-formula oracles and returned on-curve points for all 90 inputs in each map family (`code/validate_rfc_maps.py`, `data/validate_rfc_maps_p11-13-29-37_20260704.csv`).
- [EMPIRICAL: same range] Each fixed public field and curve produced exactly one recorded high-level operation schedule across all inputs (same script and data file).
- [EMPIRICAL: Python 3.13.4, $p=11$, 240 randomized rounds, batch 100, seed 5402] Elligator 2 had exceptional/ordinary mean-time ratio $1.01162$ with paired-bootstrap 95% CI $[0.99911,1.02450]$, while SSWU had ratio $0.99121$ with CI $[0.98059,1.00210]$ (`code/measure_map_timing.py`).
- [EMPIRICAL: $p\in\{11,13,29,37\}$, ordinary/$j=0$/$j=1728$, all 270 inputs] SvdW matched its independent oracle, returned on-curve outputs, and had one high-level schedule per fixed fixture (`code/validate_svdw.py`).
- [EMPIRICAL: primes $5\le p<100$] The exhaustive degree-3/5 search tested 62,664 nonsingular $AB\ne0$ curves and 45,166 rational kernels and found 1,492 quotients with $j=0$ or $j=1728$ (`code/search_exceptional_isogenies.py`).
- [EMPIRICAL: eight toy suites, all 9,080 field pairs] Two maps, addition, and cofactor clearing always landed in the declared prime-order subgroup, with complete subgroup support (`code/validate_hash_pipeline.py`, `code/validate_curve_transports.py`).
- [EMPIRICAL: $\mathbb F_{7^3}$, all 343 inputs] Extension-field SvdW matched its branch-using candidate/root oracle and used one schedule (`code/validate_extension_svdw.py`).
- [EMPIRICAL: same cubic suite, all 102,400 group pairs and 117,649 field pairs] Complete masked addition and the two-map/cofactor pipeline matched oracles, passed order-five subgroup checks, and reached all five subgroup points (`code/validate_extension_pipeline.py`).
- [EMPIRICAL: $\mathbb F_3$ and $\mathbb F_{2^n}$, $n=3,5,7$, 174 registered inputs/probes] The small-characteristic maps remained on-curve with one schedule, and the binary maps had maximum observed fiber six (`code/validate_small_characteristic.py`).
- [EMPIRICAL: compiled $p=11$ suite] All 11 maps, 144 ordered group pairs, and 121 two-map/cofactor outputs matched Python; all final outputs lie in the order-three subgroup (`code/validate_compiled_backend.py`).
- [PROVED] Two RFC 9380 Appendix K.1 SHA-256 XMD vectors pass; production curve-suite vectors remain prohibited by the shared field-size ceiling.

## Working definitions

- A **schedule trace** is the ordered tuple of named high-level field operations executed by a mapping implementation.
- An **oracle map** is a deliberately direct, branch-using transcription used only to check the straight-line implementation at toy scale.

## Scope decision

- [PROVED] The scaffold limits experiments to $\log_2 q\leq60$, while every elliptic-curve suite in RFC 9380 Appendix J uses a production-size field larger than that ceiling. The appendix suite list and the scaffold bound are sufficient to check this incompatibility.
- [PROVED] Consequently, executing an RFC 9380 suite vector in this session would violate the loaded scaffold. Session 1 validates the RFC mapping formulas against exhaustive toy-scale oracles and leaves production-vector execution open.

## Generic `sqrt_ratio` zero discrepancy

- [PROVED] The fixture $p=11$, $E:y^2=x^3+x+1$, $Z=6$ satisfies the four direct-SSWU predicates in RFC 9380 Section 6.6.2. The nonzero squares modulo 11 are $\{1,3,4,5,9\}$, so 6 is nonsquare and $6\ne-1$; the values of $x^3+x+6$ for $x=0,\ldots,10$ are $6,8,5,3,8,4,8,4,9,7,4$, so the cubic has no root and is irreducible; finally, $B/(ZA)=2$ and $g(2)=0$, which is square under RFC Section 4's definition.
- [PROVED] For $u\in\{0,3,8\}$, the SSWU exceptional denominator $Z^2u^4+Zu^2$ is zero and the prescribed candidate is $x_1=2$ with ordinate zero. This follows by direct substitution modulo 11.
- [PROVED] On numerator zero and nonzero denominator, every temporary feeding line 12 of RFC 9380 F.2.1.1 is zero, so the published test `tv5 == 1` returns false. Appendix F.2 then selects the other candidate and returns $(0,0)$ on this fixture, but $g(0)=1$, so that pair is off-curve.
- [PROVED] The local helper restores the stated `sqrt_ratio` contract with the non-short-circuit arithmetic predicate `(tv5 == 1) | (numerator == 0)`. Its zero regression and all exhaustive oracle comparisons pass in `code/tests/test_rfc_maps.py`.

> **Gap.** I do not know whether an unstated precondition was intended or the RFC pseudocode needs a technical erratum. Resolving this requires checking the derivation with the RFC authors. Blocking: no. Logged as Q012.

## Constant-time interpretation

- [PROVED] The mapping source has no branch whose condition depends on the field input $u$: all input predicates feed `cmov_mod`, while explicit Python `if` statements validate public curve parameters or toggle tracing. This is a source-level statement about `lib/curves.py`.
- [PROVED] The code has no input-indexed table lookup; the only cached lookup is keyed by the public modulus to obtain a quadratic non-residue. This is a source-level statement about `lib/curves.py`.
- [PROVED] Python's arbitrary-precision arithmetic, `pow`, equality, boolean conversion, and interpreter dispatch are not certified constant-time here. Therefore schedule invariance must not be promoted to a side-channel claim.
- [EMPIRICAL: Python 3.13.4, $p=11$, 240 randomized rounds] Neither timing-class comparison excluded ratio one at the paired-bootstrap 95% level; the intervals were $[0.99911,1.02450]$ for Elligator 2 and $[0.98059,1.00210]$ for SSWU. This is a null result for one interpreter run, not a constant-time certificate.

## Generic SvdW fallback

- [CITED] RFC 9380 Sections 6.1, 6.6.1, and F.1 specify SvdW as the generic Weierstrass fallback and give an exceptional-safe straight-line procedure (Faz-Hernandez et al. 2023).
- [PROVED] `map_to_curve_svdw` follows the Appendix F.1 candidate construction and uses arithmetic conditional moves for both candidate selection and sign normalization.
- [EMPIRICAL: 12 fixtures and all 270 inputs] The implementation matched a separately structured branch-using candidate oracle; 30 exceptional denominators and all three candidate positions occurred in the combined data.
- [EMPIRICAL: $p=7$, $E:y^2=x^3+x+1$] No base-field element satisfies all SvdW $Z$ predicates. This finite counterexample prevents interpreting the parameter finder as universally successful over every tiny prime field.

## Exceptional-invariant isogenies

- [EMPIRICAL: primes below 100] Both exceptional target families occur abundantly among the 1,492 exhaustive degree-3/5 quotient hits.
- [EMPIRICAL: fixed $p=29$ path] SSWU on $E':y^2=x^3+4x+11$ with $Z=10$, followed by the 3-isogeny with kernel generator $(15,16)$, maps all 29 inputs to nonidentity points on $E:y^2=x^3+9$.
- [EMPIRICAL: fixed $p=59$ path] SSWU on $E':y^2=x^3+2x+13$ with $Z=18$, followed by the 3-isogeny with kernel generator $(41,35)$, maps all 59 inputs to nonidentity points on $E:y^2=x^3+56x$.
- [EMPIRICAL: the two fixed paths] Their quotient orders equal their source orders, their kernels are exact, and every one of 4,500 source-point pairs satisfies the homomorphism equation (`code/validate_isogeny_workarounds.py`).

## Full toy composition

- [PROVED] `code/hash_pipeline.py` implements RFC-shaped SHA-256 XMD expansion, prime-field `hash_to_field`, distinct suite DSTs, two map calls, addition, and scalar cofactor clearing.
- [EMPIRICAL: six short-Weierstrass suites, all 8,982 field pairs] Direct SSWU, direct SvdW, and both exceptional-invariant isogeny paths landed in the declared order-three or order-five subgroup for every pair.
- [EMPIRICAL: Montgomery and twisted-Edwards $p=7$ suites, all 98 field pairs] Direct Elligator 2 and its Edwards transport landed in the declared order-three subgroup for every pair.
- [EMPIRICAL: the six short-Weierstrass histograms] Every subgroup point occurs, with exact total-variation distance from uniform between $0.00394477$ and $0.19977018$. These tiny exhaustive distributions are diagnostics, not a security proof.
- [CITED] The conditional theorem and its checked obligations are separated from empirical evidence in `INDIFFERENTIABILITY.md` (Faz-Hernandez et al. 2023, RFC 9380, Sections 3 and 10.1).

## Extended timing

- [EMPIRICAL: Python 3.13.4, 160 randomized rounds, batch 80, seed 5408] The six class-A/class-B mean ratios ranged from $0.965472$ to $0.995130$ and every paired-bootstrap interval intersected the preregistered $[0.8,1.25]$ detector band (`code/measure_extended_timing.py`).
- [EMPIRICAL: same run] Elligator-to-Edwards had ratio $0.965472$ with 95% interval $[0.938731,0.995440]$, and $j=0$ SvdW had ratio $0.971669$ with interval $[0.944756,0.999858]$; these unadjusted intervals lie just below one.
- [PROVED] The detected few-percent Python timing differences do not contradict fixed high-level schedules and do not establish a field-operation leak or a production constant-time implementation.

## Extension and small-characteristic branches

- [CITED] Brier et al. Section 8.1 uses the ordinary characteristic-three model $y^2=x^3+a x^2+b$ and two square-discriminant candidates; Appendix E uses three candidates, trace, and half trace for ordinary binary curves over odd-degree extensions (CRYPTO 2010 full version, IACR ePrint 2009/340).
- [PROVED] The binary implementation evaluates all three candidates and uses masked first-valid selection. When a candidate has $x=0$, it masks to the unique point $(0,\sqrt b)$ instead of evaluating the undefined quotient by $x^2$.
- [EMPIRICAL: $n=3,5,7$] All 17,472 pairs in the fixed-loop binary multiplier matched the original branch-using multiplier.
- [EMPIRICAL: four registered groups, all 20,853 ordered pairs and 17,481 field pairs] Masked complete group laws and two-map/cofactor pipelines matched branch-using oracles, passed prime-subgroup annihilation, and reached every subgroup point.
- [PROVED] The implemented routes do not cover even binary extension degree or the other characteristic-three discriminant cases.

## Compiled toy backend

- [PROVED] `code/ct_backend_p11.rs` specializes all field and curve constants at compile time and has no explicit secret-path branch or indexed access in its exported map, complete-add, or pipeline functions.
- [EMPIRICAL: rustc 1.93.1, recorded x86-64 Windows target] Optimized delimited assembly contains no integer divide and no non-loop conditional jump. Eight fixed-loop `jne` back edges remain.
- [EMPIRICAL: 400 randomized-order rounds, batch 1,000, seed 5409] The registered class ratio was $1.000555$, paired-bootstrap interval $[0.998811,1.002232]$, and paired sign-permutation $p=0.524248$.
- [PROVED] Source/assembly audits and a timing null result on one target do not prove portable microarchitectural constant time.

## Final scope verdict

- [PROVED] The repository achieves the compile-time-family partial-credit target for the three requested forms and both exceptional invariants in toy prime fields of characteristic greater than three.
- [PROVED] Session 3 adds one cubic extension, bounded characteristic-two/three routes, and one end-to-end compiled suite.
- [PROVED] It still does not achieve the formal universal construction: distinct formulas remain; the small-characteristic routes cover only stated subfamilies/degrees; production curve vectors are outside the scaffold; and the entire compile-time family lacks a portable constant-time backend.
