---
attempt: A019
status: completed
---
# A019 - Extended finite gap search on the 51 final quartic curves

## Idea

Use a CRT wheel of necessary local equation residues and exact integer-square
testing of the quartic discriminant to search every even gap
\(108\le c\le10^7\) on the 51 A018 survivors. Recover every integral \(p\)
and check divisibility, primality, Hasse, and exact embedding degrees.

## Predeclared outcome criteria

[CONJECTURE] No new exact quartic/quartic 2-cycle occurs through \(c=10^7\).
Any integral point, even with composite fields, must be recorded rather than
discarded silently.

## Execution log

[PROVED] The wheel retains every possible point because it uses only necessary
equation residues modulo 3, 5, 7, 11, and 13, together with even \(c\). For
each retained gap the quartic discriminant is tested by exact integer square
root, after which both quadratic roots are recovered and checked.

[EMPIRICAL: all 51 curves and every even gap 108 through 10,000,000] The
wheel retained 11,333,558 curve/gap cases. None had square discriminant, so
there was no integral point to pass on to the prime, Hasse, or exact-degree
checks.

## Outcome

[EMPIRICAL: complete stated finite range] The conjecture survives. No new
quartic/quartic cycle occurs through \(c=10^7\), and in fact none of the 51
remaining equations has an integral point in that interval.
