---
attempt: A001
status: completed
---
# A001 — Separate four degree notions on an exact toy system

## Idea

Choose a small finite-field system for which filtered Macaulay spaces, the
homogeneous top ideal, a Gröbner basis, and an explicit algorithm trace can all
be computed exactly.

## Prior art

[CITED] Caminata and Gorla (2023, *Journal of Symbolic Computation*) give rigorous
definitions of solving degree and degree of regularity and examples separating
first fall degree from other invariants; arXiv:2112.05579 is the checked
preprint record.

## Plan

1. Implement exact finite-field row reduction and Macaulay spaces.
2. Search a small deterministic family for a compact separating example.
3. Verify the chosen values independently with SymPy's Gröbner-basis routine.
4. Record what depends on the system, order, and algorithm.

## Execution log

- Checked the four definitions and the terminology mismatch against Caminata–Gorla (2023), Hodges–Petit–Schlather (2014), and Kousidis–Wiemers (2019).
- Specialized Caminata–Gorla Example 4.2 to $q=5$.
- Implemented exact modular RREF, closed Macaulay spaces, the required degree-3 syzygy check, monomial-top-ideal regularity, and a naïve Buchberger trace.
- Ran two regression tests and the shared library's thirteen tests; all passed.

## Outcome

[PROVED] The system in `NOTES.md` has four different measured quantities:
$d_{\mathrm{ff}}=3$, $\operatorname{sd}_{\mathrm{grevlex}}=4$,
$d_{\mathrm{reg}}=8$, and
$D_{\mathrm{naive\ Buchberger}}=9$.

[EMPIRICAL: q=5, one deterministic system] The implementation reproduces all
four values and SymPy 1.14.0 independently returns the stated Gröbner basis.

[PROVED] The reusable Macaulay closure is sufficient for tiny solving-degree
experiments. The first-fall helper is sufficient only for the pre-Koszul
degree-3 witness; general Semaev use requires quotienting the full trivial
syzygy subspace.
