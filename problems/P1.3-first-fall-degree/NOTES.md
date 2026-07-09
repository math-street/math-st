# Notes

## Stable facts

### Fixed conventions

[CITED] Let $k=\mathbb F_q$, $R=k[x_1,\ldots,x_N]$, and
$B_q=R/(x_1^q,\ldots,x_N^q)$. For a nonhomogeneous input system $F$,
the first fall degree used here is

\[
d_{\mathrm{ff}}(F)=\min\{d:\operatorname{Syz}(F^{\mathrm{top}})_d/
\operatorname{Triv}(F^{\mathrm{top}})_d\ne0\},
\]

where the trivial module contains the Koszul syzygies and the syzygies
$(f_i^{\mathrm{top}})^{q-1}e_i$ induced by $B_q$. This is Definition 1.3
of Caminata and Gorla (2023), following Hodges, Petit, and Schlather (2014).

[CITED] The Hilbert-function degree of regularity used here is

\[
d_{\mathrm{reg}}(F)=\min\{d:(F^{\mathrm{top}})_d=R_d\},
\]

when the top ideal is Artinian. This is Definition 1.4 of Caminata and Gorla
(2023); it is not an engine's maximum printed step degree.

[CITED] For a fixed degree-compatible order $\sigma$, the solving degree
$\operatorname{sd}_\sigma(F)$ is the least cutoff $d$ for which the
closed degree-$d$ Macaulay row space contains a $\sigma$-Gröbner basis of
$(F)$. This is Definition 1.1 of Caminata and Gorla (2023).

[CITED] Salizzoni's $V_{F,d}$ definition and the closed Macaulay construction
above are the same invariant (often called mutant solving degree in the XL
literature), not a second algorithm-trace quantity. The maximum degree printed
by a particular F4, F5, MutantXL, or Buchberger run remains the separate
$D_{\mathcal A}$ statistic below. Maximum input degree is also separate from
all three invariants.

[PROVED] A fourth quantity, $D_{\mathcal A}(F,\sigma,\theta)$, records the
largest degree processed by a specified algorithm and complete option set.
It is a run statistic, since pair criteria and preprocessing can change it
without changing the input ideal.

[CITED] The first fall degree is only a heuristic proxy for solving degree in
general. Caminata and Gorla (2023), Section 4, give families where the
difference between first fall and other degree invariants is arbitrarily large
in either direction.

### Worked separation of the four quantities

[PROVED] Over $\mathbb F_5[x_1,x_2,x_3]$, with grevlex
$x_1>x_2>x_3$, set

\[
F=\{x_1x_2+x_2,\ x_2^2-1,\ x_3^4-1,\ x_1^5-x_1\}.
\]

[PROVED] The four values are

| Quantity | Value |
|---|---:|
| $d_{\mathrm{ff}}(F)$ | 3 |
| $\operatorname{sd}_{\mathrm{grevlex}}(F)$ | 4 |
| $d_{\mathrm{reg}}(F)$ | 8 |
| $D_{\text{naive Buchberger}}(F)$ | 9 |

[PROVED] The nontrivial degree-3 relation is
$x_2(x_1x_2)-x_1(x_2^2)=0$. The degree-4 closed Macaulay space contains
$x_1+1=x_2(x_1x_2+x_2)-(x_1+1)(x_2^2-1)$, hence it contains the Gröbner
basis $\{x_1+1,x_2^2-1,x_3^4-1\}$. The top ideal
$(x_1x_2,x_2^2,x_3^4,x_1^5)$ first fills all forms in degree 8. Finally,
the stated FIFO Buchberger run processes the coprime pair with leading-monomial
LCM $x_1^5x_3^4$, of degree 9.

[CITED] This is the $q=5$ specialization of Caminata and Gorla (2023),
Example 4.2, except that the algorithm-trace value is an additional local
measurement.

## Exact Semaev and Weil pipeline

[CITED] Semaev's summation polynomials satisfy the zero-sum characterization
and recursive resultant construction used in `lib/semaev.py` and
`code/sparse_weil.py`; see Semaev (2004). Kousidis and Wiemers (2019),
Section 3, use the same construction in their binary Weil-descent setting.

[EMPIRICAL: generic $f_3,f_4,f_5$, 30-second/index ceiling] Exact sparse
expansion produced the following statistics. The generic $f_6$ expansion
was censored rather than extrapolated; the independent recursive $f_6$
evaluator still passes a six-point zero-sum test over $\mathbb F_{101}$.

| Polynomial | Status | Terms | Total degree | Degree in each $x_i$ |
|---|---|---:|---:|---|
| $f_3$ | complete | 13 | 4 | 2 |
| $f_4$ | complete | 540 | 12 | 4 |
| $f_5$ | complete | 130,705 | 32 | 8 |
| $f_6$ | censored at 30 s and 250,000-term ceiling | — | — | — |

[EMPIRICAL: fixed inputs over $\mathbb F_{101}$] The $f_3$ formula and the
$f_4$ recursive resultant agree with independently expanded fixed values;
$f_3,\ldots,f_6$ vanish on constructed point tuples summing to zero. These
checks are in `lib/tests/test_semaev.py` and `code/tests/test_sparse_weil.py`.

[PROVED] The Weil builder represents $\mathbb F_{q^n}$ in a polynomial
basis, substitutes $x_i\in\mathbb F_q$, expands
$f_{m+1}(x_1,\ldots,x_m,x_R)$, and equates its $n$ basis coordinates to
zero. This is the explicit coordinate construction of Weil restriction.

[EMPIRICAL: $q\in\{3,5,7,11,13,17,19,23\}$, recorded rows] Every reported
known-target row uses the nonsingular curve
$E:y^2=x^3+\alpha x+1$, where $\alpha$ is the polynomial-basis generator,
and its stored factor-base tuple evaluates to zero in all Weil coordinates.
The regression suite also rejects singular curve inputs.

## Measurement protocol

[PROVED] First fall is computed for the nonzero Weil coordinate equations in
$B_q$; field equations are implicit in the function-ring convention. Both
$d_{\mathrm{reg}}$ and solving degree are computed in $R$ after explicitly
adding $x_i^q-x_i$. Thus the three columns use their fixed literature
definitions rather than an F4 log label.

[PROVED] The solving-degree implementation builds the closed Macaulay space
at successive cutoffs and tests containment of a grevlex Gröbner basis with
$x_1>\cdots>x_m$. SymPy 1.14.0 supplies only the target Gröbner basis; exact
modular row reduction and closure determine the reported cutoff.

[EMPIRICAL: 34 deterministic cases] The canonical CSV contains 32 completed
rows and two stage-censored rows. It merges superseded runs by retaining the
furthest completed pipeline stage for each $(q,n,m,\text{target mode})$.

## Comparison table

[EMPIRICAL: known decompositions in the displayed range] The table below is
the known-target subset of `data/first_fall_vs_solving_20260701.csv`; every
complete row has a verified root. A dash is a censored value, not an estimate.

| $q$ | $n$ | $m$ | $d_{\mathrm{ff}}$ | $d_{\mathrm{reg}}$ | $\operatorname{sd}_{\mathrm{grevlex}}$ | $\operatorname{sd}-d_{\mathrm{ff}}$ |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 2 | 2 | 4 | 4 | 4 | 0 |
| 3 | 2 | 3 | 6 | 5 | 6 | 0 |
| 3 | 2 | 4 | 8 | 8 | 8 | 0 |
| 3 | 3 | 2 | 3 | 4 | 4 | 1 |
| 3 | 3 | 3 | 5 | 5 | 5 | 0 |
| 3 | 3 | 4 | 8 | 8 | 8 | 0 |
| 5 | 2 | 2 | 5 | 5 | 5 | 0 |
| 5 | 2 | 3 | 12 | 12 | 12 | 0 |
| 5 | 2 | 4 | 16 | 16 | — | — |
| 5 | 3 | 2 | 3 | 5 | 4 | 1 |
| 5 | 3 | 3 | 11 | 12 | 12 | 1 |
| 5 | 3 | 4 | 16 | 16 | — | — |
| 7 | 2 | 2 | 5 | 7 | 7 | 2 |
| 7 | 3 | 2 | 3 | 7 | 4 | 1 |
| 11 | 2 | 2 | 5 | 11 | 11 | 6 |
| 11 | 3 | 2 | 3 | 11 | 4 | 1 |
| 13 | 2 | 2 | 5 | 13 | 13 | 8 |
| 13 | 3 | 2 | 3 | 13 | 4 | 1 |
| 17 | 2 | 2 | 5 | 17 | 17 | 12 |
| 17 | 3 | 2 | 3 | 17 | 4 | 1 |
| 19 | 2 | 2 | 5 | 19 | 19 | 14 |
| 23 | 2 | 2 | 5 | 23 | 23 | 18 |

[EMPIRICAL: $q=3,5,7$, external targets] The canonical CSV also contains
12 completed externally selected target rows. They are secondary evidence
because some are inconsistent systems; they are not used to state the
known-solution divergence.

## Divergence result and characterization

[PROVED] For $m=n=2$, odd $q\ge5$, and a non-base target
$x_R=z_0+z_1\alpha$ with $z_1\ne0$, the top parts of the two $f_3$ Weil
coordinates have the shape

\[
g_0^{\mathrm{top}}=x_1^2x_2^2,\qquad
g_1^{\mathrm{top}}=c\,x_1x_2(x_1+x_2),\quad c=-2z_1\ne0.
\]

This follows by taking the terms of highest factor-base degree in the
published $f_3$ formula and splitting the two extension coordinates.

[PROVED] These top parts have first fall degree 5. At degree 5,

\[
(x_1+x_2)g_0^{\mathrm{top}}-c^{-1}x_1x_2g_1^{\mathrm{top}}=0.
\]

There is no relation in degree 3, and a putative degree-4 relation
$A g_0^{\mathrm{top}}+(Bx_1+Cx_2)g_1^{\mathrm{top}}=0$ has distinct
$x_1^3x_2$ and $x_1x_2^3$ coefficients forcing $B=C=0$, then $A=0$.
The first Koszul relation has degree 7 and the quotient-trivial relations
occur later, so the degree-5 relation is nontrivial.

### The corrected exact theorem for the quadratic family

[PROVED] Let $q\ge5$ be an odd prime power, write
$\mathbb F_{q^2}=\mathbb F_q[u]/(u^2+m_1u+m_0)$, and let
$T=t_0+t_1u\notin\mathbb F_q$. For arbitrary short-Weierstrass coefficients
$A,B\in\mathbb F_{q^2}$, let $G_0,G_1\in\mathbb F_q[x,y]$ be the two
coordinates of $f_3(x,y,T)$. Set

\[
F=\{G_0,G_1,x^q-x,y^q-y\},\qquad C=(G_0,G_1).
\]

[PROVED] For grevlex $x>y$ this family satisfies

\[
d_{\mathrm{ff}}(G_0,G_1)=5,\qquad
d_{\mathrm{reg}}(F)=q,\qquad
\operatorname{sd}_{\mathrm{grevlex}}(F)\le q.
\]

[CONDITIONAL: $(F)\supsetneq C$] If at least one field equation is not in
the core ideal, then

\[
\operatorname{sd}_{\mathrm{grevlex}}(F)=q.
\]

[PROVED] Since $C$ is symmetric in $x,y$, either both field equations belong
to $C$ or neither does. Let

\[
A_C=\mathbb F_q[x,y]/C.
\]

The audited core basis shows $\dim_{\mathbb F_q}A_C=8$. The following are
equivalent and give the exact redundancy condition:

1. $x^q-x,y^q-y\in C$;
2. both normal forms by the universal core basis are zero;
3. the $q$-Frobenius endomorphism of $A_C$ is the identity;
4. $A_C\cong\mathbb F_q^8$;
5. the core has eight distinct algebraic-closure zeros and all lie in
   $\mathbb F_q^2$.

Thus nonredundancy is exactly the failure of these conditions. For $q>5$,
it is also equivalent to $\operatorname{sd}_{\mathrm{grevlex}}(F)=q$:
nonredundancy gives the lower bound below, while redundancy gives
$(F)=C$ and the core basis already lies in $V_{F,5}$.

[PROVED] The regularity statement follows directly from the top ideal

\[
J=(x^2y^2,xy(x+y),x^q,y^q).
\]

[PROVED] The monomial $x^{q-1}$ shows that $J_{q-1}\ne R_{q-1}$. In degree
$q$, $x^q,y^q\in J$; every mixed $x^ay^{q-a}$ with
$2\le a\le q-2$ is divisible by $x^2y^2$. Finally,
$x^{q-3}xy(x+y)$ and $y^{q-3}xy(x+y)$ put the two boundary monomials
$x^{q-1}y$ and $xy^{q-1}$ in $J$ modulo already covered mixed monomials.
Thus $J_q=R_q$ and $d_{\mathrm{reg}}(F)=q$.

[PROVED] The solving-degree lower bound uses only the closed-space
definition. For $d<q$, the field equations cannot enter $V_{F,d}$, so
$V_{F,d}=V_{\{G_0,G_1\},d}\subseteq C$. If this space contained a
Groebner basis of $(F)$, then $(F)\subseteq C$, contradicting
$(F)\supsetneq C$. Therefore $\operatorname{sd}(F)\ge q$ under the stated
nonredundancy hypothesis.

[PROVED] For the upper bound, put $s=x+y$ and $p=xy$. The published formula
for $f_3$ becomes

\[
(s^2-4p)T^2-2\bigl(s(p+A)+2B\bigr)T+(p-A)^2-4Bs.
\]

[PROVED] Since $t_1\ne0$, elementary row operations normalize its two
coordinates to

\[
H_0=p^2+bp+cs^2+ds+e,\qquad
H_1=ps+fp+gs^2+hs+i.
\]

[PROVED] The two coefficients relevant to the exceptional specialization are

\[
c=-m_0t_1^2-t_0^2+m_1t_0t_1,qquad
g=\frac{m_1t_1-2t_0}{2},
\]

and hence

\[
c+g^2=\frac{(m_1^2-4m_0)t_1^2}{4}\ne0.
\]

[PROVED] The last inequality uses irreducibility of the odd-characteristic
quadratic modulus and $t_1\ne0$. An exact Buchberger calculation over
$\mathbb Q(b,c,d,e,f,g,h,i)$ has no nonconstant denominator except
$c+g^2$ and specializes to a four-element core basis with total degrees
$4,4,3,3$ and leading monomials

\[
xy^3,\ y^4,\ x^3,\ x^2y.
\]

[PROVED] The exact fraction-field and closed-Macaulay certificates are
generated by `code/certify_quadratic_family.py` and stored in
`data/certify_quadratic_family_20260716.json`. The strengthened certificate
checks explicit basis representations and all six Buchberger reductions over

\[
\mathbb Z[b,c,d,e,f,g,h,i][(c+g^2)^{-1}],
\]

so it is not an inference from sampled specializations. It also records a
quartic top-part minor of determinant $-1$, proving the rank claim in every
characteristic after valid specialization. Three basis elements lie in
the initial degree-5 Macaulay span; multiplying the resulting lower-degree
rows inside the closed space yields the fourth. Consequently the complete
core basis lies in $V_{\{G_0,G_1\},5}$.

[PROVED] Divide $x^q-x$ and $y^q-y$ by this core basis, obtaining remainders
$r_x,r_y$. The displayed leading monomials leave only standard monomials of
degree at most 3, so $\deg r_x,\deg r_y\le3$. Polynomial division is
degree-compatible, and the core basis is already in $V_{F,q}$; therefore
$r_x,r_y\in V_{F,q}$.

[PROVED] The mutant family

\[
F'=\{\text{four core-basis elements},r_x,r_y\}
\]

generates the same ideal as $F$, has maximum input degree at most 4, and has
degree of regularity at most 4 because its top ideal contains leading
monomials covering every degree-4 monomial. Salizzoni (2023), Proposition
3.10, therefore gives $\operatorname{sd}(F')\le5$.

[PROVED] Since $F'\subseteq V_{F,q}$ and $q\ge5$, closed-space stability
gives $V_{F',5}\subseteq V_{F,q}$. A grevlex basis of $(F')=(F)$ is thus
already in $V_{F,q}$, proving $\operatorname{sd}_{\mathrm{grevlex}}(F)\le q$.

### Automatic nonredundancy is false

[REFUTED] Nonsingularity and a non-base on-curve target do not imply that the
field equations enlarge the core. There is an infinite counterexample family.
Let $q\equiv3\pmod4$, $q\ge7$, write
$\mathbb F_{q^2}=\mathbb F_q[u]/(u^2+1)$, choose
$h\in\mathbb F_q^\times\setminus\{1,-1\}$, and put

\[
\rho=\frac{h+h^{-1}}2,\qquad
\sigma=\frac{h^{-1}-h}2,\qquad a=-4\sigma^2.
\]

The curve $E:Y^2=X^3+aX$ is nonsingular, and

\[
R=(2u,2\rho(1-u))\in E(\mathbb F_{q^2})
\]

has non-base $x$-coordinate. The two coordinates of $f_3(x,y,2u)$
generate the same ideal as

\[
H_0=(xy-a)^2-4(x-y)^2,\qquad
H_1=(x+y)(xy+a).
\]

[PROVED] The first branch $x+y=0$ gives the four points

\[
(z,-z),\quad z\in\{\pm2(1+\rho),\pm2(1-\rho)\}.
\]

The second branch $xy=-a=4\sigma^2$ gives two ordered roots with sum
$4\sigma\rho$, their swap, and the negatives of both. Its discriminant is
$16\sigma^4$. These eight points are distinct and lie in $\mathbb F_q^2$;
a collision between branches would make $-1$ a square. The universal basis
gives quotient dimension eight, hence the quotient is reduced and split:

\[
\mathbb F_q[x,y]/(H_0,H_1)\cong\mathbb F_q^8.
\]

Therefore both field equations are redundant.

[PROVED] The smallest concrete instance takes $q=7,h=2$, so
$\rho=3,\sigma=1,a=3$. Over
$\mathbb F_{49}=\mathbb F_7[u]/(u^2+1)$ use

\[
E:Y^2=X^3+3X,\qquad R=(2u,6+u).
\]

Its field-equation normal forms are both zero and exact closed-space linear
algebra gives

\[
(d_{\mathrm{ff}},d_{\mathrm{reg}},
\operatorname{sd}_{\mathrm{grevlex}})=(5,7,5).
\]

The certificate `code/certify_quadratic_field_equations.py` checks the
symbolic family over $\mathbb Z[1/2,h,h^{-1},u]/(u^2+1)$ and the concrete
normal forms, quotient multiplication matrices, and degree-4/5 closed spaces.
The full proof is in `attempts/A005-field-equation-counterexample.md`.

### Curve and target variation

[EMPIRICAL: 397 structured verified-root variants over $q\in\{5,7,11\}$]
The earlier sampler fixed a nonzero extension coordinate in the curve
coefficient $A$, so it did not cover the base-defined curves in the
counterexample family. Its exact curve/target variation gives the following summary from
`data/quadratic_family_summary_20260709.csv`. Every row is complete, has the
proved top shape, verifies its stored root, has nonredundant field equations,
and satisfies $d_{\mathrm{ff}}=5$ and
$d_{\mathrm{reg}}=\operatorname{sd}=q$.

| $q$ | Rows | Curves | Targets | Core sd | Remainder degree | Mutant $d_{\mathrm{reg}}$ | Mutant sd |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 171 | 90 | 20 | 5 | 2 or 3 | 3 or 4 | 3 or 4 |
| 7 | 190 | 96 | 38 | 5 | 2 or 3 | 3 or 4 | 3 or 4 |
| 11 | 36 | 18 | 20 | 5 | 3 | 4 | 3 or 4 |

[EMPIRICAL: exhaustive actual $q=5$ search] The script
`code/search_quadratic_counterexamples.py` checked all 12,000 nonsingular
curve/non-base-target candidates and all 6,228 cases where the target is an
$x$-coordinate on the curve. Every eligible actual Semaev system had solving
degree 5.

[EMPIRICAL: exhaustive actual $q=7$ search] The strengthened point-count and
normal-form search checked 98,784 nonsingular curve/target candidates and
50,376 eligible on-curve targets. Exactly six systems have eight rational core
zeros and zero normal forms for both field equations.

[EMPIRICAL: exhaustive actual $q=9$ search] A polynomial-basis implementation
over $\mathbb F_9$ checked 466,560 candidates and 236,160 eligible on-curve
targets. No core had eight rational zeros, so no field equations were
redundant. This is the smallest non-prime odd prime power in scope. Both new
searches are stored in `data/search_quadratic_redundancy_20260716.json`.

[EMPIRICAL: deterministic abstract search at $q=5$, seed 20260722] Keeping
only the symmetric top shape is insufficient: trial 565 gives lower
coefficients $(3,1,4,0,1,2,0,3)$ and solving degree 6. For this counterexample
$c+g^2=0$, exactly the denominator pole excluded by the irreducible Semaev
modulus identity. Both searches are recorded in
`data/search_quadratic_counterexamples_20260709.csv`.

[EMPIRICAL: $q\in\{7,11,13,17,19,23\}, n=m=2$, known decompositions] The
exact Macaulay computation gives

\[
d_{\mathrm{ff}}=5,\qquad d_{\mathrm{reg}}=
\operatorname{sd}_{\mathrm{grevlex}}=q.
\]

The solving-minus-first-fall gap therefore reaches 18 at $q=23$. This is a
strict, substantial divergence in actual Weil-restricted Semaev systems with
verified solutions, satisfying the prompt's falsifier.

[CONDITIONAL: field equations are nonredundant] The former six-prime
solving-degree conjecture holds for every odd prime power $q\ge5$ under the
stated hypothesis. Automatic nonredundancy is refuted by the infinite family
above, so this condition cannot be removed from the equality theorem.

[CITED] The existence of a growing gap is not surprising for unrestricted
polynomial systems: Caminata and Gorla (2023), Example 4.2, prove another
field-equation-driven family with $d_{\mathrm{ff}}=3$ and
$\operatorname{sd}=q-1$. The local result is narrower and new only as an
exact observation for this deterministic odd-characteristic Semaev/Weil
family; it does not refute the binary asymptotic question studied by Kousidis
and Wiemers (2019).

### Bounded secondary check at $n=3,m=2$

[EMPIRICAL: four deterministic known-target systems over
$q\in\{3,5,7,11\}$] After SG-11 was closed, a bounded check reduced the two
field equations by the exact core basis. The core basis degrees were at most
three, the field-equation remainder degrees were at most two, and the
replacement-family regularity and solving degree were at most three. For
$q=5,7,11$ both remainders were zero and the original core solving degree was
four. This supports a low-degree mutant mechanism but is not a symbolic
$n=3$ theorem and does not complete SG-12.

## Exact stopping boundary and limitations

[EMPIRICAL: $q=5,n\in\{2,3\},m=4$] Both 60-second runs verified a known
root and exactly obtained $d_{\mathrm{ff}}=d_{\mathrm{reg}}=16$, but timed
out after the regularity stage before Gröbner-basis containment. The rows are
preserved as stage-censored in the canonical CSV.

[EMPIRICAL: local environment on 2026-07-09] Sage, Singular, msolve, and
Macaulay2 executables were unavailable. Python 3.13.4, SymPy 1.14.0, and the
hand-built exact Macaulay implementation were used instead.

[PROVED] The quadratic theorem supplies an unconditional upper bound only for
$n=m=2$. Automatic field-equation nonredundancy is false. The result does not
give an all-parameter bound or address the binary $n\sim\log q$ asymptotic
regime.
