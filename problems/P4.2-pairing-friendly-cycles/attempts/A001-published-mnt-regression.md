---
attempt: A001
status: promising
---
# A001 - Published MNT cycle regression

## Idea

Validate the complete local pipeline against the explicit parameter-\(x=3\)
MNT6/MNT4 pair in Chiesa--Chua--Weidner 2019 before searching for anything
new.

## Prior art

[CITED] The source gives explicit equations and states that the first two
curves in its four-curve example form an MNT (6,4) 2-cycle
(`refs/chiesa-chua-weidner2019.md`).

## Plan

1. Instantiate both published short-Weierstrass equations.
2. Count each group by direct enumeration of the defining equation.
3. Independently count each group with Hasse bounds, sampled point orders,
   BSGS, the quadratic twist, and CRT.
4. Verify the cycle equalities, traces, CM radicand, and every residue through
   the claimed embedding degree.
5. Persist a two-row CSV and a known-answer regression test.

## Predeclared outcome criteria

[CONJECTURE] A positive regression requires both point counts to equal 43 over
\(\mathbb F_{37}\) and 37 over \(\mathbb F_{43}\), with exact embedding
degrees 6 and 4. Any mismatch makes the regression negative and blocks a new
search until explained.

## Execution log

- [EMPIRICAL: published x=3 curves over F_37 and F_43] Direct equation
  enumeration and the independent Hasse/BSGS-twist routine both returned
  orders 43 and 37 (`code/reproduce_mnt_cycle.py`,
  `data/reproduce_mnt_cycle_x3_s4202_20260627.csv`).
- [EMPIRICAL: exponents 1..6 and 1..4] The residue sequences have their first
  value 1 exactly at exponents 6 and 4 (`code/tests/test_reproduce_mnt_cycle.py`).
- [PROVED] The measured traces are -5 and 7, which sum to 2, and both CM
  radicands equal 123 by direct integer substitution.

## Outcome

The regression is positive. Both published curves and every required cycle and
embedding-degree equality passed.

