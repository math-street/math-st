---
attempt: A003
status: promising
---
# A003 - Exact penalty of power and smooth norm shapes

## Idea

Separate structural existence from KLPT search overhead by exhaustively
computing the least represented normalized norm that is a power of 2, a power
of 3, or 5-smooth in each sampled ideal class.

## Prior art

[CITED] Basic KLPT seeks an $\ell$-power norm representative through a sequence
of norm equations and is heuristically estimated near $p^{7/2}$ in its 2014
form. [Kohel--Lauter--Petit--Tignol 2014, Theorem 7]

## Plan

1. Sample near-$p$ prime ideals to avoid a fixed small representative.
2. Enumerate every normalized norm through $p$, doubling the cutoff only when
   a requested shape is absent.
3. Validate each selected witness by constructing its equivalent ideal and
   independently checking norm and left closure.
4. Compare exact shape-constrained and unconstrained exponents.

## Execution log

1. Implemented an exact normalized-norm spectrum with inverse-Gram bounds.
2. Replaced a slow Python/Fraction point loop by overflow-checked NumPy int64
   blocks; only one witness per represented norm is reconstructed in Python.
3. Added adaptive cutoffs $p,2p,4p,\ldots,16p$.
4. Ran 70 ideals for balanced $p\in[7,223]$; every shape appeared by cutoff
   $p$, so no row was censored.

## Outcome

[EMPIRICAL: 70 near-$p$ ideals, $7\le p\le223$] Median penalties over the
unconstrained optimum were 1.0 for powers of 2, 1.5 for powers of 3, and 1.0
for 5-smooth norms. Maximum penalties were respectively 21.33, 20.25, and
1.43.

[EMPIRICAL: same range] Every class represented a power of 2, a power of 3,
and a 5-smooth norm at most $p$.

[PROVED] This is an exact structural optimum comparison at the measured sizes,
not an implementation or runtime measurement of KLPT.
