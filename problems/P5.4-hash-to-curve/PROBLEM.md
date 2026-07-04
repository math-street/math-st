# P5.4 - Universal constant-time hash-to-curve

## Formal statement

For an elliptic curve $E/\mathbb F_q$ in short-Weierstrass, Montgomery, or
twisted-Edwards form, including $j=0$ and $j=1728$, construct an encoding
$f:\mathbb F_q\to E(\mathbb F_q)$ with a fixed field-operation schedule and
no input-dependent memory access.

The intended random-oracle construction is
$m\mapsto f(H_1(m))+f(H_2(m))$, including cofactor clearing when the target is
a proper prime-order subgroup.

The long-term goal is a single uniform construction, or a precisely delimited
compile-time family of constructions, together with an indifferentiability
argument and constant-time validation.

## Validation targets

- Validate standardized algorithms against RFC 9380 vectors when the global
  toy-parameter restriction permits it; otherwise use independent toy-scale
  ground truth and leave the standardized vector run explicitly open.
- Check that every output is on the target curve and, after cofactor clearing,
  in the requested subgroup.
- Audit source-level control flow and memory access, and supplement the audit
  with timing measurements.

## Scope

All experiments obey the shared ceiling $\log_2 q\leq 60$. Production-size
P-256, curve25519, secp256k1, and BLS12-381 executions are out of scope for
this repository session.
