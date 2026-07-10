# Maurer--Wolf 1999

[CITED] Ueli M. Maurer and Stefan Wolf, "The Relationship Between Breaking the
Diffie--Hellman Protocol and Computing Discrete Logarithms," *SIAM Journal on
Computing* 28(5), 1689--1721, 1999. DOI: 10.1137/S0097539796302749.

Primary text checked at:
<https://crypto.ethz.ch/publications/files/MauWol99b.pdf>

## Main result in repo notation

[CITED] For a large single prime divisor $p$ of the input group order, a
constant-rank auxiliary abelian group over $\mathbb F_p$ with known
$B$-smooth order lets a DH oracle recover the input discrete logarithm modulo
$p$ (Definitions 1--5 and Theorem 2).

[CITED] Elliptic curves over $\mathbb F_p$ supply strongly algebraically
defined rank-at-most-two auxiliary groups, with embedding by a randomized
$x$-coordinate shift (Section 4.1.1).

[CITED] The paper defines $\nu(p)$ as the smallest largest prime factor among
orders in the Hasse interval and assumes $\nu(p)=(\log p)^{O(1)}$ for its
general non-uniform polynomial-time equivalence (Definition 6, Theorem 3,
Corollary 4).

## Assumptions and limits

[CITED] The curve parameters can be supplied as side information; the
existence theorem is therefore not a uniform curve-construction algorithm.

[PROVED] In the prime-order P2.1 setting, the paper's condition about repeated
large prime factors of the input group order is vacuous.

## Verification performed

[EMPIRICAL: source pages 7--18 inspected] The oracle definition, implicit
field operations, strong algebraic definition, reduction steps, curve
embedding, Hasse interval, $\nu(p)$, and smoothness assumption were checked
directly in the primary PDF.

[EMPIRICAL: PDF pages 9--10 visually re-audited 2026-07-10] Definition 4
requires an `EMBED(x,e)` algorithm with expected at most $\alpha$ algebraic
operations over a uniformly random public $e$, a correct
`EXTRACT(EMBED(x,e),e)=x`, and extraction time at most $\alpha$.  Theorem 2
also requires bounded group rank, known smooth order, and polynomially bounded
$m,\alpha,B$.  Thus an abstract abelian variety or Weil polynomial alone is
not a valid auxiliary group.
