# Frozen 22-bit targeted extension - P4.2 session 2

This file was written before either 22-bit search was run.

## Space

[PROVED] Both searches cover distinct primes from 5 through \(2^{22}-1\),
with exact embedding degrees 3 through 12 and all primary Hasse, ordinarity,
orientation, rho, candidate-ledger, and explicit-validation conventions
unchanged.

## Algorithms and completeness

[PROVED] The targeted 2-cycle algorithm enumerates every Hasse-valid unordered
prime pair and computes both bounded exact degrees before discarding a row. It
omits only Frobenius-discriminant factorization for pairs with neither target
degree; such a pair cannot be a hit or a one-sided near-miss.

[PROVED] The targeted 3-cycle coverage proof is in `EXTENSION_20BIT.md`. It
finds every full hit and every two-of-three near-miss without enumerating
triangles having at most one target edge.

[CONJECTURE] Candidate rows and Hasse-edge/pair counts from both targeted
algorithms must match their older exhaustive versions at every prior bound.
Any mismatch blocks use of the 22-bit output.

## Prediction

[CONJECTURE] Newly appearing 2-cycle hits will all have degree pair (6,4) or
(4,6), and no new full directed 3-cycle will occur. New near-misses are allowed
and must have their missing exact degrees recorded.

## Post-run result

[EMPIRICAL: primes below 2^22, exact degrees 3 through 12] The prediction
matched. There are 76 2-cycle hits, of which 29 are new relative to 20 bits
and all have degree pair (6,4) or (4,6). There remain exactly five directed
3-cycle hits; two new two-of-three near-misses have missing exact degrees
556,386 and 1,949,325. Full counts and construction certificates are recorded
in `attempts/A007-targeted-22bit-extension.md`.
