# Code

- `observe_coordinate_bypass.py` runs BSGS twice on a known 19-element curve:
  once through the charged group interface and once through the identical
  affine formulas classified as free coordinate arithmetic.
- `observe_semaev_decomposition.py` enumerates factor-base $x$-coordinates,
  filters pairs with $f_3$, lifts the possible signs, and verifies a two-point
  decomposition by the curve law.
- `observe_smart_attack.py` lifts an anomalous order-17 curve modulo $17^2$,
  computes projective $p$-multiples, and recovers the logarithm from the ratio
  of formal-group parameters.
- `observe_mov_transfer.py` evaluates the published order-11 reduced Tate
  pairing fixture on $y^2=x^3+x$ over $\mathbb F_{43^2}$, checks the reduced
  values and bilinearity, and recovers the same logarithm in the target group.
- `observe_extension_decomposition.py` expands an $f_3$ relation over the
  polynomial basis of $\mathbb F_{5^3}$, restricts factor-base $x$-coordinates
  to $\mathbb F_5$, and verifies the unique lifted two-point relation.
- `observe_ghs_transfer.py` implements the odd-degree, genus-one GHS
  conorm/norm specialization over $\mathbb F_{2^{10}}/\mathbb F_{2^2}$,
  verifies all scalars in a prime order-three source subgroup, and recovers
  the source logarithm on the six-point auxiliary elliptic curve.
- `tests/test_observations.py` runs all six fixed observation fixtures as
  known-answer tests; the suite completes in under one second.

The higher-genus GHS construction primitive remains cross-validated by the
independent binary Frobenius-span fixture in
`../../P1.4-weil-descent-classification/code/verify_published_example.py`. That
fixture constructs the exact descent genus invariant. The local end-to-end
fixture is deliberately genus one and therefore does not claim a higher-genus
Jacobian implementation or an asymptotic attack speedup.
