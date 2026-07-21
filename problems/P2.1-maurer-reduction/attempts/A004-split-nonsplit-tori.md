---
attempt: A004
status: completed
---
# A004 - Split and nonsplit one-dimensional tori

## Idea

[CONJECTURE] Replacing $\mathbb F_r^*$, of order $r-1$, by the norm-one
quadratic torus, of order $r+1$, may cover the multiplicative route's hard
inputs.  The finite two-torus menu is a uniform solution if every prime has at
least one polylogarithmically smooth value among $r-1$ and $r+1$.

## Prediction and decision rule

[CONJECTURE] Linnik's least-prime theorem and CRT can construct infinitely
many primes $r$ for which both $r-1$ and $r+1$ have polynomially large prime
factors.  The prediction fails if the CRT construction cannot keep both
forced factors polynomially large relative to the least prime it produces.

[PROVED] The algebraic torus formulas are refuted by any toy prime/nonsquare
for which the parametrization misses or duplicates a nonexceptional point,
extraction fails, the norm equation fails, or the group law is not closed.

## Plan

1. Write the norm-one torus, group law, and rational parametrization explicitly.
2. Validate the formulas exhaustively over toy prime fields.
3. Combine two forced congruences with Linnik's theorem.
4. Separate the obstruction to the two full tori from selected-subgroup and
   elliptic-curve possibilities.

## Execution log

- [PROVED] Wrote the quadratic norm-one torus as
  $x^2-dy^2=1$ with multiplication inherited from
  $\mathbb F_{r^2}^*$, and derived its order $r+1$ from the norm kernel.
- [PROVED] Derived the bijection
  $t\mapsto((1+dt^2)/(1-dt^2),2t/(1-dt^2))$ onto all points other than
  $(-1,0)$, with inverse $t=y/(x+1)$.
- [PROVED] Wrote failing tests before `torus_alternative.py`, then implemented
  the formulas.
- [EMPIRICAL: every parameter over four toy prime/nonsquare pairs] Exhaustive
  enumeration verified $r+1$ points, bijectivity, extraction, identity, and
  group-law closure.
- [CITED] Checked Xylouris 2009's effective Linnik theorem and admissible
  exponent $L_0=5.2$.
- [PROVED] Chose primes $q\in(X,2X)$ and $s\in(2X,4X)$, imposed
  $r\equiv1\pmod q$ and $r\equiv-1\pmod s$ by CRT, and applied Linnik to get
  $r=O(X^{2L_0})$.  Hence both $P^+(r-1)$ and $P^+(r+1)$ are at least
  $\Omega(r^{1/(2L_0)})$ along an infinite prime family.
- [PROVED] On this family, removing the forced factor leaves any smooth
  subgroup with order $O(r^{1-1/(2L_0)})$; the explicit uniform
  shift-and-test parametrizations therefore hit it with probability at most
  $O(r^{-1/(2L_0)})$ per attempt.
- [CITED] Checked the fixed-modulus prime number theorem in arithmetic
  progressions (Soprounov 1998, Theorem 2.1).
- [PROVED] Generalized the CRT construction: for each $1\le n\le D$, choose a
  comparable prime $q_n\equiv1\pmod n$ and a residue of exact order $n$.
  One Linnik prime then makes $q_n$ divide the full degree-$n$ norm-one torus
  order for every $n\le D$ simultaneously, with
  $q_n\ge c_Dr^{1/(DL_0)}$.

## Outcome

[PROVED] The prediction was confirmed.  Although the norm-one torus is a
valid and exceptionally simple auxiliary on primes with smooth $r+1$, choosing
between the two full orders $r-1$ and $r+1$ cannot be a uniform construction.
The standard random-shift attempt to use their smooth subgroups is also
super-polynomial on the constructed family.

[PROVED] A004 does not rule out higher-degree tori, a fundamentally different
subgroup embedding, or elliptic curves.  It strengthens the negative side of
Q005 without solving the general alternative-structure problem.

[PROVED] More precisely, it rules out every globally bounded-degree menu of
**full norm-one** tori; “higher-degree” above means an unbounded-degree family
or a different torus construction.  General bounded-dimensional tori and
selected subgroups are not classified by this attempt.

[PROVED] A005 later extends the full-group obstruction to all algebraic tori
of globally bounded dimension; the selected-subgroup limitation remains.
