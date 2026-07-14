# Bowe 2017 — earliest surviving `pairing` root commit

**Reference. [CITED]** Sean Bowe, `pairing` repository, root commit
`a06216f24b488fa2a25b42366cb3d3614218a7b5`, July 8, 2017.
<https://github.com/zkcrypto/pairing/commit/a06216f24b488fa2a25b42366cb3d3614218a7b5>

**Relevant source facts. [CITED]** The committed BLS12-381 README states
\(q<2^{383}\), \(r<2^{255}\), \(u\bmod72\in\{16,64\}\), and a preference for
low Hamming weight. It says \(u=-\mathtt{0xd201000000010000}\) produces the
largest \(q\) and smallest Hamming weight satisfying the stated requirements.
It derives the G1 and G2 generators using lexicographically smallest valid
coordinates followed by cofactor scaling.

**Archival boundary. [CITED]** The reachable Git history has this zero-parent
commit as its root, approximately four months after the March 11 announcement;
no earlier reachable selection script or rejected-candidate transcript is
present in that repository history.

**Audit use. [PROVED]** The generator rule removes a package-only ambiguity
conditional on the curve core. The prose does not completely define a finite
\(u\)-domain, the required power-of-two threshold, or the priority/tie rule for
its optimization objectives, so it does not identify the historical menu
size.
