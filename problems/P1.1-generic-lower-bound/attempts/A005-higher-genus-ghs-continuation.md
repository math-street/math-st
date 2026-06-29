---
attempt: A005
status: dead
---
# A005 — Strengthen the GHS fixture to a genuine genus-two transfer

## Idea

Use a quadratic binary extension $K/k$ and a magic-number-two source curve.
Construct the semilinear fixed field explicitly, convert it to a genus-two
hyperelliptic equation, map source places by conorm/norm, and solve the image
DLP with Mumford divisor arithmetic.

## Prior art

[CITED] The original GHS construction defines a computable homomorphism from
$E(K)$ to the fixed curve's divisor-class group. Florian Hess's KASH code maps
places by conorm and norm and checks that a source scalar relation is preserved
by the resulting divisors.

## Execution log

- Re-read the original request and identified the genus-one A004 fixture as
  too weak to observe the actual higher-genus GHS attack row.
- Reconstructed the quadratic-extension fixed variables for conjugate binary
  curves and derived a candidate magic-number-two genus-two equation.
- Identified the remaining implementation layers: generalized Cantor/Mumford
  arithmetic in characteristic two, place-to-divisor conversion, divisor
  reduction, scalar-preservation checks, and a source Pollard-rho comparison.
- Stopped before writing or validating those layers when the user directed
  that the task be marked failed.

## Outcome

No genuinely higher-genus source-to-Jacobian transfer was implemented. No
new executable evidence was produced, and the task remains below its requested
full validation endpoint.

## Post-mortem

**Why it failed:** The previous completion boundary accepted an exact but
degenerate genus-one specialization. Correcting that boundary requires a new
Jacobian arithmetic and divisor-map stack, not a small extension of A004, and
that stack was not completed.

**What transfers:** The quadratic fixed-field derivation narrows a future
restart to a genus-two characteristic-two Mumford implementation plus an
explicit conorm/norm divisor fixture.

**Would it work under different assumptions?** A verified SageMath, Magma, or
KASH environment could supply the fixed-field reduction and divisor mapping;
alternatively, the repository would need its own independently tested
generalized Cantor implementation.
