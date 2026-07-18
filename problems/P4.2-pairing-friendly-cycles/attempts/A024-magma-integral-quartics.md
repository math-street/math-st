---
attempt: A024
status: completed
---
# A024 - Complete integral-point computations for pointed quartics

## Idea

After the A022 eliminations there are 29 normalized curves. Twenty-two have
square constant term and two more have the explicit rational points
\((-1,9)\) and \((1,9)\). Run Magma V2.29-8 `IntegralQuarticPoints` on these
24 curves, which computes all integral points modulo \(y\mapsto-y\).

## Predeclared outcome criteria

[CONJECTURE] None of the 24 pointed quartics has an integral point with
\(c\ge108\). Every returned point is recorded. A timeout or algorithm error is
not a negative result and leaves that curve unresolved.

## Execution log

[EMPIRICAL: Magma V2.29-8 complete integral-point computation] Twenty-two
curves returned successfully. Their complete integral-point lists contain
only \(c=0\), except QG004 which also contains \(c=\pm1\). Thus none has a
point at \(c\ge108\).

[REFUTED] QG012 and QG013 each have the supplied visible integral point
\((c,y)=(-1,9)\) or \((1,9)\), but `IntegralQuarticPoints` returned an empty
list even after sign changes and translation. Since this contradicts a known
point, those two outputs are rejected as certificates. Both quartics factor
over the rationals and are moved to a separate audit.

[EMPIRICAL: exact Magma V2.29-8 rank and torsion computation] Taking
\((-1,9)\) as origin on QG012 gives an elliptic curve with certified rank
bounds \([0,0]\) and torsion group \(\mathbb Z/2\). The two visible points
\((-1,\pm9)\) map to the point at infinity and the unique nonzero torsion
point. Hence they are all rational points on QG012. The substitution
\(c\mapsto-c\) gives all QG013 points \((1,\pm9)\).

## Outcome

[PROVED] All 24 pointed curves are globally closed. The direct integral-point
intrinsic closes 22, while the rank-zero argument closes the two reducible
exceptions without relying on their anomalous empty intrinsic output. The
conjecture is confirmed.
