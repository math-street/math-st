---
attempt: A001
status: folded-into-A002
---
# A001 - RFC maps with exhaustive toy validation

## Idea

Transcribe the straight-line SSWU and Elligator 2 maps from RFC 9380, but
instantiate them only over prime fields below the shared ceiling. Validate each
implementation against a simpler branch-using oracle for every input in each
selected toy field.

## Prior art

- [CITED] RFC 9380 Appendix F gives straight-line SSWU and Elligator 2 procedures, including their exceptional-case conditional moves (Faz-Hernandez et al. 2023, RFC 9380, Sections F.2 and F.3).
- [CITED] RFC 9380 requires $A\ne0$ and $B\ne0$ for direct SSWU and recommends an isogenous auxiliary curve when $AB=0$ (Faz-Hernandez et al. 2023, Sections 6.6.2-6.6.3).
- [CITED] RFC 9380 states Elligator 2 for Montgomery curves $K t^2=s^3+J s^2+s$ subject to $J K\ne0$ and a non-square discriminant predicate (Faz-Hernandez et al. 2023, Section 6.7.1).

## Plan

1. Add minimal Montgomery and mapping helpers to shared `lib/curves.py`.
2. Add independent direct-formula oracles in the problem test module.
3. Exhaust every input on at least two valid curves per mapping.
4. Record deterministic CSV summaries and the observed operation schedules.

## Execution log

- The prediction and falsifiers were recorded in `LOG.md` before environment checks or experiments.
- [PROVED] The environment baseline passed all 41 pre-existing shared tests before the mapping work began.
- [PROVED] Added prime-field `inv0`, `sgn0`, arithmetic conditional move, fixed-loop Tonelli-Shanks, generic `sqrt_ratio`, direct SSWU, a Montgomery curve type, and Elligator 2 to `lib/curves.py`.
- [EMPIRICAL: $p\in\{11,13,29,37\}$, all inputs] Both map families passed exhaustive on-curve, independent-oracle, and schedule-invariance checks (`code/validate_rfc_maps.py`).
- [PROVED] The first run falsified the unmodified generic `sqrt_ratio` path on the zero numerator; the derivation and local correction are recorded in `NOTES.md` and Q012.
- [EMPIRICAL: Python 3.13.4, $p=11$, 240 randomized timing rounds] Both timing ratios stayed within the preregistered 10% band and both paired-bootstrap 95% intervals included one (`code/measure_map_timing.py`).

## Outcome

[PROVED] SG-01a through SG-01c, SG-02a, and the Python-level SG-06a are complete at toy scale, with production RFC suite vectors deferred by the global parameter ceiling. [PROVED] A002 supplies the later isogeny, form-transport, cofactor-clearing, and full-hashing layers, so this attempt is folded into A002.
