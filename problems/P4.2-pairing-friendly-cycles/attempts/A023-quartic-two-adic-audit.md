---
attempt: A023
status: completed
---
# A023 - Complete two-adic audit of the final quartic rows

## Idea

Recursively lift solutions with even \(c\) and odd \(p\) modulo powers of two.
As in A022, an exact solution or the strong valuation inequality certifies a
2-adic branch; an empty lift level is a global obstruction.

## Predeclared outcome criteria

[CONJECTURE] Every one of the 47 odd-locally surviving rows is either
obstructed or strongly Hensel-certified by exponent 12. Any remaining branch
is reported as unresolved.

## Execution log

[EMPIRICAL: recursive lifting through the first certificate] All 47 rows that
survived the odd-prime audit were lifted through powers of two. Eleven have an
exact integral 2-adic seed and 36 satisfy the strong Hensel inequality. No row
is obstructed or unresolved.

## Outcome

[PROVED] The conjecture is confirmed. All final 47 rows (29 normalized curves)
are locally soluble over the reals and every p-adic field. Purely local
methods are exhausted; any further elimination must use global rational or
integral-point arithmetic.
