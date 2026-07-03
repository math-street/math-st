# P1.6 - The height obstruction to lifting

## Formal target

Let $E/\mathbb F_p$, let $\widetilde E/\mathbb Q$ have good reduction
$E$ at $p$, and let $\widetilde P\in\widetilde E(\mathbb Q)$ reduce to
$P\in E(\mathbb F_p)$.

The proposed target is a lower bound
$\widehat h(\widetilde P)=\Omega(p^c)$ for an explicit $c>0$, uniformly over
the lifts satisfying the constraints needed by a xedni-calculus attack.

## Operational target for this repository

- Decide whether the literal uniform statement is tenable.
- Measure one- and multi-point lifts at toy primes, with the height convention
  and lift-sampling rule stated explicitly.
- Separate data by the number of prescribed reductions and by Mordell-Weil
  rank when a rank routine is available.
- Fit a growth law with stored residuals and state a falsifiable conjecture.
- State precisely what additional hypotheses and height-theoretic input a
  proof of an attack-relevant theorem would require.

## Falsifiers

- A proof of the constrained lower bound with an explicit exponent resolves
  the stated target positively.
- A construction satisfying the actual attack constraints with heights
  polynomial in $\log p$ refutes the proposed obstruction in that model.
- A low-height construction outside the attack constraints refutes only the
  literal uniform statement and identifies a missing hypothesis.

## Current disposition

[PROVED] The literal uniform statement is false: `NOTES.md` constructs
$O(\log p)$ single-point lifts and, under an explicit row-rank condition,
$O_k(\log p)$ simultaneous lifts for $k\leq4$.

[PROVED] The construction does not impose rational dependence or total rank
below $k$, so the attack-relevant refinement is not resolved.

[CITED] The primary 2000 failure analysis uses a conditional bound on relation
coefficients together with finite-group counting rather than the lower bound
stated in the prompt.
