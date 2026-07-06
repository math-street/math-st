---
attempt: A001
status: promising
---
# A001 - Complete smoothness dependency map for exTNFS

## Idea

Separate the exTNFS complexity argument into deterministic algebraic steps, smoothness-density inputs, and adjacent probabilistic inputs.  Give every smoothness input an explicit analytic statement instead of a generic random-norm slogan.

## Prior art

[CITED] Kim--Barbulescu 2016 explicitly invoke classical NFS smoothness heuristics for relation collection and Dickman probabilities for special-$q$ descent.

[CITED] Canfield--Erdos--Pomerance 1983 rigorously supply the random-integer benchmark, while Barbulescu--Lachand 2017 and Balog--Blomer--Dartyge--Tenenbaum 2012 give partial fixed-form or fixed-field results.

[CITED] Lee--Venkatesan 2018 rigorize ordinary randomized NFS relation generation by reducing polynomial evaluations to smooth integers in arithmetic progressions; the mechanism does not include an outer tower norm.

## Plan

1. Fix tower, number-field, special-$q$, sieving-region, and smoothness notation.
2. Trace relation collection, linear algebra, initialization, and descent.
3. Number each smoothness assertion at its first use.
4. Classify the strongest unconditional theorem found for each assertion.

## Execution log

[PROVED] The audit reconstructed the iterated-resultant forms and all relation, target-splitting, and descent sampling spaces in `SMOOTHNESS_ASSUMPTIONS.md`.

[PROVED] Ten inputs S-01--S-10 were isolated.  S-09 (accepted-candidate factorization cost) and S-10 (random-integer density) are known; S-01--S-08 are not supplied by the cited theorems with the exTNFS quantifiers.

[PROVED] Relation collection can be reduced to one minimal joint lower bound (RC), which is strictly stronger than the two marginal density statements.  Special-$q$ descent requires an adaptive, lattice-conditioned analogue (SQ).

## Outcome

[PROVED] SG-01--SG-03 are complete as a dependency and literature audit, not as an unconditional exTNFS proof.  The main artifact is `SMOOTHNESS_ASSUMPTIONS.md`.

[PROVED] Polynomial-selection success and structured relation-matrix rank were identified as adjacent non-smoothness gaps, so closing only the analytic smooth-value inputs would still not prove the complete DLP complexity.
