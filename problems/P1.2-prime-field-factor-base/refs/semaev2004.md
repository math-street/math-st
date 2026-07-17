# Semaev 2004

[CITED] Igor Semaev, “Summation polynomials and the discrete logarithm problem
on elliptic curves,” IACR Cryptology ePrint Archive, Report 2004/031, 2004.
<https://eprint.iacr.org/2004/031>

## Relevance

[CITED] The paper gives the explicit third summation polynomial for short
Weierstrass curves and defines higher summation polynomials recursively by
resultants.

[CITED] Its prime-field index-calculus proposal reduces relation generation to
finding bounded solutions of explicit modular multivariate equations; the
paper's speedup is conditional on an adequate solver for those equations.

## Verification in this repository

[EMPIRICAL: F_101 fixed inputs] `lib/semaev.py` matches independently expanded
values $f_3(1,2,3)=67$, $f_4(1,2,3,4)=2$, and
$f_5(1,2,3,4,5)=51$ modulo 101 for $a=2,b=3$.
