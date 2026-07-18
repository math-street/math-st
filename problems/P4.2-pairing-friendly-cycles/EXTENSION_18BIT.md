# Frozen 18-bit extension - P4.2 session 2

This file was written before either 18-bit search was run.

## Fixed and changed axes

[PROVED] The only primary-space change is the exclusive prime bound, from
\(2^{16}\) to \(2^{18}\). The searches retain distinct primes at least 5,
exact embedding degrees \(K=\{3,\ldots,12\}\), the Hasse and ordinarity
conditions, the rho convention, directed 3-cycle orientation, candidate-row
rules, and exact embedding-degree checks from `SEARCH_SPACE.md` and
`THREE_CYCLE_CONDITIONS.md`.

[PROVED] A hit is new relative to session 1 exactly when at least one field
prime is at least \(2^{16}\), because the new enumeration strictly contains
the old one.

## Validation rule

[CONJECTURE] Every newly appearing full hit will be instantiated within 20,000
seeded coefficient trials per curve. Both Hasse/BSGS counting and direct
equation enumeration must match every target order before the hit is treated
as exhibited. An exhausted construction search is a pipeline failure, not a
non-existence result.

## Predeclared search prediction

[CONJECTURE] The larger range will add MNT-pattern 2-cycle hits with degree
pairs in {(6,4),(4,6)}, but it will add no 2-cycle outside those two degree
patterns and no full directed 3-cycle. Either kind of new exceptional hit
refutes this prediction.

