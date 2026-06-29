---
attempt: A003
status: dead
---
# A003 — Turn the GHS structural fixture into an end-to-end toy transfer

## Idea

Use the existing binary-field Frobenius-span implementation to construct a
small GHS descent, map an elliptic-curve DLP into the descended Jacobian, and
solve the auxiliary DLP exhaustively.

## Prior art

[CITED] Gaudry, Hess, and Smart (2002) construct a homomorphism from the input
elliptic-curve group into a divisor-class group over the subfield. The existing
P1.4 fixture implements the exact Frobenius-span and genus invariant, not that
homomorphism or divisor arithmetic.

## Plan

1. Reuse the binary extension-field and genus-profile fixtures.
2. Construct the descended function field and explicit divisor map.
3. Enumerate the small target Jacobian and check preservation of a logarithm.

## Execution log

- Inspected the existing P1.4 implementation and tests.
- Verified that they compute Frobenius orbits, annihilators, span ranks, magic
  numbers, and the resulting genus.
- Checked the primary construction boundary: an end-to-end transfer additionally
  needs the descended function field, a conorm/norm or cover map, reduced-divisor
  arithmetic, and a target DLP.
- Rejected an exhaustive lookup table between source and target elements because
  defining that table by source discrete logarithms would make the validation
  circular.

## Outcome

[EMPIRICAL: binary fields of absolute degree 4, 6, and 8] The repository has a
tested structural GHS fixture that observes extension/subfield arithmetic and
the exact descent-genus invariant.

[PROVED] That fixture is not an implementation of the GHS DLP transfer because
it constructs neither the target divisor classes nor the group homomorphism.

## Post-mortem

**Why it failed:** The missing object is not a small arithmetic helper; it is
the explicit descended function field plus Jacobian and transfer-map machinery.
The available pure-Python code stops one categorical level earlier, at the
Frobenius-span invariant.

**What transfers:** The operation-matrix entries for coordinate arithmetic and
extension/subfield structure are directly observed. The auxiliary group law,
equality, and relation linear algebra remain literature-backed rather than
end-to-end observed in P1.1.

**Would it work under different assumptions?** Yes, with SageMath or Magma
function-field/Jacobian support, or after implementing the fixed-field and
reduced-divisor machinery requested by repository questions Q002 and Q003.
