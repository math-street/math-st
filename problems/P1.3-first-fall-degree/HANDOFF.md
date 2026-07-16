# Handoff - P1.3 - after session 4

## State in five lines

[PROVED] Every odd-prime-power quadratic non-base-target family has
$d_{\mathrm{ff}}=5$, $d_{\mathrm{reg}}=q$, and
$\operatorname{sd}_{\mathrm{grevlex}}\le q$.
[PROVED] For $q>5$, $\operatorname{sd}_{\mathrm{grevlex}}=q$ exactly when
the field equations enlarge the core ideal.
[REFUTED] Nonsingularity and an on-curve non-base target do not imply
nonredundancy; an infinite genuine-Semaev counterexample family exists.
[PROVED] The smallest certified example over $q=7$ has
$(d_{\mathrm{ff}},d_{\mathrm{reg}},\operatorname{sd})=(5,7,5)$.
[OPEN] The all-parameter $q,n,m$ bound and a symbolic $n=3,m=2$ mutant
theorem remain open.

## Exact redundancy criterion

Let $C=(G_0,G_1)$ and $A_C=\mathbb F_q[x,y]/C$. The universal core basis
has standard monomials $1,y,y^2,y^3,x,xy,xy^2,x^2$, so $\dim A_C=8$.
The following conditions are equivalent:

1. $x^q-x,y^q-y\in C$;
2. both field-equation normal forms are zero;
3. the $q$-Frobenius of $A_C$ is the identity;
4. $A_C\cong\mathbb F_q^8$;
5. all eight core zeros are distinct and in $\mathbb F_q^2$.

The core is symmetric, so the two field equations are redundant together.

## Counterexample packet

For $q\equiv3\pmod4$, $q\ge7$, let
$\mathbb F_{q^2}=\mathbb F_q[u]/(u^2+1)$, choose
$h\notin\{0,1,-1\}$, and set

\[
\rho=(h+h^{-1})/2,\quad \sigma=(h^{-1}-h)/2,\quad a=-4\sigma^2.
\]

Then $E:Y^2=X^3+aX$ is nonsingular and
$R=(2u,2\rho(1-u))$ is an on-curve point with non-base $x$-coordinate.
The core is generated, up to an invertible row scaling, by

\[
(xy-a)^2-4(x-y)^2,\qquad (x+y)(xy+a).
\]

Its eight algebraic-closure zeros are distinct base-field points, hence the
core quotient is $\mathbb F_q^8$ and both field equations are redundant.
The complete proof is `attempts/A005-field-equation-counterexample.md`.

At $q=7,h=2$, use
$E:Y^2=X^3+3X$ and $R=(2u,6+u)$. Exact normal forms are zero and the
closed degree-4 space misses two basis elements while degree 5 contains the
whole basis, proving solving degree 5.

## A004 audit

[PROVED] The normalized core basis has degrees $4,4,3,3$, leading monomials
$xy^3,y^4,x^3,x^2y$, and sole specialization factor $c+g^2$.
[PROVED] For Semaev coefficients,
$c+g^2=(m_1^2-4m_0)t_1^2/4\ne0$.
[PROVED] The strengthened certificate checks explicit representations and all
six Buchberger reductions in
$\mathbb Z[b,c,d,e,f,g,h,i][(c+g^2)^{-1}]$.
[PROVED] A quartic top-part minor has determinant $-1$, so the replacement
family has $d_{\mathrm{reg}}\le4$ after every valid specialization.
[PROVED] Division gives cubic-or-lower field remainders; the replacement
family generates the same ideal and lies in $V_{F,q}$.
[CITED] Salizzoni Proposition 3.10 gives replacement solving degree at most 5;
closed-space stability gives the original upper bound $\operatorname{sd}\le q$.
[PROVED] A003's lower bound is valid precisely under nonredundancy, because
no degree-$q$ input can enter a cutoff $d<q$.

## Finite searches

- Exhaustive $q=5$: 6,228 eligible systems, no redundant core.
- Exhaustive $q=7$: 50,376 eligible systems, exactly six redundant cores.
- Exhaustive $q=9$: 236,160 eligible systems, no redundant core.
- The older 397-case $q=5,7,11$ sample fixed a nonbase coefficient of $A$ and
  therefore missed the new base-defined counterexample family.

## Bounded $n=3,m=2$ check

[EMPIRICAL: $q=3,5,7,11$] Core bases had degree at most 3 and field
remainders degree at most 2. The replacement family had regularity and solving
degree at most 3. This is evidence only and does not complete SG-12.

## Files that matter

- `NOTES.md`: corrected theorem, proof, audit, and limitations.
- `attempts/A005-field-equation-counterexample.md`: counterexample proof.
- `code/certify_quadratic_family.py`: localized-ring A004 certificate.
- `code/certify_quadratic_field_equations.py`: infinite family and $q=7$ certificate.
- `code/search_quadratic_redundancy.py`: exhaustive $q=5,7,9$ search.
- `data/certify_quadratic_family_20260716.json`: regenerated A004 certificate.
- `data/certify_quadratic_field_equations_20260716.json`: counterexample certificate.
- `data/search_quadratic_redundancy_20260716.json`: exhaustive results.

## Resume warning

Do not state $\operatorname{sd}=q$ without nonredundancy, do not treat
$d_{\mathrm{reg}}$ as an ideal invariant (it depends on the input top parts),
and do not extrapolate this odd-characteristic $n=m=2$ classification to the
binary $n\sim\log q$ regime.
