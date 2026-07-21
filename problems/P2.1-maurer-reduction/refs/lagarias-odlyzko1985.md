# Lagarias--Odlyzko 1985

[CITED] Jeffrey C. Lagarias and Andrew M. Odlyzko, "Solving Low-Density
Subset Sum Problems," *Journal of the ACM* 32(1), 229--246, 1985, DOI
10.1145/2455.2461.

Primary text checked at:
<https://citeseerx.ist.psu.edu/document?doi=a6275a6f1566e88ef611c71bb220c6c2b3bc0cf5&repid=rep1&type=pdf>

## Results relevant to P2.1

[CITED] The paper defines density as
$d=n/\log_2(\max_i a_i)$ and analyzes an LLL-based recovery algorithm for
almost all subset-sum instances below a fixed low-density threshold.

[CITED] The lattice algorithm always halts in polynomial time but does not
always recover an existing solution.  Its proved success statement is
distributional, not a worst-case theorem for high-density or repeated-weight
instances.

## Verification performed

[EMPIRICAL: primary-source audit 2026-07-21] The abstract, density definition,
main success theorem, and stated limitation of the algorithm were checked in
the full paper; journal metadata was cross-checked on the author's publication
page and through the DOI.
