---
attempt: A010
status: dead
---
# A010 - A finitely branched rational transfer into an affine group

## Idea

- [CONJECTURE] Input-dependent branching might splice several low-degree
  rational maps into an injective homomorphism even though no single map can
  survive A008.

## Audited model

Let \(C=\langle P\rangle\) have prime order \(r\).  Partition \(C\) into
\(B\) nonempty branch sets \(S_1,\ldots,S_B\).  On \(S_b\), the evaluator
agrees with a \(k\)-rational map \(F_b:E\dashrightarrow H\) into an affine
algebraic group with a fixed faithful linear representation.  On
\(E_{\bar k}\), the least common pole divisor of every branch's matrix entries
has degree at most \(D\).  Put \(D_+=\max(1,D)\).  No regularity is assumed of
the partition.

## Strengthened tradeoff theorem

**Theorem.**  [PROVED] If the piecewise evaluator is an injective
homomorphism on \(C\), and \(m=\lceil r/B\rceil\), then

\[
m(m-1)\le 2D(r-1). \tag{1}
\]

Consequently

\[
D_+B^2\ge \frac r4. \tag{2}
\]

The earlier \(D_+B^3\ge r/4\) theorem is valid but weaker.

## Proof

Choose a largest branch \(S\), with \(|S|=n\ge m\), and write \(F\) for its
rational map.  For \(t\in C\), let

\[
R(t)=|\{x\in S:x+t\in S\}|.
\]

Counting ordered pairs in \(S^2\) by their difference gives

\[
\sum_{t\in C}R(t)=n^2,\qquad
\sum_{t\ne0}R(t)=n(n-1).
\]

We claim that \(R(t)\le2D\) for every nonzero \(t\).  Otherwise, at more than
\(2D\) points \(x\), both \(x\) and \(x+t\) lie in \(S\), and homomorphy gives

\[
F(x+t)=\phi(t)F(x).
\]

Every matrix entry of

\[
\rho(F(X+t))-\rho(\phi(t))\rho(F(X))
\]

has pole degree at most \(2D\), so the curve zero bound makes this a rational
identity.  Because \(r\) is prime, nonzero \(t\) has order \(r\).  The least
common pole divisor of \(F\) is therefore invariant under translation by
\(t\): left multiplication by the invertible constant \(\phi(t)\) preserves
the largest local pole order.  The inequality \(R(t)>2D\) also gives \(D<r\),
so an invariant effective pole divisor of degree at most \(D\) must be empty.
The map \(F:E\to H\) is then a morphism from a proper connected curve to an
affine variety, hence constant.  The rational identity and invertibility of
that constant give \(\phi(t)=1\), contradicting injectivity.

It follows that

\[
n(n-1)=\sum_{t\ne0}R(t)\le2D(r-1),
\]

which proves (1).  If \(r<2B\), then
\(D_+B^2\ge B^2>r^2/4\ge r/4\).  If \(r\ge2B\), then
\(m\ge r/B\) and \(m-1\ge r/(2B)\); failure of (2) would make

\[
m(m-1)\ge\frac{r^2}{2B^2}>2D_+r>2D(r-1),
\]

contradicting (1).

## Audit of the earlier \(B^3\) argument

- [PROVED] Coloring \((X,Y)\) by the branches of \(X\), \(Y\), and \(X+Y\)
  does give a color class of size at least \(r^2/B^3\).
- [PROVED] The double-counting step in the old proof supplies more than
  \(2D\) usable specializations in each variable under
  \(r>4D_+B^3\), and the two zero counts are uniform because the selected
  branch maps are defined at every selected subgroup point.
- [PROVED] The noncommutative Pexider normalization in the old proof has the
  correct order of factors.
- [PROVED] The same-branch difference proof above uses only one branch color
  and improves the exponent from \(3\) to \(2\).
- [CONJECTURE] Whether one can improve \(B^2\) to \(B\) for completely
  adversarial partitions is open in this repository.  Ordinary
  Riemann--Roch interpolation heuristics do not prove such a lower bound.

## Circuit corollary

In the explicit rational decision-tree model of
RATIONAL_TRANSFER_REVIEW.md, at most \(b\) binary decisions on a root-to-leaf
path give \(B\le2^b\) transcripts.  If every transcript has arithmetic depth
\(d\), \(M\) output entries, and base pole degree \(D_0\ge1\), then
\(D\le M2^dD_0\).  Equation (2) gives

\[
d+2b\ge\log_2r-\log_2(4MD_0).
\]

With \(MD_0=(\log r)^{O(1)}\), this is
\(d+2b\ge n-O(\log n)\) for \(n=\lceil\log_2r\rceil\).

This is not a lower bound for arbitrary polynomial-time computation.  It
applies only after the evaluator is realized in the stated rational
decision-tree model; linear depth remains polynomial time.

## Outcome

- [PROVED] Polynomially many branches of degree
  \(\operatorname{poly}(\log r)\) cannot form an injective affine transfer.
- [PROVED] The audited quantitative obstruction is the exact overlap
  inequality (1), hence \(D_+B^2\ge r/4\), not merely the earlier \(B^3\)
  consequence.

## Post-mortem

**Why it failed:** [PROVED] A largest branch has a repeated nonzero difference
often enough to force a translation identity.  Low pole degree makes that
identity remove every pole and collapse the branch to a constant.

**What transfers:** [PROVED] Branching must pay the \(B^2\) tradeoff, or the
evaluator must use high degree, non-rational operations, or a non-affine
target.

**Would it work under different assumptions?** [PROVED] Linear arithmetic or
branch depth, high degree, non-rational operations, or proper targets remain
outside this exclusion.
