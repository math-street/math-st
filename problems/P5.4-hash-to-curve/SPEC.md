# P5.4 toy hash-to-curve specification

## Status and scope

- [PROVED] This document specifies the repository's compile-time toy family. It is not a universal construction, an IETF registration, or a production cryptographic API.
- [PROVED] Every executable field in this specification satisfies the loaded $\log_2 q\le60$ ceiling.
- [PROVED] Suite parameters, map choice, field representation, curve model, cofactor, and subgroup order are public compile-time values.

## Common interface

- [PROVED] A suite implements `hash_to_curve(message)` as `u = hash_to_field(message, 2)`, `Q0 = map(u[0])`, `Q1 = map(u[1])`, `R = add_complete(Q0, Q1)`, and `P = clear_cofactor(R)`.
- [CITED] This two-map/add/cofactor structure and its domain-separation and modular-reduction requirements follow RFC 9380 Sections 3 and 5.
- [PROVED] No message-dependent dispatch is permitted. A suite-construction error is raised before hashing if its public parameter predicates fail.
- [PROVED] The identity is an allowed encoded group result and is represented internally by coordinates zero plus an infinity flag in the complete toy backends.

## Conditional selection

- [PROVED] `CMOV(false, true, selector)` uses a selector in $\{0,1\}$ and returns `true` exactly when the selector is one.
- [PROVED] Candidate predicates, exceptional-denominator predicates, sign predicates, identity flags, inverse-pair flags, and doubling flags feed conditional moves rather than message-dependent source branches in the audited straight-line paths.

## Odd characteristic greater than three

- [CITED] Direct SSWU requires short-Weierstrass $AB\ne0$ plus the RFC predicates on $Z$; SSWU-through-isogeny additionally requires a public rational isogeny whose exceptional behavior is handled by the suite (RFC 9380 Sections 6.6.2--6.6.3).
- [CITED] Direct SvdW is the generic short-Weierstrass fallback subject to its public $Z$ predicates (RFC 9380 Sections 6.6.1 and F.1).
- [CITED] Direct Elligator 2 requires an eligible Montgomery model and public $Z$; twisted-Edwards output uses a suite-fixed Montgomery transport (RFC 9380 Sections 6.7--6.8 and Appendix D).
- [PROVED] The local generic `sqrt_ratio` helper additionally classifies numerator zero as square; `NOTES.md` and Q012 give the exact RFC pseudocode counterexample requiring this totalization.

## Prime-extension representation

- [PROVED] An element of $\mathbb F_{p^m}=\mathbb F_p[X]/(f)$ is encoded as `(c0,...,c[m-1])` for $\sum_i c_iX^i$, with monic public modulus $f$.
- [CITED] Extension-field sign is the low bit of the first nonzero coefficient in basis order, matching the RFC extension-field `sgn0` convention (RFC 9380 Section 4.1).
- [PROVED] The registered cubic suite is $\mathbb F_7[X]/(X^3+2)$, $E:y^2=x^3+X^2x+X^2$, and SvdW $Z=3X^2$.
- [EMPIRICAL: exhaustive point count] This curve has order 320; the registered pipeline uses cofactor 64 and subgroup order five.
- [EMPIRICAL: all 102,400 group pairs and 117,649 field pairs] Complete addition and the full cubic-extension pipeline pass oracle, subgroup, support, and schedule checks.

## Characteristic three

- [CITED] The registered ordinary model is $y^2=x^3+a x^2+b$ with $ab\ne0$ (Brier et al. 2010, Section 8).
- [CITED] For the square-discriminant route, choose nonsquare $\eta$ and $c^2=-b/a$, set $v=\eta t^2$, and evaluate $x_1=c(1-v^{-1})$ and $x_2=vx_1$; one candidate has square right-hand side (Brier et al. 2010, Section 8.1).
- [PROVED] The registered suite uses $a=1$, $b=2$, $\eta=2$, $c=1$ over $\mathbb F_3$, masked candidate selection, complete masked addition, subgroup order three, and cofactor one.

## Characteristic two

- [CITED] The registered ordinary model is $y^2+xy=x^3+a x^2+b$, $b\ne0$, over odd-degree $\mathbb F_{2^n}$ (Brier et al. 2010, Appendix E).
- [CITED] With public $w$ and $c=a+w+w^2$, the candidates are $x_1=tc/(1+t+t^2)$, $x_2=tx_1+c$, and $x_3=x_1x_2/(x_1+x_2)$; trace and half trace recover an ordinate for at least one candidate (same source).
- [PROVED] All three candidates are evaluated before masked first-valid selection. If $x_i=0$, the undefined rational ordinate expression is masked to the unique point $(0,\sqrt b)$.
- [EMPIRICAL: exhaustive point counts] The registered suites use $a=b=1$, $w=0$, degrees $n=3,5,7$, moduli `0xb`, `0x25`, `0x83`, cofactors two, and subgroup orders $7,11,71$ respectively.
- [PROVED] Binary elements are encoded as integers whose bit $i$ is the coefficient of $X^i$.

## Complete group layer

- [PROVED] The characteristic-three and binary affine laws evaluate generic-add and doubling candidates with total inversion, then mask among generic, double, infinity, and identity-input results.
- [EMPIRICAL: all 20,853 ordered pairs of the four registered small-characteristic groups] These masked laws equal independently structured branch-using group oracles.
- [EMPIRICAL: all 17,481 small-characteristic field pairs] The common two-map/add/cofactor pipeline equals its oracle, lands in the declared prime-order subgroup, reaches every subgroup point, and uses one recorded schedule per fixture.

## Compiled profile

- [PROVED] `ct_backend_p11.rs` fixes $p=11$, $E:y^2=x^3+1$, SvdW $Z=1$, subgroup order three, and cofactor four at compile time.
- [PROVED] Its exported map, complete-add, and pipeline functions contain no explicit input-dependent source branch or indexed access; field exponentiation uses a fixed 64-round loop.
- [EMPIRICAL: rustc 1.93.1, recorded x86-64 Windows target] Optimized audited functions contain no integer divide and no non-loop conditional jump, and all exhaustive Python comparisons pass.

## Security boundary

- [CONDITIONAL: RFC random-oracle/primitive assumptions and correct admissible map, group law, and cofactor clearing] An admissible RFC suite composition has the indifferentiability conclusion stated in RFC 9380 Section 10.1.
- [PROVED] The characteristic-two/three experiments do not by themselves extend that cited theorem to every curve in those characteristics.
- [PROVED] Fixed schedules, assembly inspection, and timing null results are evidence, not a portable constant-time proof.
- [PROVED] `COVERAGE.md`, `UNIFICATION.md`, and `INDIFFERENTIABILITY.md` are normative for the exact limitation of repository claims.
