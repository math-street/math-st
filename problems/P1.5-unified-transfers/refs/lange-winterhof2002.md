# Lange--Winterhof 2002

- [CITED] Tanja Lange and Arne Winterhof, "Polynomial Interpolation of the
  Elliptic Curve and XTR Discrete Logarithm," COCOON 2002, LNCS 2387,
  137--143, doi:10.1007/3-540-45655-4_16.
- [CITED] Their elliptic-curve Theorem 1 studies a polynomial in the
  $x$-coordinate that returns a fixed finite-field encoding of the scalar
  $n$ for $nP$, with the sampled exponents lying densely in an interval.
  The addition formula and two neighboring samples give a degree lower bound
  linear in the interval length after subtracting the missing-sample and
  base-$p$ carry losses.
- [CITED] Their XTR Theorem 2 applies to an arbitrary subset $S$ but gives

  \[
  d\ge \frac{|S|(|S|-1)}{5(\ell-1)(2p-1)},
  \]
  and their multiplicative-subgroup Theorem 4 has the same quadratic
  subset-over-ambient-size form with an additional base-$p$ digit/carry
  factor.
- [PROVED] The elliptic theorem computes the discrete-log scalar from one
  coordinate on a structured exponent set. It does not cover a map
  homomorphic on an arbitrary subset into an arbitrary affine algebraic
  group, nor an adversarial partition into unrelated branch maps.

Primary source: <https://doi.org/10.1007/3-540-45655-4_16>.
