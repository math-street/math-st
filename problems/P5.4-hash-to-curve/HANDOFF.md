# Handoff - P5.4 - after session 3

## State in five lines

[PROVED] The compile-time-family partial result covers the three requested presentations, both exceptional invariants, one cubic extension, and bounded characteristic-two/three routes.
[EMPIRICAL: 144,210 registered two-map field pairs] Prime-field, cubic-extension, and small-characteristic pipelines clear into their declared prime-order subgroups with complete support.
[EMPIRICAL: one compiled $p=11$ suite] All maps, complete group pairs, and pipeline pairs match Python; audited assembly has no divide or non-loop conditional jump.
[EMPIRICAL: compiled timing, 400 rounds] Ratio $1.000555$, paired-bootstrap interval $[0.998811,1.002232]$, permutation $p=0.524248$.
[PROVED] One universal formula, all-curves/all-extension-degrees coverage, a portable compiled family, and production curve vectors remain open under Q021/SG-11b/SG-12a.

## What is established

- [EMPIRICAL: $\mathbb F_{7^3}$, all 343 inputs] Generic SvdW matches its independent candidate/root oracle with one schedule.
- [EMPIRICAL: same cubic suite] All 102,400 group pairs and 117,649 two-map/cofactor pairs pass oracle, subgroup, support, and schedule checks.
- [CITED] Brier et al. Sections 8.1 and E supply the implemented characteristic-three square-discriminant and odd-degree binary maps.
- [EMPIRICAL: $\mathbb F_3$ and $\mathbb F_{2^n}$, $n=3,5,7$] The maps pass all 174 registered inputs/probes; the binary maximum fiber is six.
- [EMPIRICAL: four small-characteristic groups] All 20,853 ordered group pairs and 17,481 two-map/cofactor pairs pass oracle, subgroup, support, and schedule checks.
- [EMPIRICAL: Rust $p=11$ suite] All 11 maps, 144 ordered group pairs, and 121 two-map/cofactor pairs pass; the order-three subgroup has complete support.
- [EMPIRICAL: eight earlier prime-field suites] All 9,080 field pairs pass subgroup checks, including short Weierstrass, Montgomery, Edwards, $j=0$, and $j=1728$ routes.

## What is ruled out

- [PROVED] The code is not one algebraic formula; the new characteristic-specific formulas increase the compile-time family.
- [PROVED] The toy Rust source/assembly/timing evidence is not a portable microarchitectural constant-time certificate.
- [PROVED] Even-degree binary extensions, other characteristic-three discriminant cases, and arbitrary extension degrees are not covered.
- [PROVED] Production RFC curve-suite runs violate the loaded $\log_2q\le60$ ceiling; only Appendix K.1 XMD anchors are executed.
- [PROVED] The Q012 zero-numerator RFC `sqrt_ratio` regression remains necessary.

## Next action

Q021 is the substantive research boundary: either extend the suite family to every missing small-characteristic/extension case and compile every route, or formulate and prove an impossibility result in a precise bounded-operation model. SG-12a stays conditional on lifting the shared field ceiling.

## Invariants - do not violate

- Do not call schedule invariance, assembly inspection, or a timing null result a constant-time proof.
- Do not claim indifferentiability for a raw map; require two field elements, two maps, complete addition, and cofactor clearing.
- Keep production-size curve execution outside the repository unless the ceiling is explicitly lifted.
- Preserve the masked binary $x=0$ totalization and Q012 zero-numerator regression.
- Check actual cofactor images and subgroup support, not just $n=hr$.

## Files that matter

- `lib/finite_fields.py`: fixed polynomial-basis arithmetic, compatibility API, and extension SvdW.
- `lib/small_characteristic.py`: characteristic-two/three maps and masked complete laws.
- `code/validate_extension_svdw.py`, `code/validate_small_characteristic.py`, `code/validate_small_characteristic_pipelines.py`: new exhaustive validators.
- `code/validate_extension_pipeline.py`: cubic-extension complete-law and two-map/cofactor exhaustion.
- `code/ct_backend_p11.rs`, `code/validate_compiled_backend.py`, `code/measure_compiled_timing.py`: compiled backend, code-generation audit, and timing screen.
- `COVERAGE.md`, `UNIFICATION.md`, `INDIFFERENTIABILITY.md`, `NOTES.md`: exact scope and proof boundary.

## What I would tell my replacement

The engineering partial result is now broad and end-to-end at toy scale. The remaining gap is genuinely universal: missing curve/field regimes and portability of constant-time realization, not another unchecked toy example.

## Final validation

- [PROVED] All 70 shared tests, all 37 P5.4 tests, bytecode compilation, and every new smoke path pass under Python 3.13.4.
