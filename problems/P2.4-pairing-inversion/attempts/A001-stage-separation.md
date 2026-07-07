---
attempt: A001
status: promising
---
# A001 — Separate and invert the two pairing stages

## Idea

Implement the reduced Tate pairing as an exposed Miller evaluation followed by a field exponentiation. Exhaustive enumeration at toy scale can then distinguish algebraic fibre size from the cost of locating a curve point in a fibre.

## Prior art

The problem prompt attributes this decomposition to Galbraith, Hess, and Vercauteren (2008), but that attribution must be checked before it is used as a `[CITED]` claim.

## Plan

1. Implement the two stages in shared code.
2. Validate their composition independently, then test bilinearity and non-degeneracy.
3. Enumerate final-exponentiation fibres in the full multiplicative extension field.
4. Enumerate the fixed-argument Miller map on the selected \(r\)-torsion domain.
5. Compare direct inversion timings and image/fibre structure.
6. Attempt the natural reduction and write the exact failure point.

## Prediction and falsifiers

The prediction is that final-exponentiation inversion is constructive once the cyclic field representation is enumerated, while Miller inversion remains a point-search or equation-solving problem. This prediction is falsified on the measured instance if raw Miller preimages can be recovered uniformly faster than final-exponentiation preimages under the same precomputation accounting.

## Execution log

The shared implementation in `lib/pairing.py` keeps Miller evaluation and final exponentiation separately callable. `lib/tests/test_pairing.py` matches the published \(p=43,r=11\) vector, checks its loop trace, and exhaustively checks the target order.

`code/measure_pairing_stages.py` exhaustively enumerated six final-exponentiation maps and the cyclic FAPI-1 Miller domains, then ran 50 inversion timings per curve. `code/analyze_miller_function.py` expanded the fixed-argument rational function and validated it at every nonidentity point of the published \(G_2\).

The literature check found Satoh's revised 2025 polynomial-time MI result in the opposite argument orientation. This prevents interpreting the naive brute-force timing as an asymptotic hardness result.

## Outcome

The staged implementation and toy-scale characterization succeeded. Naive Miller inversion dominates measured runtime, but final exponentiation creates the actual representative-selection obstruction: only one of \(d\) roots is compatible with the cyclic Miller domain. The attempt is promising rather than resolved because the FAPI-1 transfer of Satoh's opposite-orientation MI algorithm remains unchecked.
