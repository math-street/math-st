# Basso et al. 2024 — SQIsign2D-West

Andrea Basso, Pierrick Dartois, Luca De Feo, Antonin Leroux, Luciano Maino,
Giacomo Pope, Damien Robert, and Benjamin Wesolowski, "SQIsign2D-West: The
Fast, the Small, and the Safer," IACR ePrint 2024/760.

## Constructive use

[CITED] The paper explicitly repurposes higher-dimensional SIDH attack
techniques to represent and evaluate response isogenies by torsion
interpolation (Introduction and Section 2).

[CITED] Key generation publishes the public-key curve but keeps the secret
ideal and internal torsion evaluations in the secret key (Section 4.1,
Algorithm 4).

## Checklist interpretation

[PROVED] This is a negative control for post-hoc fitting: the presence of Kani
machinery and public response interpolation does not pass the target-map action
test for the long-term secret isogeny.

**Proof.** The classifier tests evaluations of $\phi_{sk}$, whereas the
published interpolation data describe $\phi_{rsp}$; no equality or derivation
between these restrictions is supplied.

