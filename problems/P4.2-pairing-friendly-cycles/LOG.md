# Log - P4.2

Archived detail: `LOG-archive/LOG-001-003.md`.

- Session 1: derived cycle identities, reconstructed the published MNT cycle,
  and completed the frozen 16-bit searches.
- Session 2: extended candidate-complete searches through 22 bits, constructed
  every hit, and proved the MNT 2-cycle and consecutive-chain theorems.
- Session 3 through A016: proved cyclotomic-root completeness, extended the
  census through 28 bits, classified quadratic and mixed degree pairs, and
  reduced quartic/quartic pairs to 750 genus-one rows.

## Session 3 continuation - 2026-07-18

**Goal:** Finish the quartic/quartic classification rather than stopping at
the genus-one reduction.

**Prediction (written before the relevant runs):** [CONJECTURE] Local and
archimedean sieves eliminate some of the 750 rows; no new exact cycle appears
through (c=10^7); the remaining curves can be closed by exact genus-one
arithmetic.

**Did:**
- Proved the sharper large-gap bound \(|h|\le24\), exhaustively audited all
  gaps (2\le c\le106), and closed all 34 degenerate discriminants.
- Applied local congruence, exact real-sign, singular Hensel, and two-adic
  audits to all 750 genus-one rows.
- Searched every even gap (108\le c\le10^7) on the 51 post-sign curves.
- Canonicalized 47 final rows to 29 square-content/twist-correct curves.
- Used exact Magma V2.29-8 integral-point, fake two-Selmer, rank, and torsion
  computations to close every final curve.

**Found:**
- [EMPIRICAL: all 750 rows] Local congruences eliminate 630 and exact
  archimedean signs eliminate 69 more.
- [PROVED] Singular lifting eliminates four additional rows modulo 9 and 169;
  every remaining row has local points at all places.
- [EMPIRICAL: 51 curves, every even (108\le c\le10^7)] The CRT-wheel search
  tested 11,333,558 candidates and found no integral point.
- [EMPIRICAL: exact Magma V2.29-8 computations] Twenty-two pointed quartics
  have only gaps (-1,0,1); five locally soluble torsors have empty fake
  two-Selmer sets; the last symmetric curve has rank zero and torsion
  \(\mathbb Z/2\), hence only gaps \(\pm1\).
- [PROVED] The only quartic/quartic exact-degree 2-cycle is
  ((p,q;k_1,k_2)=(11,13;12,10)).

**Prediction vs. outcome:** matched and substantially strengthened. The local
sieves reduced the wall from 750 rows to 29 curves; global descent and
integral-point arithmetic closed all 29.

**Did not work:** Magma `IntegralQuarticPoints` anomalously returned an empty
list for QG012/QG013 despite their visible points. Those outputs were rejected.
The independent rank-zero/torsion computation closed the pair instead.

**Changed my mind about:** the quartic reduction was not the terminal wall.
After exact local pruning, the final global computations were small enough to
finish. The true remaining P4.2 frontier is degree 7, 9, or 11 and global
length-at-least-3 classification, not the degree-four cyclotomic cases.

**Next:** derive a bounded quotient/resultant reduction for one ordered pair
involving exact degree 7 or 9, starting with (7,7), and separately classify
the five tiny directed 3-cycle hits.

**Final validation:** [EMPIRICAL: Python 3.13.4 and SymPy 1.14.0,
2026-07-18] All 70 shared tests and all 58 P4.2 tests pass. Every P4.2 Python
file compiles; the quartic cross-file assertions reproduce counts
750 -> 120 -> 51 -> 47 rows -> 29 curves and find no finite-search point.
