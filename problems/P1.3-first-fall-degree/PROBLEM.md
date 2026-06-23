# P1.3 — Removing the first-fall-degree heuristic

## Formal research question

Let $E/\mathbb F_{q^n}$ be an elliptic curve, let
$f_{m+1}(x_1,\ldots,x_{m+1})$ be Semaev's summation polynomial, and let
$S(q,n,m)$ be a polynomial system over $\mathbb F_q$ obtained by Weil
restriction.

Given $q,n,m$, find an unconditional, explicit upper bound on the degree of
regularity or solving degree of $S(q,n,m)$ without assuming that its first
fall degree approximates either quantity.

The eventual target regime is $n\sim\log q$. The initial experimental range
is $n\in\{2,3\}$ and $m\leq 4$.

## Quadratic resolution (2026-07-16)

For $n=m=2$, odd prime powers $q\ge5$, nonsingular short-Weierstrass
curves, and non-base target $x$-coordinates, the strongest unconditional
statement proved here is

\[
d_{\mathrm{ff}}=5,\qquad d_{\mathrm{reg}}=q,\qquad
\operatorname{sd}_{\mathrm{grevlex}}\le q.
\]

For $q>5$, the equality $\operatorname{sd}_{\mathrm{grevlex}}=q$ holds if
and only if the field equations enlarge the two-coordinate core ideal. Automatic
nonredundancy is false: `attempts/A005-field-equation-counterexample.md`
gives an infinite eligible Semaev family with redundant field equations and
certifies a $q=7$ example with solving degree $5$, not $7$.

## Session-one target

Fix conventions for first fall degree, degree of regularity, solving degree,
and the maximum degree reached by a concrete algorithm. Give a worked toy
example that separates the notions, and establish a route to observable
intermediate-degree data.
