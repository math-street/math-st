---
attempt: A024
status: folded-into-A001
---
# A024 - A finite valuation/factor-base evaluator model

## Scope and separation from SG-30

- [PROVED] This attempt addresses SG-32 only. Setup is given an imaginary
  quadratic order $\mathcal O_\Delta$ and target data containing an order-$r$
  class. It does not construct that data; the uniform prescribed-order task
  remains SG-30.
- [PROVED] Write $n=\lceil\log_2r\rceil$ and
  $B_\Delta=\log_2|\Delta|$. The target is required to lie in the SG-25
  window

  $$
  2n-O(\log n)\le B_\Delta=o(n^2/\log n).
  $$

  The lower bound below is uniform in $\Delta$ and therefore applies to
  every supplied target in this window.

## Fixed ordinary-class output encoding

- [CITED] By the standard form--ideal correspondence (for example Cox,
  Chapters 2 and 7), for a negative order discriminant
  $\Delta\equiv0,1\pmod4$,
  proper invertible ideal classes of $\mathcal O_\Delta$ are represented by
  primitive positive-definite binary quadratic forms

  $$
  (a,b,c),\qquad b^2-4ac=\Delta,
  $$

  under proper equivalence. The corresponding ideal convention here is
  $[a,(-b+\sqrt\Delta)/2]$.
- [PROVED] `REDUCE` returns the unique canonical reduced representative with
  $|b|\le a\le c$ and the tie convention $b\ge0$ when $|b|=a$ or $a=c$.
  `COMPOSE` means proper Gauss composition followed by `REDUCE`. Thus every
  output is exactly one triple of integers in one fixed ordinary class group;
  ray data and point-dependent discriminants are not permitted.

## The VFB instruction set

A **valuation-mediated factor-base program**, abbreviated VFB, has a finite
list of opcodes and a polynomial-size instance description.

### Setup data

Setup supplies $p,E,P,r,\Delta$, a finite list of rational primes
$L=(\ell_1,\ldots,\ell_s)$, and a finite list of canonical reduced target
forms $F_1,\ldots,F_m$. All are independent of the source input point $Q$.
The forms may include a certified order-$r$ class, but finding one is outside
this model and remains SG-30.

### Raw integer instructions

1. `LIFTX`, `LIFTY`, and `INFINITY` read the affine coordinates of $Q$ as
   canonical integers in $[0,p-1]$ and the identity tag.
2. `CONST`, `NEG`, `ADD`, `SUB`, `MUL`, `EDIV`, and `REM` perform exact
   integer arithmetic. `EDIV` is legal only when the divisor is nonzero and
   divides the dividend. A valid program has no hidden data-dependent failure.
3. `VAL(i,z)` returns $v_{\ell_i}(z)$ and returns a distinguished symbol
   `INF` when $z=0$. The prime index may be selected adaptively from previous
   observations.
4. `BIT(z,z')` performs one binary comparison from the fixed set
   $=,\ne,<,\le$. Every data-dependent branch, including an identity test, is
   a counted `BIT` instruction.

### Observation and target instructions

5. Observation registers contain only `VAL` results, `BIT` results, and
   integer functions of those results. Raw lifted-coordinate registers may be
   used to form later `VAL` or `BIT` operands, but may not be copied into an
   observation register.
6. `FORMPOW(i,e)`, `COMPOSE`, `INVERSE`, `REDUCE`, and `RETURN` operate on the
   fixed setup forms, with indices and exponents determined only by
   observation registers.
7. There is no `MAKEFORM` instruction taking raw lifted integers as form
   coefficients, and raw registers cannot index a target table. This is the
   substantive VFB boundary: the target class is mediated by finitely many
   valuation/comparison outcomes and a fixed factor base.

Loops are allowed only with an a priori bound and are charged after
unrolling. The program is deterministic and exact. The same theorem applies
to a bounded zero-error randomized program after fixing any random tape,
because every tape must return the same exact class.

This interface is not a polynomial-interpolation model. `LIFTX`, `LIFTY`, and
`VAL` are integer, cross-characteristic operations with no assumed
low-degree rational realization on $E$.

## Transcript lower bound

For the $j$-th executed valuation, let $h_j$ be a bound such that every
nonzero operand $z$ satisfies $|z|<2^{h_j}$. Let $T$ be the maximum number of
`VAL` calls and $C$ the maximum number of `BIT` calls on a source input.

### Theorem - nonzero VFB evaluators need a full input-length transcript

- [PROVED] If a VFB program evaluates a nonzero homomorphism

  $$
  \phi:\langle P\rangle\longrightarrow\operatorname{Cl}(\mathcal O_\Delta),
  $$

  then

  $$
  C+\sum_{j=1}^{T}\log_2(h_j+1)\ge\log_2r. \tag{A024.1}
  $$

  In particular, if $h_j\le h$ for every call, then

  $$
  C+T\log_2(h+1)\ge\log_2r. \tag{A024.2}
  $$

**Proof.** A nonzero homomorphism out of the prime-order group
$\langle P\rangle$ has trivial kernel and hence takes $r$ distinct output
values.

For nonzero $z$ with $|z|<2^{h_j}$ and selected prime $\ell\ge2$, one has
$0\le v_{\ell}(z)\le h_j-1$. Including `INF`, the $j$-th `VAL` has at most
$h_j+1$ possible outcomes. A `BIT` has two outcomes. Adaptivity does not
change the leaf bound: induction on the remaining instruction budgets shows
that a decision tree with these per-path budgets has at most

$$
2^C\prod_{j=1}^{T}(h_j+1)
$$

leaves.

By items 5--7 of the model, two inputs with the same observation transcript
execute target operations on the same fixed forms with the same exponents and
therefore return the same reduced form. Thus the number of distinct outputs
is at most the number of leaves. Injectivity gives

$$
r\le2^C\prod_{j=1}^{T}(h_j+1).
$$

Taking base-two logarithms proves (A024.1) and (A024.2). $\square$

### Polynomial-height corollary

- [PROVED] If every valuation operand has bit length at most $h\le n^\kappa$
  for a fixed $\kappa$ and the program makes $C=o(n)$ raw comparisons, then

  $$
  T\ge
  \frac{n-1-C}{\log_2(n^\kappa+1)}
  =\Omega\!\left(\frac n{\log n}\right). \tag{A024.3}
  $$
- [PROVED] More generally, (A024.1) is a tradeoff: a proposed evaluator must
  expose essentially $n$ bits through raw coordinate comparisons and
  valuation outcomes. A constant number of polynomial-height valuations and
  $o(n)$ comparisons cannot evaluate a nonzero homomorphism in VFB.
- [PROVED] This lower bound is compatible with polynomial time. It excludes a
  shallow or low-observation valuation recipe, not every polynomial-length
  valuation computation, and therefore does not close P1.5/Q004.

## Verheul/Moody template check

- [CITED] Verheul's reverse XTR homomorphism consequence and Moody's
  generalization use a computable nondegenerate pairing together with a
  computable distortion map. They turn the proposed reverse map into an
  efficient Diffie--Hellman algorithm.
- [PROVED] An analogous conditional statement is available here. Put
  $h=\phi(P)$. If the target supplied an efficiently computable bilinear map
  $e$ and endomorphism $\delta$ such that
  $\zeta=e(h,\delta h)$ has order $r$, then from $A=aP$ and $B=bP$ one could
  compute

  $$
  e(\phi(A),\delta\phi(B))=\zeta^{ab}.
  $$

  An efficient discrete logarithm in $\langle\zeta\rangle$ would recover
  $ab$ and hence $abP$. This is the direct Verheul-style consequence for a
  forward evaluator.
- [PROVED] The checked ordinary imaginary-quadratic reduced-form target does
  not come with such a pairing/distortion package. Genus characters take
  values of exponent two and are trivial on odd order-$r$ torsion. Abstract
  order-$r$ characters do not supply an efficiently evaluable character from
  the reduced-form encoding. Consequently the Verheul/Moody template gives a
  useful audit condition but no unconditional SG-32 lower bound by itself.
- [PROVED] The transcript theorem above avoids assuming source ECDLP or CDH
  hardness and uses only the exact VFB interface.

## Boundary and falsifiers

- [PROVED] Direct Buell-style form synthesis from raw lifted coordinates is
  outside VFB because it would require `MAKEFORM`; A017 separately shows that
  the naive instance has a point-dependent discriminant.
- [PROVED] A program that copies a canonical lift or remainder directly into
  a form coefficient or factor-base exponent is outside VFB. It must receive
  its own model and invariant before (A024.1) can be claimed for it.
- [PROVED] A program using $\Omega(n/\log n)$ polynomial-height valuations is
  not excluded. Producing and proving a nonzero homomorphism with such a
  program would refute the negative assessment while respecting this theorem.
- [PROVED] An order-$r$ target constructor is not a falsifier for A024 and
  does not complete the evaluator; that remains the separate SG-30 task.

## Outcome

- [PROVED] SG-32 is complete at its requested one-model scope: the ordinary
  output is a canonical reduced primitive form, VFB is a finite
  coordinate/lift/valuation/factor-base instruction set, and every nonzero
  evaluator in it satisfies (A024.1)--(A024.3).
- [PROVED] The result is a repository-original model theorem rather than an
  application of the checked polynomial-interpolation papers. It is strictly
  scoped and is not an unrestricted concrete ECDLP lower bound.
