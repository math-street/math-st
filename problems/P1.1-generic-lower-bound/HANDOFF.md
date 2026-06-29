# Handoff — P1.1 closed as failed

## Overall status

**FAILED.** The formal free-coordinate model analysis is useful and its tests
pass, but the requested full endpoint was not reached. The executable GHS
transfer is only the degenerate genus-one specialization; no genuinely
higher-genus Jacobian transfer or meaningful attack-cost comparison exists in
the repository.

## What remains valid

- [PROVED] `MODEL.md` compiles elliptic-curve addition and coordinate attacks
  into the zero-charge coordinate fragment of $\mathsf{CCA}_0$.
- [PROVED] `READ_ONLY_MODEL.md` shows that removing `PACK` is insufficient
  because derived points can remain virtual coordinate tuples.
- [PROVED] An explicit canonical group representation with a free
  representation-level law has zero separately charged group-oracle DLP cost.
- [EMPIRICAL] Coordinate BSGS, Smart, MOV, Semaev decomposition, extension-field
  decomposition, and the genus-one GHS boundary fixture pass their fixed tests.

## Why the task failed

The genus-one A004 fixture was presented as closing the GHS validation row.
Although algebraically exact, it does not exercise a higher-genus Jacobian,
divisor-class arithmetic, or the class-group DLP used by the actual GHS
attack. Treating that boundary case as the final endpoint was too weak.

Work began on a quadratic-extension, magic-number-two construction and a
genus-two fixed curve, but the fixed-field reduction, Mumford/Jacobian group
law, non-circular point transfer, and DLP comparison were not implemented or
validated.

## Attempt history

- A001: promising negative result for syntactically charged `ECADD`.
- A002: dead read-only-handle repair.
- A003: dead higher-genus structural-to-transfer attempt.
- A004: valid genus-one transfer, but insufficient for full GHS validation.

## Restart condition

A future restart must complete all of the following before changing the
overall status:

1. Construct a genuinely genus-two-or-higher GHS fixed curve from a binary
   source curve.
2. Implement and independently test its Jacobian divisor arithmetic.
3. Map a source subgroup without using a source-logarithm lookup table.
4. Verify scalar preservation and solve the auxiliary DLP.
5. Compare the observed auxiliary cost with a source Pollard-rho baseline and
   state exactly what the toy result does and does not imply.

## Files that retain value

- `MODEL.md`, `READ_ONLY_MODEL.md`: formal models and no-go proofs.
- `NOTES.md`: operation matrix and Shoup-opacity audit.
- `REVIEW.md`: scoped findings plus explicit failure notice.
- `attempts/A001-*` through `A004-*`: attempt history.
- `lib/binary_curves.py`, `lib/ghs_transfer.py`: genus-one-only machinery.
- `code/tests/test_observations.py`: passing fixed regression tests.
