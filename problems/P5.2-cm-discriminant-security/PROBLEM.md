# P5.2 - Small CM discriminant and ECDLP security

## Formal statement

Let $E/\mathbb F_p$ be ordinary with complex multiplication by an order of
discriminant $D$, where $|D|$ is small.

Prove a polynomial-time reduction from ECDLP on small-$|D|$ curves to ECDLP
on general curves, or give a subexponential ECDLP algorithm exploiting
$|D|$.

## Initial empirical route

1. Construct and independently count curves for several small discriminants.
2. Implement Pollard rho modulo an efficiently computable endomorphism action.
3. Measure the speedup and separate constant factors from asymptotic effects.
4. Treat $D=-3$ and $D=-4$ separately because of their extra automorphisms.

## Validation targets

- Independently verify every constructed curve order.
- Verify the endomorphism equation on sampled points.
- Recover known discrete logarithms with both baseline and quotient walks.
- Record operation counts, effect sizes, sample counts, and confidence intervals.

## Scope

Only toy parameters with $\log_2 p\leq60$ are in scope.
