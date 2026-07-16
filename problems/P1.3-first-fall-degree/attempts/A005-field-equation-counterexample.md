---
attempt: A005
status: completed
---
# A005 - Refuting automatic field-equation nonredundancy

## Outcome

[REFUTED] Nonsingularity and a non-base target do not force the field equations
to enlarge the quadratic Semaev core ideal. There is an infinite family of
eligible counterexamples for every odd prime power $q\equiv3\pmod4$, $q\ge7$.

Consequently the former candidate equality

\[
d_{\mathrm{ff}}=5,\qquad d_{\mathrm{reg}}=
\operatorname{sd}_{\mathrm{grevlex}}=q
\]

is false without the nonredundancy hypothesis. The unconditional statement is

\[
d_{\mathrm{ff}}=5,\qquad d_{\mathrm{reg}}=q,\qquad
\operatorname{sd}_{\mathrm{grevlex}}\le q.
\]

The exact exceptional condition is that the $q$-Frobenius of the eight-
dimensional core quotient is the identity, equivalently that both field-
equation normal forms vanish. Because the core is symmetric in $x,y$, one
field equation belongs to the core if and only if the other does.

## Infinite genuine-Semaev family

Let $q\equiv3\pmod4$, $q\ge7$, and write
$\mathbb F_{q^2}=\mathbb F_q[u]/(u^2+1)$. Choose
$h\in\mathbb F_q^\times\setminus\{1,-1\}$ and put

\[
\rho=\frac{h+h^{-1}}2,\qquad
\sigma=\frac{h^{-1}-h}2,\qquad a=-4\sigma^2.
\]

Then $\rho^2-\sigma^2=1$. Since $-1$ is not a square, $\rho\ne0$; the
restriction on $h$ gives $\sigma\ne0$. Hence

\[
E:Y^2=X^3+aX
\]

is nonsingular. The point

\[
R=(2u,\,2\rho(1-u))
\]

lies on $E$, since both sides of the curve equation are $-8\rho^2u$.
Its $x$-coordinate is not in $\mathbb F_q$.

For $T=2u$, the two coordinates of $f_3(x,y,T)$ generate the same ideal as

\[
H_0=(xy-a)^2-4(x-y)^2,\qquad
H_1=(x+y)(xy+a).
\]

The algebraic-closure zero set consists of the following eight ordered pairs,
all in $\mathbb F_q^2$:

\[
\begin{aligned}
 &(z,-z),\quad z\in
 \{\pm2(1+\rho),\ \pm2(1-\rho)\},\\
 &(2\sigma(\rho+\sigma),2\sigma(\rho-\sigma)),
   (2\sigma(\rho-\sigma),2\sigma(\rho+\sigma)),
\end{aligned}
\]

together with the negatives of the last two pairs. The first branch follows
from $x+y=0$; the polynomial in $x^2$ has roots
$4(1+\rho)^2$ and $4(1-\rho)^2$. The second branch follows from
$xy=-a=4\sigma^2$ and has sums $\pm4\sigma\rho$ and discriminant
$16\sigma^4$. All points are distinct. A collision between the two branches
would give a square root of $-1$ in $\mathbb F_q$.

The audited universal Groebner basis has standard monomials

\[
1,y,y^2,y^3,x,xy,xy^2,x^2
\]

because its only specialization factor is
$(m_1^2-4m_0)t_1^2/4=-4\ne0$ here. Thus the core quotient has dimension
eight. Eight distinct zeros force it to be reduced and split, so it is
isomorphic to $\mathbb F_q^8$. Therefore $x^q-x$ and $y^q-y$ belong to the
core ideal.

## Smallest concrete counterexample

Take $q=7$, $h=2$, so $\rho=3$, $\sigma=1$, and $a=3$. With
$\mathbb F_{49}=\mathbb F_7[u]/(u^2+1)$, use

\[
E:Y^2=X^3+3X,\qquad R=(2u,6+u).
\]

The two core generators are

\[
\begin{aligned}
G_0&=x^2y^2+3x^2+2xy+3y^2+2,\\
G_1&=3x^2y+3xy^2+2x+2y.
\end{aligned}
\]

For grevlex $x>y$, their reduced basis is

\[
\begin{aligned}
&xy^3-3x^2+xy-2,\quad y^4-3y^2+2,\\
&x^3+x+y^3+y,\quad x^2y+xy^2+3x+3y.
\end{aligned}
\]

Exact division gives zero normal forms for both $x^7-x$ and $y^7-y$.
The closed degree-4 core space has rank four and does not contain the second
and third displayed basis elements; the degree-5 space contains all four.
Hence

\[
(d_{\mathrm{ff}},d_{\mathrm{reg}},
\operatorname{sd}_{\mathrm{grevlex}})=(5,7,5).
\]

This is a counterexample inside the actual on-curve Semaev family, not merely
inside an abstract family with the same top-degree shape.

## Exhaustive and symbolic checks

- [EMPIRICAL: exhaustive $q=5$] No redundant case among 6,228 eligible
  systems.
- [EMPIRICAL: exhaustive $q=7$] Exactly six redundant cases among 50,376
  eligible systems; every survivor of the eight-zero filter has zero field-
  equation normal forms.
- [EMPIRICAL: exhaustive $q=9$] No redundant case among 236,160 eligible
  systems. This includes the smallest non-prime odd prime power in scope.
- [PROVED: symbolic certificate] `code/certify_quadratic_field_equations.py`
  checks the infinite-family identities over
  $\mathbb Z[1/2,h,h^{-1},u]/(u^2+1)$ and certifies the exact $q=7$ normal
  forms, multiplication matrices, and closed spaces.

The exhaustive data are in
`data/search_quadratic_redundancy_20260716.json`.
