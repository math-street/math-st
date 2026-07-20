---
attempt: A006
status: dead
---
# A006 - Lift the finite-field subgroup to a global torsion subgroup

## Idea

- [CONJECTURE] Lift the order-$r$ source points to an elliptic curve over a
  number field and apply the nontrivial arithmetic ideal-class pairing of
  Buell--Call; a standard explicit package of length $(\log r)^{O(1)}$ would
  refute the negative assessment.

## Prior art

- [CITED] Parent (1999, Theorem 1.2) proves that if an elliptic curve over a
  degree-$d$ number field has a rational point of order $p^a$, then for
  $p\ge5$,
  $$p^a\le65(3d-1)(2d)^6.$$
- [CITED] Sutherland (2012, Theorem 5) restates the same explicit bound and
  discusses prime torsion orders and modular curves.

## Plan

- [PROVED] Apply Parent's bound to the single lifted generator required by a
  global class pairing, then compare the resulting field degree with SG-01's
  full input-length restriction.

## Outcome

- [PROVED] For prime $r\ge5$, Parent's bound implies
  $$r<65(3d)(2d)^6=12480d^7,$$
  hence $d>(r/12480)^{1/7}=\exp(\Omega(\log r))$.
- [PROVED] In the standard explicit number-field representation, a field
  element is a length-$d$ coordinate vector in a power or integral basis, so
  the lifted point and the ideal arithmetic have encoding and operation cost
  $\Omega(d)$.
- [PROVED] Therefore every such standard explicit global-lift package has
  full input length and evaluator cost exponential in
  $n=\lceil\log_2 r\rceil$, violating SG-01's requirement $L=n^{O(1)}$.

## Post-mortem

**Why it failed:** [PROVED] A globally rational large-prime torsion point
forces superpolynomial number-field degree, before the class pairing or target
DLP is evaluated.

**What transfers:** [PROVED] Any future arithmetic lift proposal must count
the degree and representation cost of the field of definition, not only the
formula used after the lift.

**Would it work under different assumptions?** [CONJECTURE] A succinct
implicit field/point representation supporting all global valuations and
ideal-class operations in $\operatorname{poly}(\log r)$ time would evade the
standard dense-encoding argument; an explicit construction refutes this
conjecture, and Parent's degree bound alone does not exclude such a model.
