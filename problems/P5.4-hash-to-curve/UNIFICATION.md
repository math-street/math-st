# Unification outcome - P5.4

## Compile-time interface

- [PROVED] `code/hash_pipeline.py` gives every registered suite the same external stages: `hash_to_field(msg, 2)`, two `map_field_element` calls, point addition, and cofactor clearing.
- [PROVED] The map choice is a public suite parameter fixed before any message or field input is processed.
- [PROVED] The current family contains three genuinely distinct core formulas: SSWU, SvdW, and Elligator 2. The SSWU-isogeny and Montgomery/Edwards transports add fixed public rational maps.

| Target case | Compile-time route | Toy validation |
|---|---|---|
| Short Weierstrass, $AB\ne0$ | [PROVED] direct SSWU or SvdW | all registered inputs and pair sums |
| Short Weierstrass, $j=0$ | [PROVED] direct SvdW or SSWU plus a fixed 3-isogeny | $p=29$ full toy suite |
| Short Weierstrass, $j=1728$ | [PROVED] direct SvdW or SSWU plus a fixed 3-isogeny | $p=59$ full toy suite |
| Eligible Montgomery | [PROVED] direct Elligator 2 | $p=7$ full toy suite |
| Other Montgomery in the RFC model | [PROVED] SvdW on the equivalent Weierstrass curve plus Appendix D.2 transport | $p=11$ map validation |
| Twisted Edwards with eligible Montgomery equivalent | [PROVED] Elligator 2 plus Appendix D.1 transport | $p=7$ full toy suite |
| Odd-characteristic cubic extension | [PROVED] Generic-field SvdW | $\mathbb F_{7^3}$ full two-map/group domain |
| Characteristic-three ordinary, square discriminant | [CITED] Brier et al. Section 8.1 two-candidate map | $\mathbb F_3$ full two-map/group domain |
| Characteristic-two ordinary, odd extension degree | [CITED] Brier et al. Appendix E three-candidate map with masked $x=0$ totalization | $\mathbb F_{2^n}$ for $n=3,5,7$ full two-map/group domains |
| Compiled fixed-width end-to-end path | [PROVED] SvdW, complete masked affine addition, and cofactor-four clearing | $p=11$, all 121 field pairs |

## Verdict

- [PROVED] This is a compile-time family, not one parameter substitution into one algebraic formula: the source of `map_field_element` dispatches among distinct SSWU, SvdW, and Elligator 2 routines.
- [CITED] RFC 9380 itself standardizes the same kind of suite-specific map choice and recommends different maps by presentation and performance goal (Faz-Hernandez et al. 2023, Sections 6.1 and 8).
- [PROVED] The implementation therefore meets the prompt's partial-credit criterion but not its stronger uniformity condition.
- [PROVED] SvdW plus rational model conversion is the smallest generic route implemented here for prime fields of characteristic greater than three, but it still requires suite-specific $Z$, conversion constants, and exceptional-safe transports.
- [PROVED] The small-characteristic additions increase, rather than remove, compile-time diversity: they use trace/half-trace or a characteristic-specific $x^2$ model unavailable to the odd-characteristic RFC formulas.
- [PROVED] The Rust result establishes a complete compiled path for one suite only; it does not turn the whole interface into a portable constant-time family.
