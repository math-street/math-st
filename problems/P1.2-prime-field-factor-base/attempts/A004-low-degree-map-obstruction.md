---
attempt: A004
status: dead
---
# A004 — Low-degree maps and auxiliary curves

## Idea

Test Candidate C by defining the factor base either as the image of a
low-degree rational map $\mathbb P^1\dashrightarrow E$ or as the intersection
of $E$ with a second plane curve of low degree.

## Prior art

[CITED] Stacks Project Lemma 53.2.2 states that a rational map from a normal
curve to a proper variety extends to a morphism.

[CITED] Stacks Project Proposition 53.13.7 factors a positive-characteristic
morphism of smooth proper curves into Frobenius followed by a separable
morphism, and Lemma 53.12.2 gives Riemann–Hurwitz for the separable part.

[CITED] Bézout's theorem in the MIT 18.721 algebraic-geometry notes bounds the
number of intersection points of distinct degree-$m$ and degree-$n$ plane
curves by $mn$.

## Execution and proof

[PROVED] Every rational map $\mathbb P^1\dashrightarrow E$ extends to a
morphism because $\mathbb P^1$ is normal and $E$ is proper. If it were
nonconstant, factor off every purely inseparable Frobenius map. The remaining
nonconstant separable morphism still has genus-zero source and genus-one
target. Riemann–Hurwitz would give
$$
-2 = \deg(f)(2\cdot 1-2)+\deg(R)=\deg(R),
$$
contradicting the effectiveness of the ramification divisor. Thus the map is
constant in every characteristic.

[PROVED] The image construction therefore produces at most one factor-base
point. With a fixed number $m$ of summands it reaches at most one target, so
its success probability on a uniform target is at most $1/r$.

[PROVED] Let $H$ be a plane curve of degree $d$ that does not contain the
plane cubic $E$ as a component. Bézout bounds the geometric intersection by
$3d$, hence $|E(\mathbb F_p)\cap H(\mathbb F_p)|\le 3d$. A fixed-$m$
decomposition from this factor base reaches at most $(3d)^m$ targets and has
success probability at most $(3d)^m/r$.

[CONDITIONAL: d and m are bounded by poly(log p), while r grows at prime-field scale]
The preceding success bound is smaller than $1/\operatorname{poly}(\log p)$,
so this auxiliary-curve subclass fails condition (3).

[PROVED] If $H$ instead contains $E$ as a component, every point of
$E(\mathbb F_p)$ lies on $H$ and the resulting factor base has size $r$, so it
does not provide the required small factor base.

## Outcome

[PROVED] Candidate C is ruled out for rational images of $\mathbb P^1$ and for
fixed/polylog-degree plane auxiliary curves under the stated constant-$m$
decomposition model. This does not rule out higher-dimensional parameter
spaces or auxiliary varieties whose degree grows faster.

## Post-mortem

**Why it failed:** [PROVED] Genus blocks nonconstant rational parametrization,
while Bézout makes a genuinely distinct low-degree plane condition too sparse.
Sharing the elliptic component flips the construction from too sparse to the
entire curve.

**What transfers:** [PROVED] Any later algebraic candidate should check this
same dichotomy: a bounded-degree condition on the one-dimensional curve is
either finite of degree-controlled size or contains a curve component.

**Would it work under different assumptions?** [CONJECTURE] A construction
using a higher-dimensional parameter space and a many-to-one map might evade
the genus obstruction, but it must still supply cheap membership and a
polylogarithmic decomposition algorithm. An explicit construction satisfying
all three conditions would refute this assessment.
