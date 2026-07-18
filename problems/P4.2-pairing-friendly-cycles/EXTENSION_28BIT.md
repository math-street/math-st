# Frozen 28-bit cyclotomic-root extension - P4.2 session 3

This file was written before either 28-bit search was run.

## Space

[PROVED] Both searches cover distinct primes from 5 through \(2^{28}-1\),
with exact embedding degrees 3 through 12 and all primary cycle conventions
unchanged.

[PROVED] `CYCLOTOMIC_ROOT_ENUMERATION.md` proves that the generator retains
every full hit and the required near-miss ledgers.

## Prediction

[CONJECTURE] The only 2-cycle hits outside degree patterns (6,4) and (4,6)
remain the five examples below field 32, and no new full directed 3-cycle
appears. Any counterexample refutes the prediction.

[CONJECTURE] New directed near-misses may be MNT-chain rows or isolated
residuals. Every residual must be preserved with its exact closing degree; no
family label is assigned from a single row.

## Post-run result

[EMPIRICAL: primes below \(2^{28}\), exact degrees 3 through 12] The 2-cycle
ledger has 333 hits, comprising 328 MNT-pattern rows and the same five tiny
exceptions. The directed ledger has the same five hits and 61 near-misses.
All four rows newly appearing above 26 bits are MNT-chain orientations at
\(x=5967,7095\); no residual row was added.
