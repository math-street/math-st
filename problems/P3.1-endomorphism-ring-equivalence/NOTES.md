# Notes — P3.1

## Stable facts

- [CITED] Deuring's correspondence is algebraic; its basic statement does not require GRH (Deuring 1941).
- [CITED] Wesolowski 2022 proves the smooth $\ell$-path/endomorphism-ring equivalence in expected polynomial time under GRH.
- [CITED] Herlédan Le Merdy--Wesolowski 2026 prove the analogous equivalence unconditionally only for unrestricted isogeny degree and explicitly retain GRH for $\ell$-`IsogenyPath` to `EndRing`.
- [PROVED] The old proof has four genuine GRH leaves D1--D4; `GRH_USAGE_MAP.md` gives their complete dependency closure.
- [PROVED] The use of ordinary RH in Wesolowski's Theorem 6.4 can be replaced by the unconditional prime number theorem, but Theorem 6.4 remains conditional through Theorem 6.3.
- [PROVED] A003 replaces the fixed-binary-form prime sampler D2 by an unconditional direct rank-four sampler whose expected cost is polynomial in \(\log p\) and the numerical value of \(\ell\); D1, D3, and D4 remain.
- [PROVED] Brandt-class mixing does not transfer the checked average binary-form theorems through Proposition 3.5's deterministic LLL-and-gcd subform map; A002 records the probability-space mismatch.
- [PROVED] Ramification forces \(p\) into a coefficient, binary discriminant, or index in every integral orthogonal \(2+2\) norm split, so changing bases does not put the old norm equation in the unconditional Assing--Blomer--Li modulus range; A004 records the invariant obstruction.
- [PROVED] Effective quaternary representability does not construct a representation of one fixed target in polynomial time by ellipsoid rejection; the success loss is essentially one factor of the target integer, as recorded in A005.
- [PROVED] The 2026 flexible model removes the special-curve dictionary use of D1, but the old smooth-equivalent-ideal algorithm still needs the D1-small binary discriminant internally; A006 records why the direct hybrid fails.
- [EMPIRICAL: p=11, ell=3, 30 independent seeds] The local Deuring fixture recovered the ideal and quotient curve key, visited all four embedded neighbor right orders of trace discriminant \(11^2\), verified \(I\bar I=3O\), and returned through the dual kernel to the source curve key in 30/30 trials.
- [EMPIRICAL: p in {11,23,47,59,71}, ell=3, n=5] Exhaustive right-order-aware two-step timings fit an exponent 1.6796 with classical 95% interval \([1.2366,2.1226]\) and \(R^2=0.9798\); `TIGHTNESS_STATUS.md` explains why this is not yet a security-bit loss.

## Working terminology

- A **direct GRH use** is a lemma whose own proof invokes a GRH-conditional analytic theorem.
- An **inherited GRH dependency** is a result that calls a direct-use lemma without adding another analytic assumption.
- A reduction is **polynomial-time** only when its cost is polynomial in the bit length $\log p$ and in the explicit input/output lengths.

## GRH usage map

See `GRH_USAGE_MAP.md`.

## Current frontier

- [PROVED] Task 1 is not solved: the remaining old-route assumptions are D1, D3, and D4.
- [PROVED] The strongest single replacement target is a constructive polynomial-time fixed-target solver for the structured quaternary norm equation on an arbitrary maximal-order lattice; it would bypass the special-order dependency as well as the D3+D4 sampling mechanism.
- [PROVED] Task 2 is not solved: the recorded local path has no oracle call, so the bit-loss proxy cannot yet be evaluated.
