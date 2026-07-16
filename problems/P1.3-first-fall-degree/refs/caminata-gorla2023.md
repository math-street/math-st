# Caminata and Gorla (2023)

Alessio Caminata and Elisa Gorla, “Solving degree, last fall degree, and
related invariants,” *Journal of Symbolic Computation* 114 (2023), 322–335.
DOI: 10.1016/j.jsc.2022.05.001; arXiv:2112.05579v2.

## Results used here

[CITED] Definitions 1.1, 1.3, and 1.4 give the solving-degree, modified
first-fall-degree, and Hilbert-function degree-of-regularity conventions used
in `NOTES.md`.

[CITED] Theorem 3.1 identifies solving degree for a degree-compatible order
with the maximum of last fall degree and the maximum degree in the reduced
Gröbner basis.

[CITED] Section 4 gives examples where the difference between first fall and
the other invariants is arbitrarily large in either direction.

[CITED] Example 4.2 proves, for odd $q>3$, a family with
$d_{\mathrm{ff}}=3$, $\operatorname{sd}=q-1$, and
$d_{\mathrm{reg}}=2q-2$, even after compatible field equations are added.

## Boundary of the citation

[CITED] The examples establish failure of the general first-fall heuristic;
they do not analyze the specific Semaev systems constructed in this
repository.

## Local verification

[EMPIRICAL: $q=5$, one deterministic system] `measure_toy_degrees.py`
reproduces Example 4.2's three invariants and additionally records a specified
naive Buchberger trace.
