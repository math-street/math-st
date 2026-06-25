# Log — P5.3

## Session 1 — 2026-06-25

**Goal:** Define a sound rigidity game and choice accounting, prove its main
bound, and use primary specifications to audit five named standard curves.

**Prediction (written before running literature or mathematical checks):** The
bound \(\min(1,2^b\epsilon)\) will follow by a union bound only when the weak
set and designer menu are fixed independently of the generator's fresh random
experiment and every menu entry has weak-set probability at most \(\epsilon\).
Published standards will support exact replay descriptions, but most will not
identify the historical alternative menu, so honest provenance values of
\(b\) will require bounds or an explicit sensitivity profile rather than a
single unconditional number.

**Did:**

- Initialized the P5.3 problem folder and A001.
- Ran `env/check_env.py` and the shared library tests: Python 3.13.4 was
  available, SageMath/Singular/msolve were unavailable, and all 39 tests
  passed.
- Defined a fixed-menu selective-generation game, category accounting,
  projection-sensitive selection capacity, and a reference-source domination
  factor.
- Proved the union bound, gave tight examples, and recorded three quantifier
  failures.
- Constructed an ideal minimal-designer-freedom generator and separated its
  information-theoretic statement from a conditional XOF/beacon refinement.
- Audited P-256, Curve25519, brainpoolP256r1, secp256k1, and BLS12-381 from
  primary specifications or the original construction source.
- Added six source records, repository bibliography/glossary entries, and two
  concrete open questions.
- Implemented and tested the SG-08 toy exact-rejection sampler. The final
  combined suite passed 58 tests, including 3 P5.3 tests.

**Found:**

- [PROVED] If every candidate marginal is dominated by \(\kappa\nu\) and the
  safe weak-set mass under \(\nu\) is at most \(\epsilon\), success is at most
  \(\min(1,2^b\kappa\epsilon)\); candidate independence is unnecessary.
- [PROVED] The requested \(\min(1,2^b\epsilon)\) result is the uniform-source
  case, and it is tight for correlated translated candidates with disjoint
  hit events.
- [PROVED] Without fresh randomness independent of the weak set, \(b=0\)
  expresses reproducibility but does not itself give a probability bound.
- [CITED] Under A256, P-256 has a curve-core cap of 161 bits conditional on
  its field/model/hash rule; Curve25519 given \(p\) and brainpoolP256r1 have
  zero core bits; Curve25519 and Brainpool each expose at most one
  package-only sign bit under the full affine-point projection.
- [CITED] The audited SEC 2 section for secp256k1 and the original BLS12-381
  construction note do not expose finite menus from which unconditional
  provenance \(b\) values can be computed.
- [CONDITIONAL: ideal-XOF outputs are independent uniform byte strings] The
  toy first-passing sampler is uniform over the coefficient encodings passing
  its fixed public predicate.
- [EMPIRICAL: bits=7, p=127, 8 beacon labels] All smoke labels passed by
  counter 13; deterministic replay and independent point enumeration passed.

**Prediction vs. outcome:** matched. The union bound required a marginal
source condition in addition to the quantifier order, and the audit produced
conditional caps plus explicit non-identifiability rather than five
unconditional historical numbers.

**Did not work:** Treating encoded literal length as designer freedom was
rejected because it confuses deterministic outputs with menu size. A single
combined patch also failed on legacy repository text encoding; it was split
into isolated, non-destructive edits with no partial change.

**Changed my mind about:** A deterministic zero-choice generator is not by
itself the desired probabilistic construction. The clean minimum needs either
fresh entropy outside the designer's control or an explicit distribution on
weak sets.

**Next:** Investigate Q014 using archival, pre-publication sources for finite
secp256k1 or BLS12-381 candidate menus; do not replace missing evidence with
later folklore.
