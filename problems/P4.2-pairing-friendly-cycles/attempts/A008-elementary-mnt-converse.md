---
attempt: A008
status: promising
---
# A008 - Elementary converse for degree-(4,6) cycles

## Idea

Use the field gap \(c=q-p\), cyclotomic divisibility, and Hasse's bound to show
that every exact degree-(6,4) or degree-(4,6) 2-cycle lies on the MNT cycle
polynomials.

## Plan

1. Reduce \(\Phi_4\) and \(\Phi_6\) modulo the opposite cycle prime.
2. Express \(c^2+1\) as a small multiple of one field prime.
3. Use the other divisibility to show that prime divides the multiplier minus
   one.
4. Apply the Hasse bound to force the multiplier to be one.
5. Verify every such 22-bit hit against the resulting parameter formulas.

## Outcome

[PROVED] The complete argument is in `MNT_CLASSIFICATION.md`.

[EMPIRICAL: all 71 degree-{4,6} hits below 2^22] The verification script
matched every hit to an integer parameter: 40 MNT6-to-MNT4 orientations and
31 MNT4-to-MNT6 orientations
(`data/verify_mnt_parameterization_n71_20260627.csv`).
