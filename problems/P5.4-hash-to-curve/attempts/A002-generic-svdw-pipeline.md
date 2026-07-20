---
attempt: A002
status: promising
---
# A002 - Generic SvdW and subgroup-cleared two-map pipeline

## Idea

Use the RFC SvdW straight-line map as the characteristic-greater-than-three
fallback for all short-Weierstrass coefficients, then wrap all implemented maps
behind compile-time suite objects that perform the two-map sum and cofactor
clearing.

## Prior art

- [CITED] RFC 9380 Sections 6.1 and 6.6.1 recommend SvdW when a generic mapping is required and give its parameter predicates.
- [CITED] RFC 9380 Appendix F.1 gives a straight-line SvdW implementation using conditional moves.
- [CITED] RFC 9380 Section 3 defines `hash_to_curve` as two map evaluations, point addition, and cofactor clearing.

## Plan

1. Implement and exhaustively validate SvdW on ordinary, $j=0$, and $j=1728$ toy curves.
2. Search for toy isogeny sources mapping into both exceptional-invariant targets.
3. Add compile-time suite wrappers and subgroup-membership tests.
4. Record the exact boundary of the indifferentiability argument.

## Execution log

- Predictions and falsifiers are in `LOG.md` before implementation.
- [EMPIRICAL: $p\in\{11,13,29,37\}$, 12 fixtures, all 270 inputs] SvdW matched the independent branch-using oracle, stayed on-curve, and produced one high-level schedule on ordinary, $j=0$, and $j=1728$ curves (`code/validate_svdw.py`).
- [EMPIRICAL: all nonsingular $AB\ne0$ curves over primes $5\le p<100$, all rational 3/5-subgroups] The exhaustive search tested 62,664 curves and 45,166 kernels and found 1,492 quotients with $j=0$ or $j=1728$ (`code/search_exceptional_isogenies.py`).
- [EMPIRICAL: fixed $p=29$ and $p=59$ workarounds] Both selected SSWU ranges avoided their isogeny kernels; 88 map inputs and 4,500 group-law pairs passed (`code/validate_isogeny_workarounds.py`).
- [EMPIRICAL: six short-Weierstrass suites, all 8,982 field pairs] Every two-map sum followed by cofactor multiplication landed in the declared prime-order subgroup, and every subgroup point occurred (`code/validate_hash_pipeline.py`).
- [EMPIRICAL: toy Montgomery and twisted-Edwards suites over $p=7$] All 98 field pairs cleared into the declared order-three subgroups; direct-oracle, rational-transport, and group-law checks passed (`code/validate_curve_transports.py`).
- [PROVED] Two RFC 9380 Appendix K.1 `expand_message_xmd(SHA-256)` vectors pass in `code/tests/test_svdw_pipeline.py`.
- [CITED] `INDIFFERENTIABILITY.md` records the RFC composition theorem and checks the structural hypotheses without promoting the tiny toy instances to cryptographic security claims.

## Outcome

[PROVED] The attempt achieves the problem's partial-credit target: a small compile-time family covers all three requested curve forms and both exceptional invariants in the characteristic-greater-than-three prime-field toy model. [PROVED] It does not produce one formula, cover extension fields or characteristics two and three, execute production curve vectors, or certify Python/group arithmetic as constant-time. The exact boundary is in `UNIFICATION.md` and `INDIFFERENTIABILITY.md`.
