# P4.2 - Pairing-friendly curve cycles

## Formal statement

A 2-cycle is a pair of curves with
\(\#E_1(\mathbb F_p)=q\) and \(\#E_2(\mathbb F_q)=p\). An \(m\)-cycle is
the analogous closed chain of length \(m\).

The research questions are:

1. Do pairing-friendly 2-cycles exist outside the MNT families with embedding
   degrees 4 and 6?
2. Do pairing-friendly cycles of length at least 3 exist?
3. Can a cycle satisfy a clearly specified cycle-level \(\rho<2\) criterion?

## Target outcome

The preferred outcome is a fully verified new cycle or a non-existence proof
for a stated class. The session-scale target is an exhaustive negative search
over a precisely documented toy space, including near-misses and the condition
that rejects each one.

Any candidate must pass independent point counting on both curves. Its exact
embedding degree must be checked by proving divisibility at the claimed degree
and non-divisibility at every smaller positive degree.

## Scope

All experiments obey the repository-wide toy ceiling \(\log_2 p\leq 60\).
Negative results are claimed only for the explicitly enumerated search space.

