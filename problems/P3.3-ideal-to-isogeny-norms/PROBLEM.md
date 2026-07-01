# P3.3 - Optimality of ideal-to-isogeny translation

## Formal target

Let $\mathcal O$ be a maximal order in $B_{p,\infty}$ and let $I$ be a left
$\mathcal O$-ideal. Find, in polynomial time, an equivalent ideal $J\sim I$
with the same left order and class such that

$$
N(J)\le p^{1/2+o(1)}.
$$

Alternatively, define a precise KLPT-style strategy class and prove that no
algorithm in that class reaches this bound.

## Experimental route

The requested first deliverables are:

1. validate KLPT and measure its output norms if an implementation is present;
2. otherwise, construct ideal norm lattices and establish the short-vector
   target independently;
3. compare norm-aware lattice reduction with exact shortest-vector search at
   small $p$;
4. measure dependence on the sampled ideal, input norm, and congruence data;
5. state a structural-versus-algorithmic verdict limited to the measured
   parameter range.

All experiments remain below the repository ceiling $\log_2 p\le 60$.
