---
attempt: A006
status: dead
---
# A006 - Combine the unconditional flexible model with smooth conversion

## Idea

- [CONJECTURE] Replace the special quaternion model and global dictionary behind D1 by the flexible model and local quaternion/endomorphism dictionary of Herledan Le Merdy--Wesolowski, while retaining A003 and any smooth part of the older reduction.
- [CONJECTURE] A refuting source check is an unavoidable call to arbitrary-ideal-to-isogeny conversion whose output degree is not controlled by the input ideal norm or by a fixed smoothness bound.

## Prior art

- [CITED] Herledan Le Merdy--Wesolowski 2026 prove an unconditional equivalence for unrestricted `Isogeny`, `EndRing`, and `MaxOrder` using flexible quaternion models, a local dictionary, and arbitrary-ideal-to-isogeny translation.
- [CITED] The same paper explicitly leaves the reduction from prescribed-degree `IsogenyPath` to `EndRing` GRH-conditional.

## Plan

- [PROVED] Trace the flexible-model translation and arbitrary-ideal conversion separately, recording whether either operation preserves ideal norm or outputs a smooth isogeny chain.
- [PROVED] Classify D1 as removable only if the replacement supplies every dictionary operation used by the smooth reduction without introducing an uncontrolled-degree isogeny.

## Execution log

- [CITED] Proposition 13 of Herledan Le Merdy--Wesolowski 2026 converts an explicit endomorphism-ring basis into a flexible MOER model and dictionary unconditionally, with cost polynomial in the bit lengths of the basis elements.
- [CITED] Proposition 4 of the same paper converts any ideal to an efficiently represented isogeny without requiring the ideal norm to be smooth.
- [CITED] Proposition 12 uses these tools to convert a connecting ideal directly into an unrestricted isogeny; it makes no prescribed-smooth-degree guarantee.
- [CITED] Wesolowski 2022, Algorithm 2 and Corollary 5.8, do not operate only at the dictionary layer: they solve the smooth-equivalent-ideal problem inside the special order \(O_0\), whose quadratic suborder has discriminant \(O((\log p)^2)\) only through D1.
- [CITED] The proof of Wesolowski 2022, Theorem 5.1, performs an exhaustive search modulo the binary discriminant; its stated complexity is polynomial in the numerical discriminant, not merely its bit length.
- [PROVED] Replacing the special model by an unconditionally found flexible model therefore removes the special-curve enumeration but does not provide a small-discriminant binary suborder on which Algorithm 2 remains polynomial-time.
- [PROVED] An auxiliary model parameter of size \(p^{O(1)}\) has polynomial bit length, but a loop polynomial in its numerical value is exponential in the input length \(\log p\).

## Outcome

- [PROVED] The flexible-model machinery bypasses the dictionary manifestation of D1, but it does not remove D1 from the old smooth-equivalent-ideal algorithm.
- [PROVED] The proposed direct hybrid therefore fails to reduce the current frontier below D1+D3+D4.
- [PROVED] A constructive fixed-target quaternary norm solver that works on arbitrary maximal-order lattices would bypass this special-order dependency together with D3 and D4; this is the precise target isolated by A005.

## Post-mortem

**Why it failed:**

- [PROVED] D1 is used twice in the old route, and the new local dictionary removes only the curve/dictionary use; the small binary discriminant remains embedded in the norm-equation algorithm.

**What transfers:**

- [PROVED] Future smooth-path constructions may use Proposition 13 to obtain a dictionary without a special curve, provided their ideal-smoothing step works directly on an arbitrary maximal-order norm lattice.

**Would it work under different assumptions?**

- [CONDITIONAL: constructive arbitrary-order fixed-target norm solver] Yes; after producing a smooth equivalent ideal in the flexible order, the explicit MOER dictionary and ideal-to-isogeny machinery supply the algebraic conversion layer without D1.
