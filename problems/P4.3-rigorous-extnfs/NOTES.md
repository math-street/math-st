# Notes

## Stable facts

[CITED] The exTNFS relation norms are the two iterated resultants written in `SMOOTHNESS_ASSUMPTIONS.md`; Kim--Barbulescu 2016 model their smoothness probabilities as those of arbitrary integers of the same sizes and multiply the probabilities.

[CITED] Canfield--Erdos--Pomerance rigorously give the required random-integer $L$-density, but not its transfer to polynomial or norm-form values.

[PROVED] The minimal relation-supply theorem is the joint lower bound (RC).  Separate marginal estimates do not imply it because both norms use the same coefficient vector.

[PROVED] The strongest smoothness obstacle is special-$q$ descent: (SQ) must hold uniformly over an adaptive family of short-vector boxes in lattices whose determinant and basis depend on the current prime ideal.

[CITED] Lee--Venkatesan's ordinary randomized NFS makes a polynomial evaluation vary in an arithmetic progression.  A tower retains a nonlinear outer field norm, so that proof does not directly transfer.

[CITED] Bender--Pomerance supply a rigorous finite-field DLP fallback.  In medium-characteristic notation its cost is $L_Q(1/2,\sqrt2+o(1))$ below the $\ell_p=1/2$ boundary and $L_Q(\ell_p,2c_p+o(1))$ above it, with boundary behavior depending on constants.

[EMPIRICAL: p=5, eta=2, kappa=3, A=4] Exact enumeration finds much larger joint smoothness and side dependence than a dyadic size-matched integer baseline for $B\in\{7,13,31,61\}$; this is finite evidence only.

[PROVED] A003 proves the degree-uniformity barrier: maintaining the standard $L_Q(2/3)$ relation norm scale for fixed $1/3<\ell_p<2/3$ forces $\eta=\Theta((\log Q/\log\log Q)^{2/3-\ell_p})$, so every fixed-degree smooth-form theorem misses the optimized interior regime.

[PROVED] A004 reduces the independent relation-rank gap to the escape condition $\inf_{\varphi\ne0}\Pr[\varphi(R)\ne0]\ge L_Q(1/3,-o(1))$ for accepted relation rows.

[PROVED] A005 gives an unconditional $L_Q(1/3,O(1))$ relation-supply algorithm on the restricted boundary family $p=L_Q(2/3,c_p)$, $p\equiv3\pmod4$, $\eta=2$, using a fixed Gaussian norm, kernel-preserving coefficient randomization, bounded lattice fibers, and irreducibility modulo an auxiliary prime above the smoothness bound.

## Working material

[CONJECTURE] For fixed $\eta=2$, a carefully chosen one-dimensional coefficient slice might turn the randomized outer norm into a quadratic polynomial to which a fixed-form theorem applies.  This would be refuted as an exTNFS route if the slice has too few candidates or forces norm coefficients/discriminants outside every uniform theorem needed for $L(1/3)$ supply.
