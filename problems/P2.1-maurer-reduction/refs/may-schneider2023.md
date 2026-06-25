# May--Schneider 2023

[CITED] Alexander May and Carl Richard Theodor Schneider, "Dlog is
Practically as Hard (or Easy) as DH -- Solving Dlogs via DH Oracles on EC
Standards," *IACR Transactions on Cryptographic Hardware and Embedded
Systems* 2023(4), 146--166, DOI 10.46586/tches.v2023.i4.146-166; IACR ePrint
2023/539.

Primary text checked at:
<https://eprint.iacr.org/2023/539>

## Result in P2.1 notation

[CITED] The paper calls the assumed smooth auxiliary curve the non-uniform
part of Maurer's reduction and implements the remaining implicit arithmetic
and discrete-log recovery for current standardized groups.

[EMPIRICAL: 13 standard groups of at most 256 bits] Random curve sampling,
Schoof point counting, and factorization found auxiliary cyclic curves with
largest prime factors of at most 39 bits within at most $10^6$ samples for the
reported at-most-256-bit cases.

[HEURISTIC] Its runtime analysis models curve orders as approximately uniform
Hasse-interval integers and transfers the global smoothness probability to
that interval; a proved contrary curve-order distribution would falsify this
model.

## Assumptions and limits

[CITED] The construction is a finite practical search and does not claim a
worst-case polynomial-time algorithm for every prime.

## Verification performed

[EMPIRICAL: primary PDF Sections 1--2 and 5 inspected 2026-06-25] The
non-uniformity statement, random-search algorithm, sample counts, and
smoothness heuristic were checked directly.
