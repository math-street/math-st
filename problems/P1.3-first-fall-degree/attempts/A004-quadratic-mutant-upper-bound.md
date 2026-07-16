---
attempt: A004
status: completed
---
# A004 - Closing the quadratic upper bound with a low-degree mutant family

## Idea

[PROVED] Replace the degree-$q$ field equations by their low-degree remainders
modulo a universal Groebner basis of the two Semaev core coordinates. The
replacement family generates the same ideal, is constructed inside the
original degree-$q$ closed space, and has a constant solving-degree bound.

## Prior art

[CITED] Salizzoni (2023), Proposition 3.10, bounds the closed/mutant solving
degree by
$\max\{d_{\mathrm{reg}}+1,\text{maximum input degree}\}$.

[CITED] Caminata and Gorla (2021) bound solving degree using homogenized
regularity under generic-coordinate hypotheses, but their Remark 4.6 warns
that raw input homogenization is usually not the homogenization of the affine
ideal.

## Plan

1. Normalize the two quadratic-extension coordinates in symmetric variables.
2. Prove a universal constant-degree core Groebner basis.
3. Reduce the field equations by that basis and bound the remainders.
4. Apply Salizzoni's theorem to the replacement family.
5. Try to break any argument using only the top shape.

## Execution log

[PROVED] With $s=x+y$, $p=xy$, and a non-base target, row operations put the
core in the form

\[
p^2+bp+cs^2+ds+e,\qquad ps+fp+gs^2+hs+i.
\]

[PROVED] The only nonconstant denominator in the symbolic grevlex basis is
$c+g^2$, and the Semaev specialization gives

\[
c+g^2=(m_1^2-4m_0)t_1^2/4\ne0.
\]

[PROVED: strengthened audit] The regenerated certificate checks explicit
basis representations and all Buchberger pairs over
$\mathbb Z[b,c,d,e,f,g,h,i][(c+g^2)^{-1}]$. A quartic top-part minor has
determinant $-1$, so the mutant regularity bound is valid after every allowed
finite-field specialization.

[PROVED] The specialized core basis has degrees $4,4,3,3$, leading monomials
$xy^3,y^4,x^3,x^2y$, and is contained in the closed degree-5 core space. The
exact symbolic certificate is `code/certify_quadratic_family.py`.

[PROVED] Field-equation remainders have degree at most 3. The replacement
family has maximum degree and degree of regularity at most 4, so its solving
degree is at most 5 by Salizzoni (2023).

[PROVED] For $q\ge5$, the replacement family and its complete degree-5 closed
space sit inside the original degree-$q$ closed space. Therefore
$\operatorname{sd}_{\mathrm{grevlex}}\le q$.

[EMPIRICAL: deterministic abstract $q=5$ search, seed 20260722] Top shape
alone does not suffice. The lower coefficient tuple
$(3,1,4,0,1,2,0,3)$ has solving degree 6 and satisfies $c+g^2=0$.

[EMPIRICAL: exhaustive actual $q=5$ search] All 6,228 eligible Semaev
curve/target systems have solving degree 5; none reaches 6.

## Outcome

[CONDITIONAL: the field equations enlarge the core ideal] Combining this
upper bound with A003's lower bound proves

\[
d_{\mathrm{ff}}=5,\qquad d_{\mathrm{reg}}=
\operatorname{sd}_{\mathrm{grevlex}}=q
\]

for the quadratic non-base-target family over every odd prime power
$q\ge5$.

## Limitation

[REFUTED by A005] Automatic field-equation nonredundancy is false, including
for nonsingular curves and non-base on-curve targets. The upper bound proved
here survives unchanged; the equality needs nonredundancy. Characteristic two
and all cases with $n>2$ or $m>2$ remain outside this theorem.
