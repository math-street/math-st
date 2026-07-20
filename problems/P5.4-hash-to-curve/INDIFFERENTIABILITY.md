# Indifferentiability boundary - P5.4

## The cited composition

- [CITED] RFC 9380 Section 3 defines `hash_to_curve` by obtaining two field elements with `hash_to_field(msg, 2)`, mapping both, adding the points, and clearing the cofactor (Faz-Hernandez et al. 2023, RFC 9380).
- [CITED] RFC 9380 Section 10.1 states that this composition is indifferentiable from a random oracle when `hash_to_field` is itself indifferentiable from a random oracle; it also explicitly permits the identity output (Faz-Hernandez et al. 2023, RFC 9380).
- [CITED] RFC 9380 Sections 5.2 and 5.3 require bias-controlled modular reduction without rejection sampling, a conforming message expander, and domain separation (Faz-Hernandez et al. 2023, RFC 9380).

## Obligations and checks

| Obligation | Repository check | Verdict |
|---|---|---|
| Two independently expanded field elements | [PROVED] `hash_to_field_sha256(msg, 2, ...)` consumes disjoint $L$-byte substrings of one RFC XMD expansion. | checked structurally |
| Conforming expander | [PROVED] The empty-message and `abc` SHA-256 XMD outputs equal RFC 9380 Appendix K.1. | checked on two official vectors |
| Bias bound | [CITED] The implemented $L=\lceil(\lceil\log_2p\rceil+128)/8\rceil$ modular-reduction rule has bias at most $2^{-128}$ under the RFC model (RFC 9380, Section 5). | cited, not statistically inferred |
| Domain separation | [PROVED] Every toy suite has a distinct nonempty DST of at least 16 bytes. | checked by the validator |
| Admissible deterministic map | [EMPIRICAL: every input of the registered toy fields] SSWU, SvdW, Elligator 2, isogeny, and rational-transport outputs pass direct-oracle and on-curve checks. | checked at toy scale |
| Two-map sum | [PROVED] Every suite calls its map twice before addition. | checked by source inspection and exhaustive pair tests |
| Cofactor clearing | [EMPIRICAL: 9,080 field pairs across eight suites] Every output is annihilated by the declared prime subgroup order and the cofactor image has the declared size. | checked at toy scale |
| Correct group operations | [EMPIRICAL: 4,500 isogeny homomorphism pairs and 3,744 transported-form group-law checks] The selected toy laws and transports passed exhaustive checks. | checked at toy scale |
| Compiled complete group path | [EMPIRICAL: $p=11$, all 144 ordered group pairs] The masked Rust law agrees with the affine oracle, including identities and exceptional pairs. | checked for one toy suite |
| Small-characteristic composition | [EMPIRICAL: four fixtures, all 17,481 field pairs] Two maps, masked complete addition, and cofactor clearing land in prime-order subgroups with complete support. | checked at toy scale for stated subfamilies |
| Cubic-extension composition | [EMPIRICAL: $\mathbb F_{7^3}$, all 117,649 field pairs] Two SvdW maps, masked complete addition, and cofactor-64 clearing land in the order-five subgroup with complete support. | checked for one cubic suite |

## What follows

- [CONDITIONAL: the RFC random-oracle and primitive assumptions, an admissible RFC map, correct group operations, and correct cofactor clearing] The same suite composition is indifferentiable from a random oracle into the target subgroup (Faz-Hernandez et al. 2023, RFC 9380, Sections 3 and 10.1).
- [PROVED] The raw maps alone do not meet that conclusion; `code/hash_pipeline.py` is the first repository layer that implements the required two-map composition.
- [PROVED] Exhaustive toy output histograms do not prove indifferentiability. Their total-variation distances from exact uniformity range from $0.00394477$ to $0.19977018$ because the tested groups have orders three or five; the recorded histograms are finite correctness diagnostics.
- [PROVED] The toy groups are cryptographically insecure and therefore cannot instantiate a meaningful asymptotic security theorem despite matching its control flow.

> **Gap.** [PROVED] The repository now has complete toy pipelines in characteristics two and three, but only for stated subfamilies and degrees; it does not extend the cited theorem to every such curve family. It also lacks a certified production field/group backend and one formula covering all presentations. Resolving the full formal statement requires those constructions or an impossibility result. Blocking: yes for calling P5.4 solved. Logged as Q021.
