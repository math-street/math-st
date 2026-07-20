---
attempt: A005
status: dead
---
# A005 - Specialize arithmetic ideal-class pairings to the finite-field source

## Idea

- [CITED] Buell--Call's number-field pairing gives actual computable
  homomorphisms from elliptic-curve points to ideal or idele class groups, so
  specializing it might produce the missing finite-field class character
  (Buell--Call 2016).

## Prior art

- [CITED] Buell and Call (2016) express the elliptic class pairing through
  local symbols and prove that, with a torsion argument fixed, it is the image
  of the Weil-descent pairing under a valuation/class map.

## Plan

- [PROVED] Test the direct base changes relevant to a finite-field point:
  $\operatorname{Spec}\mathbb F_q$ and a local integral lift.
- [PROVED] Separate direct specialization from a genuinely global lift over a
  number field.

## Outcome

- [PROVED] The ideal-class target of an arithmetic class pairing is the Picard
  group of its base.  Both $\operatorname{Pic}(\operatorname{Spec}\mathbb
  F_q)$ and the Picard group of a discrete valuation ring are trivial because
  every invertible module over a field or local PID is free of rank one.
- [PROVED] Therefore direct finite-field specialization and a purely local
  $p$-adic lift make the ideal-class component identically zero.
- [CITED] The available global pairing is also explicitly related to the
  established Weil-descent/Kummer pairing, so it is not evidence for a new
  independent mechanism (Buell--Call 2016, Corollary 4.5).

## Post-mortem

**Why it failed:** [PROVED] The nontrivial target comes from global places of a
number field; those places disappear over a finite or local base.

**What transfers:** [PROVED] Arithmetic class pairings are an important
counterexample to the overbroad statement that elliptic points never map to
class groups, but their finite-field specialization is trivial and their
pairing input is structurally a Weil-descent/Kummer input.

**Would it work under different assumptions?** [PROVED] A006 excludes standard
explicit global lifts using Parent's number-field torsion bound.
[CONJECTURE] Only a succinct implicit field/point representation supporting
global ideal arithmetic in polynomial time remains logically possible; an
explicit construction refutes the negative assessment.
