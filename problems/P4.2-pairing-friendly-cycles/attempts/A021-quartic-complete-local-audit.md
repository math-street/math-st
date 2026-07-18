---
attempt: A021
status: completed
---
# A021 - Complete odd-prime local audit of the final curves

## Idea

For a good odd prime not dividing \(h\), the smooth projective quartic has at
least \(\ell+1-2\sqrt\ell\) points. At most two are at infinity, four have
\(p=0\), and four have \(p+c=0\). Hence every good prime \(\ell\ge19\) has an
allowable point. It remains only to test primes below 19, divisors of \(h\),
and divisors of the quartic discriminant, requiring a nonsingular solution so
that Hensel lifting applies.

## Predeclared outcome criteria

[CONJECTURE] Every one of the 51 rows has a nonsingular allowable solution at
all of its finitely many critical odd primes. A row with no solution is
globally eliminated; a singular-only solution remains unresolved until a
higher-power audit.

## Execution log

[PROVED] For a good odd prime \(\ell\nmid h\), the smooth projective genus-one
curve has at least \(\ell+1-2\sqrt\ell\) points. At most two points are at
infinity, four have \(p=0\), and four have \(p+c=0\). This proves existence
of an allowable point for every \(\ell\ge19\). The remaining critical set is
therefore finite and consists of primes below 19 and divisors of \(h\) or the
quartic discriminant.

[EMPIRICAL: complete enumeration at every critical odd prime] The largest
critical prime is 521. No row has an odd-prime obstruction. Thirty-four rows
have a nonsingular allowable residue at every critical prime. Seventeen have
only singular residues at one or more of 3, 7, and 13.

## Outcome

[EMPIRICAL: all 51 final rows] The conjecture is refuted in its nonsingularity
clause: 17 rows require higher-power lifting. The other 34 are certified
locally soluble at every odd prime. No row is eliminated.
