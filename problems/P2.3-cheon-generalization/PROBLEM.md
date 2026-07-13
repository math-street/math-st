# P2.3 — Generalizing Cheon's attack

## Formal research target

Let \(G=\langle g\rangle\) be a cyclic group of prime order \(n\). Given
\(g,g^{f_1(x)},\ldots,g^{f_k(x)}\) for fixed, public polynomials
\(f_i\in\mathbb Z[X]\), recover \(x\).

The long-term task is to express the recovery complexity through algebraic
invariants of the polynomial family, extend the known special-case attacks,
and seek matching generic-group lower bounds.

## Session-1 scope

Reproduce the \(d\mid n-1\) attack from the input
\((g,g^x,g^{x^d})\), validate recovery on toy instances, and measure whether
the operation-count scaling near \(d\approx\sqrt n\) is compatible with an
\(n^{1/4}\) exponent. The non-divisor and general-polynomial questions remain
later sub-goals.

