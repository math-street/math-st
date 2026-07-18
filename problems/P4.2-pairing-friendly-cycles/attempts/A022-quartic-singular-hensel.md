---
attempt: A022
status: completed
---
# A022 - Higher-power Hensel audit at singular odd residues

## Idea

Recursively lift every allowable singular solution modulo the exceptional
primes 3, 7, and 13. A lift (x) is a certified p-adic branch as soon as

\[
v_\ell(f(x))>2\min\{v_\ell(f_c(x)),v_\ell(f_p(x))\},
\]

by the strong one-variable Hensel lemma applied in the coordinate with the
smaller derivative valuation.

## Predeclared outcome criteria

[CONJECTURE] Every singular-only critical pair is either obstructed at a
finite power or satisfies the strong Hensel criterion by exponent 8. Any
survivor without either certificate remains explicitly unresolved.

## Execution log

[EMPIRICAL: complete recursive lifting through the first certificate] All 21
singular row/prime pairs were lifted. Three have an exact integral residue
solution, ten satisfy the strong Hensel inequality at exponent 2, and eight
have no lift modulo \(\ell^2\).

## Outcome

[PROVED] The eight finite-power obstructions eliminate four rows: degree
pairs ((5,8),(8,10),(8,5),(10,8)), each at (h=10). Every one is
obstructed modulo both 9 and 169. The conjecture is confirmed, and the global
wall falls from 51 rows/31 normalized curves to 47 rows/29 curves.
