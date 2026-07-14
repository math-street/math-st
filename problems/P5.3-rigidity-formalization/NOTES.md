# Notes — P5.3

## Stable facts

- [PROVED] Under the fixed-menu game in `DEFINITIONS.md`, a designer with
  selection capacity \(b\) has success probability at most
  \(\min(1,2^b\kappa\epsilon)\); independence between candidates is not
  required.
- [PROVED] The requested \(\min(1,2^b\epsilon)\) bound is the uniform-source
  case \(\kappa=1\).
- [PROVED] Exact provenance \(b\) is not identifiable from a fixed published
  constant unless a source menu or an explicit sensitivity convention is
  supplied.
- [PROVED] A generator with an externally sampled, unbiasable random stream
  and a forced uniform-unranking rule has minimal designer freedom \(b=0\).
- [CONDITIONAL: ideal-XOF outputs are independent uniform byte strings] The
  SG-08 exact-rejection sampler is uniform over the coefficient encodings
  passing its fixed safety predicate, and has designer \(b=0\) when its beacon
  cannot be selected, restarted, or suppressed.
- [EMPIRICAL: bits=7, p=127, 8 beacon labels] Every smoke-run label found a
  passing curve by counter 13; three regression tests independently
  recomputed point counts, stopping, and safety data.
- [EMPIRICAL: exhaustive p=127 census] The 16,002 nonsingular coefficient
  encodings form 258 isomorphism classes; the safety predicate retains 4,179
  encodings in 67 classes with orbit histogram \(\{21:1,63:66\}\).
- [PROVED] Conditional on the census, coefficient-uniform class masses are
  \(1/199\) and \(3/199\), not \(1/67\), and their total-variation distance
  from class-uniform is \(132/13333\).
- [CONDITIONAL: ideal-XOF outputs are independent uniform byte strings] A004's
  rejection/unranking kernel is exactly uniform over the 67 canonical safe
  classes and has designer capacity \(b=0\) under a forced beacon.
- [PROVED] Uniform sampling is the unique distribution minimizing the maximum
  singleton probability on a fixed finite class universe.
- [CITED] Under audit profile A256, the conditional curve-core caps are P-256
  \(\leq161\), Curve25519 given \(p\) equal to 0, and brainpoolP256r1 equal
  to 0; secp256k1 and BLS12-381 are not identifiable from their cited source
  menus.

## Working material

The central distinction is between reproducibility (a fixed document
determines one curve) and provenance rigidity (the designer's admissible menu
before publication contains few independently screenable candidates). The
audit in `AUDIT.md` reports both curve-core and full-package projections.
