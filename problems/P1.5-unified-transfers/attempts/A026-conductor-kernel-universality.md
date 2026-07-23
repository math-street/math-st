---
attempt: A026
status: prior-art-control
---
# A026 - Conductor-kernel universality or a genuinely direct class transfer

## Why Q004 is open again

- [PROVED] A025 is a correct ordinary ring-class presentation of the known
  degree-two pairing transfer.
- [PROVED] It does not meet the genuine research standard for Q004 because
  both of its nonzero character and target-DLP advantage factor through the
  already known finite-field pairing target.
- [PROVED] A024 is a lower bound only for its valuation-mediated factor-base
  model. It does not cover direct `MAKEFORM` programs or all polynomial-time
  coordinate/lift/valuation evaluators.

Q004 is therefore open at the novelty-grade standard below.

## Novelty-grade closure contract

A positive result must give an infinite uniform family and an evaluator

$$
\phi:\langle P\rangle\longrightarrow\operatorname{Pic}(\mathcal O)
$$

that meets SG-01 and whose proof does not use a nonzero local, pairing, or
geometric transfer as an intermediate character. In particular, the
evaluator may not call a Miller loop, a Weil/Tate pairing, a distortion map,
an anomalous formal logarithm, or a qualifying descent map.

A negative result must cover a strictly broader exact model than A024 and
prove one of the following.

1. Every qualifying evaluator in that model factors efficiently through a
   known local, pairing, or geometric transfer.
2. Every nonzero evaluator in that model yields a stronger hard-problem
   consequence than the target-DLP sandwich alone.
3. No nonzero evaluator exists in that model, by an unconditional proof that
   does not assume the source DLP lower bound it is trying to explain.

Before either verdict is called a discovery, its exact theorem statement and
proof mechanism must survive a primary-source prior-art audit. A routine
specialization of a standard exact sequence is a control theorem, not enough.

## Candidate structural theorem

Let $K$ be an imaginary quadratic field with maximal order
$\mathcal O_K$, and let

$$
\mathcal O_f=\mathbb Z+f\mathcal O_K.
$$

The conductor exact sequence gives

$$
(\mathcal O_K/f\mathcal O_K)^\times/
\bigl((\mathbb Z/f\mathbb Z)^\times
      \operatorname{im}(\mathcal O_K^\times)\bigr)
\longrightarrow
\operatorname{Pic}(\mathcal O_f)
\mathop{\longrightarrow}^{\pi_f}
\operatorname{Pic}(\mathcal O_K)
\longrightarrow1. \tag{A026.1}
$$

For a prime-order source $C$ and a nonzero
$\phi:C\to\operatorname{Pic}(\mathcal O_f)$, the prime-order kernel lemma
gives an exact dichotomy:

1. $\pi_f\phi$ is nonzero and hence injective, so Q004 already has a
   maximal-order class transfer; or
2. $\pi_f\phi=0$, so the whole image lies in the conductor kernel.

The second branch has a CRT decomposition over primes $\ell\mid f$. For
$r\ge5$, the bounded unit quotient has no $r$-torsion. A nonzero projection
of the order-$r$ image therefore lands in a local factor

$$
T_{\ell^e}=
(\mathcal O_K/\ell^e\mathcal O_K)^\times/
(\mathbb Z/\ell^e\mathbb Z)^\times. \tag{A026.2}
$$

The local order is

$$
|T_{\ell^e}|=
\ell^{e-1}\bigl(\ell-\chi_K(\ell)\bigr). \tag{A026.3}
$$

Consequently:

- if $r=\ell$, the image is in the principal-unit/ramified filtration, whose
  successive order-$r$ quotients are additive $\mathbb F_r$ lines;
- if $r\ne\ell$, then
  $r\mid\ell-\chi_K(\ell)$ and the image is in the split multiplicative
  torus $\mathbb F_\ell^\times$ or the inert norm-one torus in
  $\mathbb F_{\ell^2}^\times$.

This algebraic dichotomy is standard exact-sequence arithmetic.

## Computational check

- [PROVED] For \(K=\mathbb Q(i)\) and every odd conductor \(f\), an arbitrary
  primitive form of discriminant \(-4f^2\) can be moved to an equivalent form
  \((A,B,C)\) with \(\gcd(A,f)=1\) by the shear
  \[
  (A,B,C)\longmapsto
  (A+Bt+Ct^2,\;B+2Ct,\;C).
  \]
  Modulo each prime \(\ell\mid f\), the primitive discriminant-zero
  polynomial \(A+Bt+Ct^2\) has at most one root. Random \(t\bmod f\)
  therefore succeeds with density at least
  \(\prod_{\ell\mid f}(1-1/\ell)\), giving a Las Vegas
  expected-polynomial search.
- [PROVED] For such a form,
  \[
  \gamma=\gcd_{\mathbb Z[i]}(A,-B/2+fi)
  \]
  gives the inverse conductor residue \(\gamma\bmod f\), up to rational
  units and \(i\).
- [PROVED] For an odd prime \(p\), the principal-unit line in conductor
  \(p^2\) has the exact form realization
  \[
  a\longmapsto
  \left[\left(1+p^2a^2,\;2p^3a,\;p^4\right)\right],
  \qquad a\in\mathbb F_p.
  \]
  Multiplication of \(1+pai\bmod p^2\) proves additivity and injectivity.
- [EMPIRICAL: complete source subgroups at \(p=101,211,401\)] The regression
  probe checked every scalar, obtained \(p\) distinct ordinary ring classes,
  inverted every class to \(1+pai\bmod p^2\), and recovered the seeded
  logarithm. It also checked all 44 projective residues in the tame
  conductor-\(43\) control.

## Prior-art falsification of the novelty claim

- [CITED] Hühnlein--Takagi (1999) already reduce DLP in totally nonmaximal
  class-number-one imaginary quadratic orders to DLP in
  \(\mathbb F_\ell^\times\) or \(\mathbb F_{\ell^2}^\times\).
- [CITED] Castagnos--Laguillaumie (2009), Lemma 1, gives the effective
  isomorphism (A026.2) for general conductor and explicitly describes the
  inverse from a reduced kernel ideal by conductor-coprime replacement,
  extension, principalization, and reduction modulo the conductor.
- [CITED] Kopp--Lagarias (2024) supplies a general change-of-order and
  change-of-modulus exact-sequence framework.
- [PROVED] The proposed computational strengthening is therefore not new.
  The Gaussian gcd and the explicit wild forms are useful executable
  specializations, but they are controls, not a Q004 discovery.

The part not supplied by those papers is source-side: when the target order
is constrained to the CM field of the source curve, the Hasse bound and the
prime-order projection can force a proposed class transfer into a known
source regime. A027 isolates and proves that statement without recycling
A026 as novelty.

## Immediate falsifiers

- A direct evaluator into the maximal-order component makes (A026.1) a
  reduction, not an impossibility theorem.
- A conductor-kernel evaluator whose reduced-form output cannot be lifted to
  a local residue certificate in polynomial time falsifies the proposed
  computational factorization.
- [TRIGGERED] A primary source that already states the same effective
  conductor-kernel isomorphism removes the novelty claim even though the
  formulas and implementation are correct.
- An argument that merely composes the evaluator with the target DLP repeats
  A015 and is not a new hard-problem consequence.

## SG-30 separation

A026 takes the target order and its order-$r$ image as supplied setup. It does
not construct a prescribed-order target from arbitrary $r$ and does not work
SG-30.

A029 later observes that A026's own wild formula at \(p=r\), parameter
\(a=1\), is already the missing target constructor once source compatibility
is dropped. Its reduction is \([r^2,2r,r^2+1]\). Thus A026's Q004 novelty
verdict remains unchanged, while SG-30 is subsequently closed.
