---
attempt: A004
status: promising
---
# A004 - Does addition descend to a non-unit orbit quotient?

## Idea

Formalize the information a coefficient-tracking quotient-rho walk needs after replacing a point by a representative of its $\langle\lambda\rangle$ orbit. Test whether an exponent-free orbit state can support the additive r-adding transition at all.

## Prior art

- [CITED] Duursma-Gaudry-Morain (ASIACRYPT 1999) and the later negation-map literature implement rho on automorphism classes while transforming the linear coefficients together with the point.
- [PROVED] A003 shows that any canonicalizer returning the orbit multiplier already reduces ECDLP to the number of nonzero orbits plus one calls.

## Plan

1. Decide whether the orbit relation $X\sim[h]X$ is a congruence for the additive group law.
2. State the exact invariant required by an r-adding state $(X,a,b)$ with $X=[a]P+[b]Q$.
3. Prove either that orientation-free metadata suffices for transitions and collision equations, or that a standard coefficient-tracking transition must recover an orbit multiplier.
4. Separate this standard-walk result from richer algorithms that do not maintain linear coefficients.

## Prediction

- [CONJECTURE] For every nontrivial scalar subgroup $H\le\mathbb F_r^*$, addition does not descend to $G/H$. A refutation is a well-defined operation on orbit classes satisfying $\pi(X+Y)=\pi(X)\oplus\pi(Y)$ for all $X,Y\in G$.
- [CONJECTURE] A standard r-adding walk that canonicalizes after each addition cannot maintain the invariant $X=[a]P+[b]Q$ without recovering the multiplier between the pre-canonical and canonical points. A refutation is a known-log implementation that updates valid linear coefficients while returning and storing no such multiplier or equivalent orientation information.

## Execution log

Recorded before writing the proof.

- [PROVED] If $h\ne1$, then $P\sim[h]P$ but $P+(-P)=0$ and $[h]P+(-P)=[h-1]P\ne0$. Since zero is a singleton orbit, no addition compatible with the quotient map can be well-defined.
- [PROVED] In the formal coefficient model, canonicalizing $X=[a]P+[b]Q$ to $R=[h]X$ changes the coefficient polynomial $a+bz$ to $h(a+bz)$. Equality in $\mathbb F_r[z]$ forces both tracked coefficients to be multiplied by $h$.
- [PROVED] The A003 reduction needs only the multiplier $h$, not a discrete logarithm $j$ with $h=\lambda^j$.

## Outcome

- [PROVED] An orientation-free orbit class cannot carry the additive r-adding transition because the scalar-orbit relation is not a group congruence.
- [PROVED] A standard algebraic coefficient-tracking quotient walk must retain the multiplier between the incoming point and its chosen orbit representative, or information from which that multiplier is recovered.
- [PROVED] If a canonicalizer returns that multiplier, precomputing one normalized point per nonzero orbit reduces ECDLP to $q+1$ normalizations for $q=(r-1)/m$; no discrete logarithm inside $H$ is required.
- [PROVED] A batched canonicalizer that returns the multipliers for a requested batch gives the same reduction in one batch containing the $q$ transversal points and the target.
- [PROVED] This closes Q024 for standard algebraic coefficient-tracking rho and multiplier-returning batches. It does not rule out a nonlinear collision solver that works directly with the membership constraints $(a+bs)/(c+ds)\in H$; that richer question is Q025.
