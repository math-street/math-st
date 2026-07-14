---
attempt: A001
status: promising
---
# A001 - Explicit small simultaneous lifts

## Idea

[CITED] Reductions of the fixed rank-one curve 37.a1 and its first four
generator multiples give simultaneous lifts whose canonical heights do not
grow with $p$ at its infinitely many good primes.

## Prior art

[CITED] Jacobson, Koblitz, Silverman, Stein, and Teske (2000) analyze the
xedni construction through relation coefficients, discriminants, and Lang's
height conjecture; `refs/jacobson-et-al2000.md` records the checked result.

## Plan

1. Validate curve arithmetic and the height routine.
2. Fix a rational curve with one known non-torsion point and use its first four
   multiples as simultaneous lifts.
3. Reduce the curve and points at seeded toy primes of good reduction.
4. Compare this adversarial construction with a stated random-lift procedure.

## Execution log

Pre-registered before environment checks and experiments.

[PROVED] A direct short-Weierstrass construction gives an $O(\log p)$
canonical-height upper bound for every single target point.

[PROVED] A five-coefficient linear construction gives the same upper bound for
$k\leq4$ whenever the coordinate constraint matrix has full row rank modulo
$p$.

[EMPIRICAL: six primes from 31 to 32719, three trials per prime] Exact
measurements, fits, and residuals support logarithmic growth for the specified
least-norm construction.

## Outcome

[PROVED] The attempt refutes the literal height lower bound without a
Mordell-Weil-rank/dependence constraint.

[PROVED] It does not revive xedni calculus because neither the proof nor the
random experiment makes the lifted points dependent.

## Post-mortem

**Why it did not solve the attack-relevant problem:** [PROVED] Low-height
simultaneous lifting and low rational rank are different constraints; the
linear coefficient construction guarantees the former and says nothing about
the latter.

**What transfers:** [PROVED] Any future formulation must exclude the explicit
$O_k(\log p)$ lift family through a precise rank, dependence, and finite-field
no-small-relation condition.

**Would it work under different assumptions?** [CONDITIONAL: an efficient
procedure that makes the constructed points dependent while preserving the
finite-field no-small-relation condition] The construction would become a
xedni-style attack.
