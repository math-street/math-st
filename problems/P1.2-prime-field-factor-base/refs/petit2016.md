# Petit–Kosters–Messeng 2016 — Algebraic prime-field factor bases

## Source

[CITED] Christophe Petit, Michiel Kosters, and Ange Messeng, “Algebraic
Approaches for the Elliptic Curve Discrete Logarithm Problem over Prime
Fields,” PKC 2016, LNCS 9615, pp. 3–18,
doi:10.1007/978-3-662-49387-8_1.
<https://people.maths.ox.ac.uk/petit/files/16PKC_primeECDLP.pdf>

## Results used here

[CITED] The paper restates Semaev's prime-field proposal with
$V=\{0,\ldots,B-1\}$ of size about $p^{1/m}$ and records that no relation
algorithm was supplied for this interval factor base.

[CITED] Its replacement defines the factor-base abscissas as the roots of a
large-degree rational map $L$ that decomposes into low-degree maps. One concrete
case takes a smooth-order multiplicative subgroup (or coset) of
$\mathbb F_p^*$; another uses the abscissas of a smooth subgroup on an
auxiliary elliptic curve.

[CITED] The paper leaves the Gröbner-basis complexity of the resulting
prime-field systems open and reports that its tested attacks remain slower than
generic discrete-logarithm algorithms at relevant parameters.

## Repository consequence

[PROVED] For a multiplicative subgroup $H$ of order
$n=\prod_i\ell_i$, the condition $x\in H$ is $x^n=1$ and can be expressed by
the chain $z_0=x$, $z_{i+1}=z_i^{\ell_i}$, $z_t=1$. If the factors $\ell_i$
are small, every equation in the chain has low degree.

## Scope

[PROVED] This construction is coordinate-aware and lies outside A009's
translate-probe model. The cited paper does not prove a polynomial or
sub-generic complexity bound for solving the full summation-polynomial system.

No published timing table was reproduced; A010 independently checks only the
factor-base predicate, composition chain, decomposition density, and generic
finder work at toy scale.
