# Maino--Martindale 2023

Luciano Maino and Chloe Martindale, "An Attack on SIDH with Arbitrary Starting
Curve," EUROCRYPT 2023, Part V; IACR ePrint 2022/1026.

## Main result in repository notation

[CITED] SSI-T supplies coprime $A,B$, public endpoints of an unknown
degree-$A$ isogeny, and its restriction to full $B$-torsion; Algorithm 1
recovers a matching secret isogeny after finding a suitable smooth-cofactor
decomposition.

[CITED] Theorem 1 packages the secret and auxiliary isogenies into a polarized
product isogeny whose kernel is determined by the leaked torsion action.

## Assumptions and conveniences

[CITED] The algorithm does not assume that the starting endomorphism ring is
known, but it does require a feasible smooth cofactor, surface-isogeny
computation, and bounded guessing parameters (SSI-T discussion and Algorithm 1).

## What it rules out and leaves open

[CITED] The paper applies to SIDH-related SSI-T instances and explicitly says
that it does not apply to protocols that publish no secret-map point images,
including CSIDH and SQIsign (Introduction).

## Verification status

[CITED] The corrected second-version Theorem 1 and Algorithm 1 inputs were
checked. No attack computation was reproduced in this repository.

