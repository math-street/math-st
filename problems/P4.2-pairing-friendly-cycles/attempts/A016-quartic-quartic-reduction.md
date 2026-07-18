---
attempt: A016
status: completed
---
# A016 - Reduce all quartic/quartic degree pairs to genus-zero/one curves

## Idea

For both degrees in {5,8,10,12}, write the cyclotomic quotients as \(m,n\).
Their congruence modulo the even field gap gives \(n=m+hc\). Hasse bounds
\(|h|\), and eliminating \(m,n\) leaves a quartic discriminant equation
\(y^2=D_{k_1,k_2,h}(c)\).

## Predeclared outcome criteria

[CONJECTURE] For every ordered degree pair and \(|h|\le552\), no
perfect-square discriminant polynomial produces an unaccounted polynomial
cycle family. Any such square case refutes the prediction and must be analyzed
before using the reduction.

## Execution log

[EMPIRICAL: exact SymPy reduction] The initial audit covered all 17,680
ordered `(degree pair,h)` cases for \(|h|\le552\). It found no perfect-square
discriminant polynomial, 17,646 genus-one rows, and 34 degenerate rows.

[PROVED] The monotone Hasse estimate recorded in
`QUARTIC_DEGREE_REDUCTION.md` improves the necessary bound to \(|h|\le24\)
when \(c\ge108\). The reduced large-gap certificate therefore has 784 rows:
750 genus-one and the same 34 degenerate cases.

[EMPIRICAL: complete finite audits under proved bounds] All 848 ordered
pair/small-even-gap cases through \(c=106\) were enumerated. All 34
degenerate symbolic rows were closed. The only exact cycle found is
\((p,q;k_1,k_2)=(11,13;12,10)\).

## Outcome

[PROVED] The predicted square-polynomial family does not occur. Every other
quartic/quartic cycle reduces to an integral point with even \(c\ge108\) on
one of 750 explicit genus-one equations. This completes the stated reduction
goal but does not solve those 750 integral-point problems.
