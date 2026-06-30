---
attempt: A001
status: promising
---
# A001 — Exhaustive toy CSIDH action

## Idea

[PROVED] For (p\equiv3\pmod4), the curve (E_0:y^2=x^3+x) has (p+1) rational points when (p>3): pairing each (x) with the quadratic-character sum gives trace zero, and the implementation also checks the count exhaustively.

[HEURISTIC] Small split-prime isogeny steps should generate the class-group action orbit in a suitably chosen toy instance. This is falsified if the generated orbit is smaller than the independently enumerated class number or if a generator step is not a permutation.

## Prior art

[CITED] CSIDH uses the class group of an imaginary-quadratic order acting through horizontal isogenies on supersingular curves over a prime field (Castryck et al., 2018, ASIACRYPT, DOI 10.1007/978-3-030-03332-3_15).

## Plan

1. Implement odd-degree Vélu quotients for short-Weierstrass curves.
2. Canonicalize curves up to `F_p`-isomorphism, retaining twist information rather than identifying by (j)-invariant alone.
3. Enumerate primitive reduced forms of discriminant (-4p).
4. Compare the orbit and class-number cardinalities and construct the generator permutations.

## Positive and negative outcomes

- [PROVED] A positive SG-01 outcome requires matching cardinalities, bijective generator maps, a transitive generated permutation group, and trivial stabilizer.
- [PROVED] Any mismatch is a negative result for the chosen implementation or instance, not evidence against the CSIDH theorem.

## Execution log

- [EMPIRICAL: repository baseline on 2026-06-30] The pre-existing shared test suite passed 34 tests.
- [EMPIRICAL: test fixture at p=419] The first twist-separation test used the (j=1728) starting curve and failed because its nominal quadratic twist was already prime-field isomorphic; the corrected test uses a generic Vélu quotient.

## Outcome

[EMPIRICAL: (p=59), degrees (3,5)] The reduced-form class number, isogeny orbit size, and generated permutation-group order all equal 9; the action is abelian and regular.

[EMPIRICAL: (p=419), degrees (3,5,7)] The reduced-form class number, isogeny orbit size, and generated permutation-group order all equal 27; the action is abelian and regular.

[PROVED] In each computed transition table, regularity follows from transitivity and the singleton base-state stabilizer, both checked by exhaustive permutation-group enumeration.

[EMPIRICAL: A001 prediction test at (p=419)] The prediction that the available primes might generate only a proper subgroup was refuted: the orbit cardinality equals (h(-1676)=27).
