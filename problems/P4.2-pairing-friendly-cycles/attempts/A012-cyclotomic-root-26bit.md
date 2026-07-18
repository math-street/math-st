---
attempt: A012
status: promising
---
# A012 - Cyclotomic-root enumeration and 26-bit extension

## Idea

Generate only exact-order residues instead of scanning every Hasse-near prime
pair, prove candidate completeness, validate at 24 bits, and extend two bits.

## Predeclared outcome criteria

[CONJECTURE] Root-generated ledgers match the 24-bit Hasse-scan ledgers
exactly. At 26 bits, no exceptional 2-cycle and no new full 3-cycle appears.
Either mismatch refutes the corresponding prediction.

## Execution log

- [EMPIRICAL: 24-bit primary spaces] Both root-generated candidate CSVs are
  byte-identical to the Hasse-scanned CSVs. Runtime fell from about 405 seconds
  each to 20.4 seconds for 2-cycles and 28.4 seconds for 3-cycles.
- [PROVED] Candidate completeness is established in
  `CYCLOTOMIC_ROOT_ENUMERATION.md`.

## Outcome

[EMPIRICAL: primes below \(2^{26}\), exact degrees 3 through 12] The 2-cycle
ledger has 206 hits, of which exactly the original five are exceptional. The
directed 3-cycle ledger still has five hits and now has 57 near-misses.

[EMPIRICAL: nine newly appearing 3-cycle near-misses] Eight are MNT-chain
orientations at \(x=3003,3048,3153,3507\). The remaining path is
\((24106111,24103481,24100957)\), has target degrees (8,9), signed gaps
\((-2630,-2524)\), and closing degree 12,053,055.

The full-hit prediction matched. The residual family picture changed by one
isolated row, which is retained rather than folded into the MNT theorem.
