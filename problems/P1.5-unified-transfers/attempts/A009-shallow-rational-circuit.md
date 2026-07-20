---
attempt: A009
status: dead
---
# A009 - A shallow rational-arithmetic circuit for an affine transfer

## Idea

- [CONJECTURE] Although A008 excludes an explicitly expanded low-degree
  formula, a short straight-line program might evaluate a high-degree affine
  transfer with sublinear sequential depth in $n=\lceil\log_2 r\rceil$.

## Plan

- [PROVED] Bound pole degree under each binary arithmetic gate.
- [PROVED] Combine the circuit bound with A008's necessary condition
  $D\ge r/2$.
- [PROVED] Compare the result with the Miller loop, whose purpose is precisely
  to represent a high-degree function by a short straight-line program.

## Circuit model

Fix finitely many rational input functions on $E$ whose pole divisors have
degree at most $D_0$.  A branch-free circuit over the coefficient field uses
binary $+,-,\times,/$ gates, with division only where the resulting rational
map is defined on the source subgroup.  Let $d$ be its arithmetic depth and
let $M$ be the number of matrix-entry outputs in a faithful representation of
the affine target.  This is an algebraic-depth model, not a model of every
polynomial-time bit program.  A uniform bit-complexity interpretation also
requires polynomial encodings for the field, constants, circuit, and target
representation, plus polynomial-cost field operations.

## Degree lemma

- [PROVED] If rational functions $u,v$ have pole degrees at most $a,b$, then
  each of $u+v$, $u-v$, $uv$, and $u/v$ has pole degree at most $a+b$.
  For division, use
  $\operatorname{div}_\infty(u/v)\le
  \operatorname{div}_\infty(u)+\operatorname{div}_0(v)$ and
  $\deg\operatorname{div}_0(v)=\deg\operatorname{div}_\infty(v)$.
- [PROVED] Induction on circuit depth gives pole degree at most
  $2^dD_0$ for each output.  Summing the output pole divisors supplies a common
  pole divisor of degree at most $M2^dD_0$.

## Depth theorem

- [PROVED] If the circuit restricts to an injective homomorphism on
  $\langle P\rangle$, A008 gives
  $$\frac r2\le M2^dD_0,$$
  and therefore
  $$d\ge\log_2 r-\log_2(2MD_0).$$
- [PROVED] In particular, if $M D_0=(\log r)^{O(1)}$, then
  $d\ge n-O(\log n)$.  A branch-free affine transfer cannot have
  $o(\log r)$ rational-arithmetic depth even when its total straight-line
  representation is compact.

## Boundary audit

- [CITED] Miller's original straight-line-program work explicitly separates a
  compact program from the exponentially larger expanded rational function
  (Miller 1986/2024).
- [CITED] For a pairing, the Miller recurrence follows a length-$\Theta(\log r)$
  addition chain while constructing a function of pole degree $\Theta(r)$.
  It matches the theorem's depth scale rather than contradicting it.
- [PROVED] The anomalous evaluator is outside the base-curve rational circuit
  model because it computes in a lift or infinitesimal thickening.  Its
  multiplication-by-$p$ stage nevertheless also has a dependent
  $\Theta(\log p)$ double-and-add chain in the validated implementation.
- [PROVED] Input-dependent branches and non-affine targets are not covered;
  A010 treats a bounded number of rational branches.
- [PROVED] The lower bound does not exclude polynomial-time evaluation:
  depth $\Theta(\log r)$ is polynomial in the input length.  It excludes only
  sublinear algebraic depth in the explicitly stated rational model.

## Outcome

- [PROVED] The proposed shallow branch-free circuit cannot be a transfer in
  the stated model.

## Post-mortem

**Why it failed:** [PROVED] Every arithmetic layer can at most double pole
degree, but injectivity forces degree at least $r/2$.

**What transfers:** [PROVED] The obstruction is a nearly tight sequential
depth lower bound, $d\ge n-O(\log n)$, for affine rational transfers.

**Would it work under different assumptions?** [PROVED] Linear depth in $n$,
input-dependent branching, a lift, or a proper target lies outside the failed
claim; Miller evaluation uses the first exit.
