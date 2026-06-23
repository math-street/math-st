# P2.1 - Completing the Maurer reduction (CDH => DLP)

This file records the user-supplied research target. Epistemic status belongs
to the session notes, not to the wording of the target.

## Formal target

Let the input group be cyclic of prime order $r$.

Find an algorithm that, on input $r$, constructs in time
$\operatorname{poly}(\log r)$ an auxiliary elliptic curve $E'/\mathbb F_r$
(or a related structure) whose group order is
$(\log r)^{O(1)}$-smooth.

Alternatively, exhibit an infinite family of primes $r$ for which no such
curve exists, or for which finding one is hard.

## Session deliverables

1. Restate Maurer's reduction with its precise smoothness requirement.
2. Implement and validate naive sampling, point counting, and smoothness tests.
3. Measure search work at toy sizes and compare it with a stated heuristic.
4. State exactly what remains open for an unconditional construction.

The default experimental ceiling is $\log_2 r\le 60$, as required by the
shared scaffold.
