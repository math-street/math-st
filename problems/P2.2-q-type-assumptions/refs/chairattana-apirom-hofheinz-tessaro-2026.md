# Chairattana-Apirom--Hofheinz--Tessaro -- tight BBS security

Rutchathon Chairattana-Apirom, Dennis Hofheinz, and Stefano Tessaro, “Tight
Security for BBS Signatures,” EUROCRYPT 2026; IACR ePrint 2025/1973, revised
2026-02-20.

Primary record: <https://eprint.iacr.org/2025/1973>

## Relevant result

[CITED] The abstract states a tight reduction for BBS under $q$-SDH when each
message is signed at most once, including the common derandomized-signing use
case.

[CITED] For repeated signatures of the same message, the abstract states a
meta-reduction ruling out a tight algebraic reduction to $q$-SDH and the
variants considered by the paper.

[PROVED] Neither statement is a reduction from $q$-SDH to a fixed-size
assumption; the positive result retains the $q$-type premise and the negative
result concerns tightness for a signature scheme.

## Audit limit

[PROVED] The ePrint abstract and revision metadata were checked.  The exact
algebraic-reduction class and quantitative lower bound were not imported into
P2.2 beyond the abstract-level statement above.
