# Frozen 26-bit cyclotomic-root extension - P4.2 session 3

This file was written before either 26-bit search was run.

## Space and completeness

[PROVED] Both searches cover distinct primes from 5 through \(2^{26}-1\) and
exact embedding degrees 3 through 12, with all primary Hasse, ordinarity,
orientation, rho, and candidate-ledger conventions unchanged.

[PROVED] Candidate completeness follows from
`CYCLOTOMIC_ROOT_ENUMERATION.md`. The new generator changes enumeration cost,
not the reported set.

## Prediction

[CONJECTURE] No new non-{(6,4),(4,6)} 2-cycle and no new directed 3-cycle hit
appears. Any such hit refutes the prediction. New residual near-misses are
allowed and must be assigned exact closing degrees.

## Construction rule

[PROVED] Every 2-cycle full hit newly appearing above 24 bits has degree pair
(6,4) or (4,6) if the prediction holds, and
`MNT_CLASSIFICATION.md` then supplies its parameter-level classification.
Explicit curve construction is required for any exceptional hit; MNT-pattern
rows may first be certified arithmetically before deciding whether duplicating
hundreds of already validated model searches adds information.
