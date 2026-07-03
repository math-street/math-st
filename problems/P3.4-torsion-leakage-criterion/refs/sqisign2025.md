# SQIsign specification 2.0.1 (2025)

SQIsign team, *SQIsign: Algorithm Specifications and Supporting Documentation*,
version 2.0.1, 2025-07-07.

## Protocol fact used by P3.4

[CITED] The public key contains $E_{pk}$ and a deterministic-basis hint, while
the secret ideal and the change-of-basis matrix encoding the secret isogeny's
torsion action remain in the secret key (Sections 4.3 and 4.6).

[CITED] The signature describes a response isogeny from the commitment curve to
the challenge curve; version 2 uses interpolation data and abelian-surface
computations for that response (Sections 1.2--1.3 and 4.4--4.6).

[CITED] The specification states that its endomorphism-ring problem is not
affected by the polynomial-time attacks on SIDH (Section 1.1).

## Checklist interpretation

[PROVED] Publishing an efficient representation of the response map does not,
without a derivation, satisfy the classifier field
`target_action_derivable` for the distinct long-term map $\phi_{sk}$.

**Proof.** The source and target maps have different named endpoints and roles
in the specification; the classifier binds leakage to one candidate target map.

