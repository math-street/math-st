# Castryck--Decru 2023

Wouter Castryck and Thomas Decru, "An Efficient Key Recovery Attack on SIDH,"
EUROCRYPT 2023, Part V; IACR ePrint 2022/975.

## Main result in repository notation

[CITED] Given a degree-$3^b$ secret map and its images on a basis of
$2^a$-torsion, the basic decision construction uses an evaluable auxiliary
isogeny of degree $2^a-3^b$ to build a reducible $(2^a,2^a)$-isogeny from a
product (Sections 3--4).

[CITED] Kani reducibility gives a decision test, and a search-to-decision
reduction recovers the secret isogeny (Sections 4 and 6).

## Assumptions and conveniences

[CITED] Efficient construction/evaluation of the auxiliary isogeny is a real
algorithmic hypothesis; a known starting endomorphism ring is one route to it
(Sections 4--5).

[CITED] SIKE's explicit small endomorphism, 2-power leaked torsion, and Richelot
formulas make the concrete attack fast but are not asserted as universal
requirements (Introduction and Section 11).

## What it rules out and leaves open

[CITED] The paper breaks SIDH/SIKE and related protocols exposing comparable
torsion images and known degree, but says its route does not obviously adjust
to CRS/CSIDH or SQIsign (Section 2).

## Verification status

[CITED] The theorem statements and algorithm inputs were checked in the paper.
No attack computation was reproduced in this repository.

