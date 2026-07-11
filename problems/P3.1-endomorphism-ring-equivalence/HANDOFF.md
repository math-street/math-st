# Handoff - P3.1 - after session 2

## State in five lines

[PROVED] P3.1 is partial, not resolved.
[PROVED] A003 gives a repo-internal unconditional replacement for D2; D1, D3, and D4 remain.
[PROVED] A002, A004, A005, and A006 are dead with precise mathematical post-mortems.
[EMPIRICAL: p=11, ell=3, 30 independent seeds] The right-order-aware dual two-step Deuring fixture passed 30/30 trials.
[EMPIRICAL: p in {11,23,47,59,71}, ell=3, n=5] Five exhaustive toy timings have stored residuals, but they do not identify security-bit loss.

## What is established

- [PROVED] `GRH_USAGE_MAP.md` classifies the original proof's four direct leaves D1--D4 and all inherited uses.
- [PROVED] A003 replaces Proposition 3.8 by direct rank-four residue-lattice sampling using effective quaternary theta bounds, explicit primes in progressions, and fixed-rank CVP.
- [EMPIRICAL: p<=31, ell in {3,5}, q<=3000] A003's 22-case refutation grid had no reciprocity violation; scaled prime density ranged from 0.832 to 1.815.
- [EMPIRICAL: p=11, ell=3, 30 independent seeds] Every ideal, right-order, dual-product, and terminal-curve check matched; all four embedded neighbor orders had discriminant 121, every product was $I\bar I=3O$, and every dual quotient returned the source class, with Wilson 95% interval approximately [0.886,1].
- [EMPIRICAL: p in {11,23,47,59,71}, ell=3, n=5] The exhaustive right-order-aware two-step cost exponent is 1.6796, with classical 95% interval [1.2366,2.1226] and R-squared 0.9798.

## What is ruled out

- [PROVED] A002: Brandt mixing does not control the deterministic binary-subform pushforward needed by average-form theorems.
- [PROVED] A004: an integral orthogonal 2+2 split cannot hide the ramified prime p from every modulus/discriminant/index.
- [PROVED] A005: ellipsoid rejection for one fixed quaternary target loses essentially a factor n and is exponential in log n.
- [PROVED] A006: the flexible dictionary removes D1 from conversion, but not the small-discriminant dependency inside the old norm-equation solver.

## Active thread

A003 is promising and removes D2 only. The main theory target is a constructive fixed-target quaternary solver on arbitrary maximal-order lattices. The implementation thread is SG-03f, non-backtracking dictionary propagation across a second ideal.

## Next action

For p=11 and ell=3, represent a non-dual norm-3 ideal in the first embedded right order, propagate its action to the intermediate curve, and identify the terminal right order without an exhaustive curve-key lookup.

## Invariants - do not violate

- [PROVED] Keep unrestricted `Isogeny` separate from prescribed/smooth `ell-IsogenyPath`.
- [PROVED] Treat A003 as a repo-internal proof candidate, not a published resolution of P3.1.
- [PROVED] D1, D3, and D4 remain; do not report the full equivalence as unconditional.
- [PROVED] The timing fit measures exhaustive toy enumeration and cannot be used as a security-bit loss.
- Preserve the current tuple-based `PrimePolynomialField` API in `lib/finite_fields.py`.

## Files that matter

`GRH_USAGE_MAP.md`; `attempts/A003-direct-quaternary-prime-sampler.md`; `TIGHTNESS_STATUS.md`; `DEURING_ROUNDTRIP_SPEC.md`; `REDUCTION_COST_SPEC.md`; `lib/quaternion.py`; `code/toy_deuring_roundtrip.py`; `code/fit_roundtrip_cost.py`; `data/fit_roundtrip_cost_ell3_p11-71_20260711.csv`.

## What I would tell my replacement

The modern flexible dictionary is not the missing smoothness theorem. It removes the need for a special curve at conversion time, but the old ideal-smoothing core still depends on a D1-small quadratic suborder and on D3+D4. Attack the constructive fixed-target quaternary equation or complete the right-order round-trip fixture; do not return to least-prime bounds alone.
