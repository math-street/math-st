---
attempt: A007
status: dead
---
# A007 - A subexponential transfer using only a generic source interface

## Idea

- [CONJECTURE] A transfer evaluator and its instance setup might use only
  equality, inversion, and addition in a randomly encoded order-$r$ source
  group, yet output an injective image in a target with a subexponential DLP;
  one such generic algorithm refutes the expected impossibility.

## Plan

- [PROVED] Compose the evaluator with its promised target logarithm algorithm.
- [PROVED] Compare the source-oracle query count of the composition with
  Shoup's checked generic-group DLP lower bound.
- [PROVED] Audit anomalous, pairing, descent, and class-group candidates against
  the exact interface rather than treating "non-generic" as an explanation by
  itself.

## Positive and negative criteria

- [PROVED] A positive theorem must cover randomized expected-time evaluation,
  instance setup, and target preprocessing after constant-probability
  truncation.
- [PROVED] A negative outcome is any admissible cross-group or coordinate
  operation inside the claimed model that invalidates the source generic-group
  lower bound.

## Model

Fix a prime $r$ and choose a uniformly random injective encoding
$\sigma:\mathbb Z/r\mathbb Z\to S$.  The source input consists of handles
$\sigma(1)$ and $\sigma(x)$, and the only permitted source operations are the
generic addition, inversion, identity, and equality oracles.  Public instance
parameters and nonuniform data independent of $\sigma$ are permitted.

A **generic-source transfer package** is a classical uniform package satisfying
SG-01 with the following accounting rules.

1. Setup, both evaluator calls, and any preprocessing must count every source
   oracle call.  Their joint expected source-query count is $r^{o(1)}$; the
   polynomial evaluator bound in SG-01 is a special case.
2. The evaluator may construct and operate on any explicitly represented
   target group.  All such target computation is free for the source-query
   lower bound.
3. No advice may depend on the random encoding, and no uncounted oracle may
   translate a source handle into coordinates, a lift, a divisor, a pairing
   value, or another representation.
4. On a uniformly random logarithm $x$, the joint setup/evaluation/target-DLP
   computation succeeds with probability at least a fixed $\delta>0$ for all
   sufficiently large family members.

The third item is the substantive restriction.  It makes the theorem below a
classification of black-box source transfers, not of all coordinate-sensitive
elliptic-curve algorithms.  The result is classical: quantum generic groups
are outside Shoup's 1997 model, and Shor's algorithm would make the source DLP
itself polynomial-time.

## Impossibility theorem

**Theorem.**  [PROVED] No infinite family of generic-source transfer packages
can have both an injective homomorphic evaluator and an $\exp(o(\log r))$
target logarithm algorithm.

**Proof.**  Give the alleged package the generic DLP challenge
$(\sigma(1),\sigma(x))$.  Run its counted setup, and evaluate

$$h=\phi(\sigma(1)),\qquad y=\phi(\sigma(x)).$$

Because $\phi$ is a homomorphism, $y=xh$.  Because the source has prime order
and $\phi$ is injective, $h$ has order $r$.  The promised target algorithm on
$(h,y)$ therefore returns $x$.

Let $q(r)=r^{o(1)}$ be an upper bound on the composition's expected number of
source-oracle calls.  Truncate it after $4q(r)/\delta$ calls.  Markov's
inequality loses at most $\delta/4$ success probability, so the truncated
generic DLP algorithm still succeeds with probability at least
$3\delta/4$.  Its deterministic query cap is
$m=r^{o(1)}$.

Shoup's random-encoding lower bound gives success probability
$O(m^2/r)=r^{-1+o(1)}$ for a classical generic algorithm in a prime-order
group.  This tends to zero, contradicting the fixed success probability
$3\delta/4$.  The target representation, group operations, and target
precomputation do not weaken the argument: after composition they are simply
arbitrary local computation by the generic source algorithm.  $\square$

## Escape audit

- [CITED] The anomalous attacks use field coordinates and a $p$-adic or
  dual-number lift/formal parameter.  Their evaluator is not available from a
  random source handle.
- [CITED] MOV/Frey--Ruck use curve equations, an independent torsion argument,
  line functions, and extension-field arithmetic.  A pairing or coordinate
  oracle is a cross-representation oracle excluded by item 3.
- [CITED] Weil descent uses the curve equation, a field basis, Frobenius, and
  explicit divisor maps.  It is likewise representation-specific.
- [PROVED] A coordinate formula into a class or ray-class group is not ruled
  out merely because its target uses generic ideal arithmetic.  To evade the
  theorem it must extract information from concrete source coordinates or
  another explicitly identified cross-representation operation.
- [PROVED] Efficient CM endomorphisms also use concrete representation, but
  this alone does not make them transfers: their elliptic target still lacks
  the required subexponential DLP.

## Outcome

- [PROVED] The proposed generic-source transfer is impossible in the stated
  classical model.
- [PROVED] This closes the black-box part of A001: generic ideal, class, ray,
  or level arithmetic cannot create an easy injective image unless some
  representation-specific source operation first crosses the model boundary.
- [CONJECTURE] Arbitrary coordinate-sensitive maps remain outside this lower
  bound.  A008 tests the next larger class: bounded-degree rational maps whose
  homomorphism law is promised only on the prime-order subgroup.

## Post-mortem

**Why it failed:** [PROVED] Composition with the easy target DLP would be a
generic source DLP algorithm using $r^{o(1)}$ queries, contradicting Shoup's
$O(m^2/r)$ success bound.

**What transfers:** [PROVED] Every surviving construction must name a
representation-specific source operation or cross-representation oracle.

**Would it work under different assumptions?** [PROVED] Concrete coordinates,
lifts, pairings, divisor maps, or quantum computation leave the classical
generic-source model; the theorem makes no claim about them.
