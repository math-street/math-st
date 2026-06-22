# P1.2 — Existence of a factor base over prime fields

This file records the supplied research target. It is a specification, not a
set of findings from this repository.

## Formal statement

Let $E/\mathbb F_p$ be ordinary with prime order
$r=\#E(\mathbb F_p)$ as $p\to\infty$. Given $p$, $E$, and oracle access to
uniform random points, find $(\mathcal F,\mathcal D)$ such that:

1. $\mathcal F\subset E(\mathbb F_p)$ and $|\mathcal F|\le L_p(1/2)$;
2. membership in $\mathcal F$ is decidable in $\operatorname{poly}(\log p)$;
3. $\mathcal D$ runs in $\operatorname{poly}(\log p)$ and decomposes a uniform
   random $R$ as $R=\sum_{i=1}^m P_i$, with $P_i\in\mathcal F$ and constant
   $m$, with probability at least $1/\operatorname{poly}(\log p)$.

The regime is prime fields only. The immediate task is SG-01 (a random-subset
baseline near $p=2^{16},2^{18},2^{20}$), followed when practical by SG-03
($x$ in the integer interval $[0,\sqrt p)$).

## Success discipline

Existence of decompositions is not enough: a candidate must also provide a
polylogarithmic-time method to find one. Solver timeouts and mathematical
nonexistence must be recorded separately.

## Interpretation discovered during execution

[CITED] In standard generalized L-notation,
$L_p[1/2,c]=\exp((c+o(1))\sqrt{\log p\log\log p})=p^{o(1)}$ for fixed $c$.
[PROVED] With $m$ fixed, condition (1) then permits only $p^{o(1)}$ ordered
summand tuples, while Hasse's bound gives
$\#E(\mathbb F_p)=p^{1+o(1)}$. Consequently condition (3) is impossible as
written; `CLAIM.md` gives the attacked proof and the exact necessary repairs.

[CONDITIONAL: the supplied notation intended $p^{1/2}$ rather than standard
L-notation] The square-root experimental program is a corrected variant, not
a witness for formal condition (1), and its efficient-finder question remains
open.
