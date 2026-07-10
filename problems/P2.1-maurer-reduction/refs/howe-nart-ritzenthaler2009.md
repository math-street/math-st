# Howe--Nart--Ritzenthaler 2009

[CITED] Everett W. Howe, Enric Nart, and Christophe Ritzenthaler, "Jacobians
in Isogeny Classes of Abelian Surfaces over Finite Fields," *Annales de
l'Institut Fourier* 59(1), 239--289, 2009, DOI 10.5802/aif.2430.

Primary text checked at:
<https://www.numdam.org/item/10.5802/aif.2430.pdf>

## Results relevant to P2.1

[CITED] Theorem 1.2 gives a complete classification of the degree-four Weil
polynomials whose abelian-surface isogeny classes do not contain a genus-two
Jacobian, separately for split and simple classes.

[CITED] For ordinary prime fields the exceptional conditions reduce to the
coefficient and split-trace cases implemented in
`code/surface_jacobian_scan.py`.

[PROVED] The theorem is an existence criterion for a Jacobian inside an
isogeny class.  It does not return a genus-two equation, so satisfying its
criterion is not an explicit Maurer--Wolf auxiliary construction.

## Verification performed

[EMPIRICAL: primary-source audit 2026-07-10] The introduction, Theorems
1.2--1.4, Tables 1.1--1.2, and the ordinary/split case distinctions were
checked directly.  Published ordinary exception families are unit-test
fixtures for the implementation.
