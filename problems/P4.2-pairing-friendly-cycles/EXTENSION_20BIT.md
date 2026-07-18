# Frozen 20-bit extension - P4.2 session 2

This file was written before either 20-bit search was run.

## Fixed and changed axes

[PROVED] The exclusive prime bound is raised from \(2^{18}\) to \(2^{20}\).
All other primary conditions remain fixed: distinct primes at least 5, exact
embedding degrees 3 through 12, Hasse validity, ordinarity, directed-cycle
orientation, rho convention, and explicit validation of every new full hit.

## Targeted 3-cycle enumeration

[PROVED] A full pairing-friendly directed 3-cycle consists of three target
edges whose exact degrees lie in 3 through 12. A two-of-three near-miss has two
target edges; in a directed triangle those two edges are consecutive after a
cyclic rotation. Therefore enumerating every target edge \(p_1\to p_2\), every
target continuation \(p_2\to p_3\), and testing the closing Hasse edge
\(p_3\to p_1\) finds every full hit and every two-of-three near-miss.

[PROVED] The targeted algorithm omits only directed triangles with at most one
target edge. Such triangles cannot be full hits or candidate-ledger rows under
the frozen rule. It still counts every directed Hasse edge while building the
target-edge graph.

[CONJECTURE] Before using the targeted algorithm at 20 bits, its complete
candidate rows must equal the original exhaustive algorithm at both 16 and 18
bits. Any row difference blocks the extension until explained.

## Predeclared prediction

[CONJECTURE] The 20-bit range will add only MNT-pattern 2-cycles and will add no
new full directed 3-cycle or two-of-three 3-cycle near-miss. A new exceptional
2-cycle or any new 3-cycle candidate row refutes this prediction.

