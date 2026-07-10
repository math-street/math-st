---
attempt: A001
status: in-progress
---
# A001 - A computable elliptic-to-class-group character

## Idea

Construct an imaginary-quadratic order $\mathcal O_I$ whose class group has an
order-$r$ element and evaluate a nonzero homomorphism
$\langle P\rangle\to\operatorname{Cl}(\mathcal O_I)$ without first solving the
source DLP.

## Prior art

- [CONDITIONAL: ERH and factor-base decomposition of represented inputs]
  Hafner--McCurley-style class-group relations give a subexponential target
  route.
- [CITED] CM theory relates elliptic curves, ideals, and isogenies.
- [CITED] Buell and Call (2016) give computable ideal-class pairings on
  number-field points and identify them with a Weil-descent pairing after
  fixing a torsion argument; this does not directly have domain
  $E(\mathbb F_q)$.
- [CITED] Castryck--Houben--Vercauteren--Wesolowski (2022) define the usual CM
  direction from an ideal class to an oriented curve via the kernel
  $E[\mathfrak a]$; it is not a point-to-ideal character.

## Plan

1. Restrict first to ordinary CM curves with a known endomorphism ring.
2. Test maps obtained from point ideals, divisors, and isogeny actions for the
   homomorphism identity on complete toy subgroups.
3. Reject any construction whose evaluation requires the scalar of $P$ or a
   table of $r$ points.

## Execution log

- [EMPIRICAL: literature and structure scan on 2026-06-26] No evaluator was
  identified; only the target-side subexponential algorithm was verified.
- [PROVED] A003 shows that the annihilator, cyclic kernel, and kernel-isogeny
  quotient of a nonzero point all forget which generator of the order-$r$
  subgroup was supplied.
- [PROVED] A003 also gives an explicit asymptotic size obstruction for the
  class group of the curve's own endomorphism order when $r\ge q/2$.
- [PROVED] A004 excludes the ray class group modulo $r$ for
  $K=\mathbb Q(i)$ by its order, while the modulus-$r^2$ principal units retain
  an easy order-$r$ target but no known source evaluator.
- [PROVED] A005 rules out the direct specialization of arithmetic class
  pairings to a finite field or a local PID because the base Picard group is
  trivial.
- [PROVED] A006 rules out standard dense global torsion lifts because their
  number-field degree is exponential in $\log r$.
- [PROVED] A007 rules out every generic-source realization, even if all target
  ideal/class arithmetic is free: composing the evaluator with the target DLP
  contradicts Shoup's $O(m^2/r)$ generic success bound.
- [PROVED] A008--A010 rule out low-degree or shallow piecewise-rational
  realizations in a polynomial-size affine algebraic presentation; they force
  $\max(1,D)B^2\ge r/4$ and
  $d+2b\ge\log_2r-O(\log\log r)$ in the audited rational decision-tree model.
- [PROVED] A011--A013 classify proper and mixed algebraic targets: proper
  rational branches collapse to a global elliptic-isogenous image, while a
  non-global mixed map must violate an explicit fibrewise affine-kernel
  defect degree bound.
- [PROVED] A014 reduces finite/local class targets to the trivial group and
  global function-field class targets to Jacobian or generalized-Jacobian
  targets; only a global number-field order remains genuinely distinct.
- [PROVED] A015 makes evaluator construction equivalent to source DLP given a
  target-DLP oracle; target size and target algorithms alone cannot supply the
  missing coordinate computation.
- [PROVED] A016 restricts the checked Hafner--McCurley route to discriminant
  bit length $2\log_2r-O(\log\log r)\le B=o((\log r)^2/\log\log r)$.
- [PROVED] A017 shows that canonical residue representatives in the explicit
  Buell formula have point-dependent discriminants and do not land in one
  class group.
- [EMPIRICAL: bounded literature search on 2026-07-10] A018 found only
  characteristic-zero point-to-class pairings and finite-field class actions
  in the reverse direction, not the required direct cross-characteristic map.
- [PROVED] A019 gives a uniform exact order-$r$ ideal class in discriminant
  $1-4\cdot2^r$, but its $\Theta(r)$-bit target description is exponential in
  $\log r$ and violates SG-01.
- [EMPIRICAL: exhaustive $|\Delta|\le200000$, primes $3\le r\le43$] A020
  finds much smaller exact-order toy targets: every least qualifying
  discriminant has class number $r$ and $0.684711\le|\Delta|/r^2\le2.555556$.
  The exhaustive search is not a uniform polynomial-time construction.
- [EMPIRICAL: bounded primary-source search on 2026-07-10] A021 found
  prescribed-order existence theorems and $n$-th-power discriminant families,
  but no uniform polynomial-bit exact-order constructor.  This target-only
  gap is separate from the evaluator; A004 supplies a succinct ray target,
  but A022 below shows why that transparent target is not an intermediate
  substitute for an ordinary class group.
- [PROVED] A022 sharpens the ray branch: linearizing any nonzero evaluator into
  $(1+r\mathbb Z[i])/(1+r^2\mathbb Z[i])$ reveals the source scalar with one
  evaluator call.  Ray evaluation and source DLP are polynomial-time
  equivalent, so this easy target has no intermediate subexponential regime.
- [CITED] A023 reconciles the rational package with the cryptographic
  interpolation literature. Coppersmith--Shparlinski already supply the
  arbitrary-subset quadratic-overlap mechanism in the scalar finite-field
  setting, so the $B^2$ scale is prior art; the checked results do not state
  the elliptic-source, faithful-affine-target theorem and do not improve the
  adversarial branch exponent toward one.
- [PROVED] A024 fixes the VFB coordinate/lift/valuation model and proves
  $C+\sum_j\log_2(h_j+1)\ge\log_2r$ for any nonzero evaluator. This completes
  SG-32 at its one-model scope but leaves polynomial-length VFB programs and
  direct raw-coordinate form synthesis outside the lower bound. SG-30 remains
  the separate ordinary-target construction task.

## Falsifier

- [PROVED] One explicit infinite family, polynomial-time evaluator, nonzero
  image test, and target complexity bound satisfying SG-01 would refute the
  current negative assessment.

## Outcome

- [PROVED] The natural CM-order constructions have been split into the dead
  A003--A006 branches, and A007 closes the generic-source branch.
- [CONJECTURE] A separately constructed order or a non-CM point-to-ideal
  formula using concrete source coordinates, high-degree rational arithmetic,
  or a non-rational lift/valuation operation will not yield a structurally new
  finite-field transfer; an explicit polynomial-time nonzero evaluator refutes
  this conjecture.
