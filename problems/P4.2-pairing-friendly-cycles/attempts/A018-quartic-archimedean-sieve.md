---
attempt: A018
status: completed
---
# A018 - Archimedean Hasse sieve for local survivors

## Idea

For each of the 120 A017 survivors, translate \(p\) by the exact real Hasse
boundary \(L(c)=(c-1)^2/4\). Exact polynomial sign analysis on
\(c\ge108\) can rule out rows whose quadratic in \(p-L(c)\) is already on
the wrong side of zero and moves monotonically away from it.

## Predeclared outcome criteria

[CONJECTURE] The Hasse-bound sign test eliminates at least one A017 survivor.
A null result refutes the prediction and leaves all 120 rows for integral-point
methods.

## Execution log

[PROVED] Translating by \(L=(c-1)^2/4\) writes the defining equation as a
quadratic in \(x=p-L\ge0\). Exact Sturm root counts certify the signs of its
discriminant, value at \(x=0\), and derivative there on the full ray
\(c\ge108\).

[EMPIRICAL: all 120 A017 survivors] 55 rows have negative discriminant on the
entire ray. Another 14 have positive value and positive derivative at the
Hasse boundary with positive leading coefficient, so the quadratic cannot
vanish for \(x\ge0\).

## Outcome

[EMPIRICAL: exact polynomial sign certificates] 69 rows are rigorously
excluded and 51 survive. The conjecture is confirmed. Every survivor has
\(h>0\), positive discriminant, and a real root above the Hasse boundary.
