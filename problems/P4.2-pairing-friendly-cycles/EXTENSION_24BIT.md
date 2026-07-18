# Frozen 24-bit targeted extension - P4.2 session 3

This file was written before either 24-bit search was run.

## Space

[PROVED] Both searches cover distinct primes from 5 through \(2^{24}-1\),
with every exact embedding degree in 3 through 12 for a hit. All Hasse,
ordinarity, orientation, rho, candidate-ledger, and explicit-construction
conventions are unchanged from the primary space.

## Algorithms and completeness

[PROVED] The targeted 2-cycle search enumerates every Hasse-valid unordered
prime pair and computes both bounded exact degrees. It retains every full hit
and every one-sided near-miss.

[PROVED] The target-edge 3-cycle join retains every full hit and every
two-of-three near-miss. Its proof is in `EXTENSION_20BIT.md`, and both targeted
algorithms reproduce exhaustive ledgers at all overlapping bounds.

## Predictions

[CONJECTURE] No newly appearing 2-cycle hit has a degree pair outside
{(6,4),(4,6)}, and no new full directed 3-cycle appears. Either event refutes
the prediction.

[CONJECTURE] Any new repeated equal-gap degree-(4,6) near-miss is an MNT-chain
orientation by `MNT_PATH_CLASSIFICATION.md`. The search may add isolated
residual rows; every one must be canonicalized and assigned its exact closing
degree before interpretation.

## Validation rule

[CONJECTURE] Every newly appearing full hit can be instantiated as explicit
curves and independently counted. An exhausted declared construction bound or
an order mismatch blocks reporting that hit as exhibited.
