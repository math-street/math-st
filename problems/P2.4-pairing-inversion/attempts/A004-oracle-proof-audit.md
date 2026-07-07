---
attempt: A004
status: successful
---
# A004 — Close the A002 oracle proof

## Audit targets

- [PROVED] Model question: identify whether A002 uses Shoup random representations, Maurer hidden state, or an undocumented hybrid.
- [PROVED] Adaptive question: cover algorithms branching on opaque label bits and choosing later source exponents from those branches.
- [PROVED] Quantifier question: pass from an average over random encodings to one fixed infinite oracle against every probabilistic polynomial-time machine.
- [PROVED] Realization question: retain an actual elliptic curve and polynomial-bit-size public parameters behind the generic labels.

## Primary-source check

- [CITED] Shoup defines generic algorithms through random encodings and proves square-root DLP lower bounds by formal-expression collisions (EUROCRYPT 1997).
- [CITED] Maurer explicitly writes every generic DLP value as \(ax+b\) and obtains the \(\binom k2/q\) collision bound (Cryptography and Coding 2005, Section 1.2).
- [CITED] Zhandry names the two principal models RR/Shoup and TS/Maurer and proves security equivalence for single-stage games that exist in both (CRYPTO 2022, Theorems 1.5–1.6).
- [PROVED] A002 is now stated directly in RR/Shoup, with a matching typed single-stage formulation; it no longer conflates the models.

## Proof audit

- [PROVED] Fixing the collision-free simulator's coins and sampled strings fixes one adaptive transcript and at most \(t\) affine forms, despite arbitrary bit-level branching. Each good challenge is coupled to a fresh uniformly distributed encoding consistent with those strings; the proof does not incorrectly hold one encoding fixed while changing its challenge label.
- [PROVED] At most \(\binom t2\) challenges cause a pair collision, and at most one further collision-free challenge equals the output source exponent.
- [PROVED] The exact registered-handle success bound is therefore \((\binom t2+1)/r\); arbitrary unregistered strings supplied through any typed oracle interface add \(O(q/2^L)\).
- [PROVED] A solver correct with bounded error on every valid FAPI target would inherit the same success on the uniform challenge distribution, so the average bound refutes the ordinary worst-case search solver.
- [PROVED] For each machine, Markov plus Borel–Cantelli turns the expected bound into an eventually negligible bound for almost every fixed oracle.
- [PROVED] Countability of oracle machines permits one probability-one intersection, hence one fixed oracle defeating all of them.

## Computational counterexample search

- [EMPIRICAL: \(p\in\{5,7,11\},2\le t\le4\)] `verify_generic_oracle_bound.py` checked 541,966 affine sets exhaustively and 10,000 seeded four-form sets at \(p=11\). There were zero violations.
- [EMPIRICAL: exact tight fixtures] The maximum bad-set size attained \(\min(p,\binom t2)\) in every exhaustive row, so the verifier detects tight rather than vacuous behavior.

## Verdict

[PROVED] Q019 is closed. A002 is a valid oracle separation in the explicitly stated elliptic-curve-backed RR/Shoup generic bilinear model. The coordinate-exposing finite-field model is a different, stronger problem and is not part of this theorem.
