---
attempt: A017
status: completed
---
# A017 - Local-obstruction sieve for the remaining genus-one equations

## Idea

For each of the 750 large-gap genus-one rows from A016, test the defining
quadratic equation in \((c,p)\) modulo powers of two and small odd primes.
For odd moduli, also impose the necessary prime-field residues
\(p\not\equiv0\) and \(p+c\not\equiv0\). These are valid because the Hasse
lower bound gives \(p\ge(c-1)^2/4>2800\) for \(c\ge108\).

## Predeclared outcome criteria

[CONJECTURE] At least one of the 750 rows has no locally allowable residue for
some modulus at most 251 and can therefore be eliminated globally. A null
result refutes this prediction but still records a reproducible arithmetic
wall.

## Execution log

[PROVED] For \(c\ge108\), Hasse gives \(p>(107)^2/4>2800\). Therefore, for
every odd prime \(\ell\le251\), prime fields necessarily satisfy
\(p\not\equiv0\pmod\ell\) and \(p+c\not\equiv0\pmod\ell\).

[EMPIRICAL: complete residue enumeration] All 750 genus-one rows were tested
modulo 8, 16, and 32 and every odd prime through 251. The optimized
discriminant check was independently regression-tested against direct
enumeration for representative rows and moduli.

## Outcome

[EMPIRICAL: all 750 A016 genus-one rows] 630 rows have a rigorous local
obstruction and 120 survive every tested modulus. The conjecture is confirmed.
The first obstructions occur modulo 3, 5, 7, 8, 11, 13, 16, 17, 19, 23, 37,
53, or 67.
