# Handoff - P4.2 - after session 3 continuation

## State in five lines

[EMPIRICAL: distinct primes below \(2^{28}\)] The exact-degree-3-through-12 primary census is candidate-complete.
[EMPIRICAL: same space] It has 333 2-cycle hits and five directed 3-cycle hits.
[PROVED] Every 2-cycle with both degrees in {3,4,5,6,8,10,12} is globally classified.
[PROVED] The quartic/quartic genus-one remainder is fully closed; no arithmetic wall remains there.
[PROVED] The remaining global frontier is degree 7, 9, or 11 and general length-at-least-3 cycles.

## What is established

- [PROVED] For an \(m\)-cycle, \(t_i=p_i+1-p_{i+1}\),
  \(\sum_i t_i=m\), and exact degree is
  \(\operatorname{ord}_{p_{i+1}}(p_i)\).
- [PROVED] A 2-cycle has equal Frobenius discriminants.
- [EMPIRICAL: primes below \(2^{28}\), degrees 3 through 12] The 333 hits are
  164 degree-(6,4), 164 degree-(4,6), and five tiny exceptions.
- [EMPIRICAL: three distinct primes below \(2^{28}\)] There are five directed
  hits and 61 two-of-three near-misses; no hit has a field above 43.
- [EMPIRICAL: all full hits through 24 bits] Every hit has explicit equations
  verified by BSGS plus enumeration or a prime-point Hasse certificate.

## Global 2-cycle results

- [PROVED] Degree pairs (6,4) and (4,6) are exactly the two MNT polynomial
  orientations (`MNT_CLASSIFICATION.md`).
- [PROVED] If both degrees lie in {3,4,6}, no other pair occurs
  (`QUADRATIC_DEGREE_CLASSIFICATION.md`).
- [PROVED] If exactly one degree lies in {3,4,6} and the other in
  {5,8,10,12}, the unique cycle is \((7,11;10,3)\)
  (`MIXED_DEGREE_CLASSIFICATION.md`).
- [PROVED] If both degrees lie in {5,8,10,12}, the unique cycle is
  \((11,13;12,10)\) (`QUARTIC_DEGREE_REDUCTION.md`).
- [PROVED] Therefore all pairs in {3,4,5,6,8,10,12} squared are classified.

## Quartic closure details

- [PROVED] Small gaps \(2\le c\le106\) and all 34 degenerate discriminants
  are exhaustively audited; only \((11,13;12,10)\) occurs.
- [PROVED] For \(c\ge108\), \(|h|\le24\), leaving 750 genus-one rows.
- [PROVED] Congruence, real-sign, and higher-power Hensel obstructions reduce
  these to 47 rows on 29 normalized curves.
- [EMPIRICAL: every even \(108\le c\le10^7\) on 51 pre-Hensel curves] An
  11,333,558-candidate exact square search found no integral point.
- [EMPIRICAL: exact Magma V2.29-8 computations] Twenty-two curves have only
  small integral points, five have empty fake two-Selmer sets, and the last
  symmetric curve has rank zero and torsion \(\mathbb Z/2\).

## Length-three structure

- [PROVED] No consecutive MNT prime triple closes in either orientation with
  all exact degrees in 3 through 12 (`MNT_THREE_CHAIN_OBSTRUCTION.md`).
- [PROVED] Every equal-signed-gap degree-(4,6) path is consecutive MNT
  (`MNT_PATH_CLASSIFICATION.md`).
- [EMPIRICAL: all 61 near-misses below \(2^{28}\)] Twenty-six are excluded
  MNT chains and 35 are residual; only two residuals lie above \(2^{16}\).

## Precisely scoped negatives

- [EMPIRICAL: \(5\le p<q<2^{28}\), degrees 3 through 12] No
  non-{(6,4),(4,6)} 2-cycle has \(q\ge32\).
- [EMPIRICAL: three distinct fields below \(2^{28}\), same degrees] No
  directed 3-cycle hit contains a field greater than 43.
- [PROVED] These finite statements do not cover fields at least \(2^{28}\),
  degrees above 12, or global pairs involving exact degree 7, 9, or 11.

## Validation

[EMPIRICAL: Python 3.13.4 and SymPy 1.14.0] All 70 shared and 58 P4.2 tests
pass; all P4.2 Python files compile. Magma outputs have local parser and
substitution regressions.

## Next action

Derive the quotient/resultant reduction for ordered degree pair (7,7). In
parallel mathematically (not with agents), classify the five tiny directed
3-cycle hits by exact degree pattern and determine whether each is isolated.

## Invariants - do not violate

- Keep `SEARCH_SPACE.md` and `THREE_CYCLE_CONDITIONS.md` frozen.
- Preserve all one-sided and two-of-three near-misses.
- Distinguish global proofs from the 28-bit empirical census.
- Do not rely on the anomalous empty QG012/QG013 `IntegralQuarticPoints`
  output; the independent rank-zero proof closes them.
- Cycle rho is \(\max_i\log(p_i)/\log(p_{i+1})\); its geometric mean is 1.

## Files that matter

`RESULTS.md` is the scoped write-up.
`QUARTIC_DEGREE_REDUCTION.md` is the newest global theorem.
`data/magma_*_20260718.txt` stores the final exact global outputs.
`code/search_*_targeted.py` implements candidate-complete root enumeration.
`data/classify_three_cycle_near_misses_n61_20260718.csv` is the residual ledger.

## What I would tell my replacement

The quartic wall is gone: do not reopen its 750 curves. The next genuinely
new algebra starts with cyclotomic degrees six and ten (exact degrees 7, 9,
11), while the length-three global question is still open beyond MNT chains.
