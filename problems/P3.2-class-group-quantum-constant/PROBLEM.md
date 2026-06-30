# P3.2 — The constant in the quantum attack on class group actions

## Formal statement

[CITED] In CSIDH, an imaginary-quadratic ideal class group acts freely and transitively on the intended set of supersingular curves (Castryck et al., 2018, ASIACRYPT, DOI 10.1007/978-3-030-03332-3_15).

Let (N) denote the class-group order.

1. Under an explicit physical error-correction model, determine the leading constant and lower-order terms in a cost of the form \(\exp(c\sqrt{\log N})\) for Kuperberg-style abelian hidden-shift algorithms.
2. Prove a quantum query lower bound for group-action inversion.

## Realistic deliverable

[PROVED] This repository treats a parameterized calculator, a validated classical simulation of sieve combinatorics, and a precise account of unresolved lower bounds as partial progress rather than as a solution of either formal task; this scope follows directly from the definitions in this file.

## Validation targets

- Match a toy class-group order against reduced-form enumeration.
- Verify the toy isogeny action exhaustively for freeness and transitivity.
- Fit simulated query counts over at least five sizes and report uncertainty and residuals.
- Keep all physical-cost assumptions as named inputs.
- Reproduce a published numerical estimate only when its assumptions can be checked from a primary source.

## Scope boundary

[PROVED] Classical simulation can measure the implemented sieve's combinatorial counters, but it cannot measure quantum wall-clock cost; this is a definitional distinction between the simulator and a quantum execution.
