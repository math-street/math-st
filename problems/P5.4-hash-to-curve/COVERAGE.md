# Coverage matrix - P5.4 sessions 1-3

## Mathematical applicability in characteristic greater than three

| Target presentation | Direct SSWU | SSWU via isogeny | Elligator 2 | Generic fallback |
|---|---|---|---|---|
| Short Weierstrass, $A B\ne0$ | [CITED] Applies when the suite constant $Z$ satisfies the four RFC predicates (RFC 9380, Section 6.6.2). | [CITED] Unnecessary for applicability (RFC 9380, Section 6.6.2). | [CITED] Requires a separate eligible Montgomery presentation (RFC 9380, Section 6.7.1). | [CITED] SvdW applies directly, subject to its $Z$ predicates (RFC 9380, Sections 6.1 and 6.6.1). |
| Short Weierstrass, $A=0$, $B\ne0$ | [CITED] Does not apply directly (RFC 9380, Section 6.6.2). | [CITED] Applies after fixing an isogenous $E'$ with $A'B'\ne0$ and an explicit isogeny $E'\to E$ (RFC 9380, Section 6.6.3). | [CITED] Applies only if an eligible Montgomery presentation is supplied (RFC 9380, Section 6.7.1). | [CITED] SvdW applies directly (RFC 9380, Sections 6.1 and 6.6.1). |
| Short Weierstrass, $A\ne0$, $B=0$ | [CITED] Does not apply directly (RFC 9380, Section 6.6.2). | [CITED] Applies after fixing an isogenous $E'$ with $A'B'\ne0$ and an explicit isogeny $E'\to E$ (RFC 9380, Section 6.6.3). | [CITED] Applies only if an eligible Montgomery presentation is supplied (RFC 9380, Section 6.7.1). | [CITED] SvdW applies directly (RFC 9380, Sections 6.1 and 6.6.1). |
| Montgomery $K t^2=s^3+J s^2+s$ | [CITED] Requires conversion through a Weierstrass presentation (RFC 9380, Sections 6.1 and 6.6). | [CITED] The isogeny case is presentation-specific (RFC 9380, Section 6.6.3). | [CITED] Applies when $J K\ne0$ and $(J^2-4)/K^2$ is nonzero and nonsquare; $Z$ must be nonsquare (RFC 9380, Section 6.7.1). | [CITED] SvdW can be evaluated on an equivalent Weierstrass curve and transported by a rational map (RFC 9380, Sections 6.1 and 6.6.1). |
| Twisted Edwards $a v^2+w^2=1+d v^2w^2$ | [CITED] Requires conversion through another presentation (RFC 9380, Sections 6.1 and 6.8). | [CITED] The isogeny case is presentation-specific (RFC 9380, Sections 6.6.3 and 6.8). | [CITED] Applies through a suite-fixed eligible Montgomery equivalent and rational map (RFC 9380, Sections 6.8.1-6.8.2). | [CITED] SvdW can be evaluated on an equivalent Weierstrass curve and transported by a rational map (RFC 9380, Sections 6.1 and 6.6.1). |

## Exceptional invariants

- [PROVED] For a nonsingular short-Weierstrass curve in characteristic greater than three, the direct-SSWU coefficient precondition $AB\ne0$ excludes exactly $j=0$ and $j=1728$; the separate predicates on $Z$ still apply. Indeed,
  $$j=1728\frac{4A^3}{4A^3+27B^2};$$
  the nonzero denominator gives $j=0\iff A=0$, and subtracting the denominator from the numerator gives $j=1728\iff B=0$.
- [CITED] RFC 9380 handles $AB=0$ by moving SSWU to a suite-fixed isogenous curve with $A'B'\ne0$ and then applying an explicit rational isogeny (RFC 9380, Section 6.6.3).
- [PROVED] The RFC Montgomery model always exposes the rational point $(s,t)=(0,0)$, which has order two on a nonsingular curve; therefore a full group $E(\mathbb F_q)$ of odd prime order cannot admit this presentation over $\mathbb F_q$. Substitution puts $(0,0)$ on the curve, and Montgomery negation fixes it because $(0,-0)=(0,0)$, so it is a nonidentity point equal to its inverse.
- [CITED] The RFC Elligator 2 exceptional equation $Z u^2=-1$ can occur only when $q\equiv3\pmod4$, and the straight-line procedure replaces its candidate through a conditional move (RFC 9380, Sections 6.7.1 and F.3).

## What the current code covers

- [EMPIRICAL: $p\in\{11,13,29,37\}$, all 90 field inputs per map family] `lib/curves.py` implements prime-field direct SSWU and Montgomery Elligator 2; all outputs matched independent direct-formula oracles and were on-curve (`code/validate_rfc_maps.py`, `data/validate_rfc_maps_p11-13-29-37_20260704.csv`).
- [EMPIRICAL: same range] Each fixed curve and modulus produced one high-level operation schedule across all inputs; the recorded schedule length varied only with the public modulus because the fixed Tonelli-Shanks loop bound varies with the two-adicity of $p-1$ (same script and data file).
- [EMPIRICAL: 12 fixtures, all 270 inputs] Direct SvdW now covers ordinary, $j=0$, and $j=1728$ short-Weierstrass toy curves with independent-oracle and schedule checks (`code/validate_svdw.py`).
- [EMPIRICAL: fixed $p=29$ and $p=59$ paths] SSWU-through-isogeny covers both exceptional invariants, and the selected source-map ranges avoid the isogeny kernels (`code/validate_isogeny_workarounds.py`).
- [EMPIRICAL: $p=7$ and $p=11$ transports] Direct Elligator 2, Elligator-to-Edwards, and Weierstrass-SvdW-to-Montgomery transports pass independent-oracle and schedule checks (`code/validate_curve_transports.py`).
- [EMPIRICAL: eight suites, all 9,080 field pairs] The two-map sum and cofactor clearing land in the declared prime-order subgroups (`code/validate_hash_pipeline.py`, `code/validate_curve_transports.py`).
- [EMPIRICAL: $\mathbb F_{7^3}$, all 343 inputs] Generic-field SvdW passed its independent candidate/root oracle with one schedule (`code/validate_extension_svdw.py`).
- [EMPIRICAL: same cubic suite, all 102,400 group pairs and 117,649 field pairs] Masked complete addition and the two-map/cofactor-64 pipeline matched branch-using oracles, landed in the order-five subgroup, reached all five subgroup points, and used one schedule (`code/validate_extension_pipeline.py`).
- [EMPIRICAL: $\mathbb F_3$ and $\mathbb F_{2^n}$ for $n=3,5,7$, all 174 registered inputs/probes] The characteristic-three square-discriminant map and the odd-degree binary SvdW map passed their toy oracles with one schedule (`code/validate_small_characteristic.py`).
- [EMPIRICAL: same four pipeline fixtures, all 20,853 group pairs and 17,481 field pairs] Masked complete addition and the two-map/cofactor pipelines matched branch-using oracles, landed in prime-order subgroups, had complete subgroup support, and used one schedule per fixture (`code/validate_small_characteristic_pipelines.py`).
- [EMPIRICAL: compiled $p=11$ suite] The Rust SvdW map, all 144 ordered group pairs, and all 121 two-map/cofactor pairs matched Python; the audited assembly had no divide or non-loop conditional jump (`code/validate_compiled_backend.py`).
- [PROVED] Even-degree binary extensions, the other characteristic-three discriminant families, arbitrary extension degrees, and a compiled implementation of every route remain uncovered. The Python paths are not production constant-time code.

## Outcome against the formal requirements

- [PROVED] Sessions 1-3 meet the partial-credit criterion: a compile-time family covers every requested form and both exceptional invariants in the tested prime-field model and adds bounded small-characteristic branches, but no single formula covers them.
- [PROVED] No indifferentiability claim applies to a raw map; `code/hash_pipeline.py` now implements the required composition for the toy suites.
- [CONDITIONAL: the RFC random-oracle and primitive assumptions plus correct admissible maps, group laws, and cofactor clearing] The full composition is indifferentiable from a random oracle into the subgroup (Faz-Hernandez et al. 2023, RFC 9380, Sections 3 and 10.1; obligation table in `INDIFFERENTIABILITY.md`).
- [PROVED] The original universal statement remains unresolved because the repository lacks one uniform formula, all-curves/all-extension-degrees coverage in characteristics two and three, production curve vectors, and a portable compiled backend for the entire family.
