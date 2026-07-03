# Castryck et al. 2018 — CSIDH

Wouter Castryck, Tanja Lange, Chloe Martindale, Lorenz Panny, and Joost Renes,
"CSIDH: An Efficient Post-Quantum Commutative Group Action," ASIACRYPT 2018.

## Protocol fact used by P3.4

[CITED] A CSIDH public key is a representative of a curve class obtained by the
secret group action; the paper emphasizes that no extra torsion points are sent.

[CITED] Consequently the public transcript does not provide the restriction of
one named secret isogeny to rank-two torsion, which is a common input of the
published K2/R8 templates.

## What this does not claim

[PROVED] The P3.4 classification concerns only Kani/higher-dimensional
torsion-leakage templates and makes no assertion about independent classical or
quantum attacks on the CSIDH group action.

**Proof.** The classifier's verdict string is `NO_PUBLISHED_ROUTE`, and its
documented scope is limited to R8, K2-CD, and K2-MM.

