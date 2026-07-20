---
attempt: A014
status: folded-into-A001
---
# A014 - Classify the possible bases of an ideal-class target

## Idea

- [CONJECTURE] The unresolved phrase "a class group" may hide a new finite or
  function-field target that is neither trivial nor a Jacobian, so classify
  the base before searching for formulas.

## Finite and local bases

- [PROVED] Every invertible module over a commutative local ring is free of
  rank one.  Indeed, reduce a finite locally free rank-one module modulo the
  maximal ideal, lift a basis element, and apply Nakayama; the resulting map
  from the ring to the module is an isomorphism after localization at the only
  maximal ideal and hence globally.
- [CITED] A finite commutative ring is Artinian and decomposes as a finite
  product of Artinian local rings; the Stacks Project gives the local-product
  decomposition in Lemma 10.153.10 and the Picard interpretation of invertible
  modules in Section 15.119.
- [PROVED] Picard groups commute with finite products, so
  $\operatorname{Pic}(R)=0$ for every finite commutative ring $R$.  The same
  local argument gives $\operatorname{Pic}(R)=0$ for every local base,
  including a DVR or complete local lift.

## Global function-field bases

Let $C/\mathbb F_q$ be a smooth projective geometrically connected curve with
a rational point $\infty$, and put
$A=\Gamma(C\setminus\{\infty\},\mathcal O_C)$.

- [PROVED] Divisor theory gives
  $$\operatorname{Cl}(A)\simeq
  \operatorname{Pic}(C)/\mathbb Z[\infty]
  \simeq\operatorname{Pic}^0(C).$$
  The last isomorphism sends a divisor class $[D]$ to
  $[D-\deg(D)\infty]$ and uses $\deg(\infty)=1$.
- [CITED] Milne's Jacobian Theorem 1.1 identifies
  $\operatorname{Pic}^0(C)$ with $J_C(\mathbb F_q)$ when $C$ has an
  $\mathbb F_q$-point.
- [PROVED] Hence the ordinary ideal class group of a global function-field
  order with rational infinity is exactly a Jacobian target, not a fourth
  target type.
- [CITED] Adding a modulus produces a generalized Jacobian whose rational
  points are degree-zero divisor classes prime to the modulus modulo the
  corresponding principal relation (Milne, *Jacobian Varieties*, Section 9).
- [PROVED] A generalized Jacobian is a mixed algebraic-group target, so SG-21
  applies to rational point maps and their affine-kernel defects.

## Number-field bases

- [PROVED] A nontrivial classical ideal-class target must therefore retain a
  genuinely global number-field order, or an equivalent cross-characteristic
  global arithmetic object; finite quotients and localizations alone have
  trivial Picard group.
- [PROVED] A005--A006 exclude direct finite/local specialization and standard
  dense global lifts of the elliptic torsion point.
- [CONJECTURE] The sole surviving class-target interface is a direct algorithm
  that reads the finite-field point encoding and outputs an ideal class of a
  separately constructed number-field order without representing the point as
  a rational torsion point over that number field.  A polynomial-time nonzero
  homomorphism of this form refutes the present negative assessment.

## Outcome

- [PROVED] Finite/local class targets are trivial; global function-field class
  targets are ordinary or generalized Jacobians; standard number-field lifts
  are too large.  Q004 is reduced to one cross-characteristic number-field
  evaluator rather than an unspecified universe of class groups.

