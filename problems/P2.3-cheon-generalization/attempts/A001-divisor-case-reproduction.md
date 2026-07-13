---
attempt: A001
status: promising
---
# A001 — Reproduce the divisor-case attack and its quarter-power scaling

## Idea

Use a generic multiplicative-subset search twice: first recover \(x^d\) from
the subgroup of \(d\)-th powers in \(\mathbb F_n^*\), then recover \(x\) from
the multiplicative coset of the \(d\)-th roots of unity.

## Prior art

[CITED] Cheon's Theorem 1 gives
\(O(\log n(\sqrt{(n-1)/d}+\sqrt d))\) primitive group operations for
\(d\mid n-1\), with the square-root sum counting repeated exponentiations
(Cheon, EUROCRYPT 2006, LNCS 4004, Theorem 1; `../refs/cheon2006.md`).

## Plan

1. Validate the repository environment and shared discrete-log tests.
2. Implement the multiplicative-subset BSGS with explicit operation counts.
3. Validate against exhaustive tiny cases before measuring.
4. Generate or select primes whose \(n-1\) has a divisor near \(\sqrt n\).
5. Run seeded trials at at least four sizes, fit the log-log operation-count
   slope, bootstrap a 95% confidence interval, and save row-level residuals.

## Execution log

- [EMPIRICAL: initial repository test suite] The 18 shared-library tests
  present at session start passed before implementation work.
- [EMPIRICAL: exhaustive n in {17,19,31}] `code/cheon.py` was validated
  exhaustively in three simulated groups and in
  the existing concrete order-19 elliptic-curve group.
- [EMPIRICAL: 328 trials, 70913 <= n <= 17592207015937]
  `code/run_scaling.py` completed 328 seeded trials over eight group orders;
  every recovery matched the ground truth.
- [EMPIRICAL: 328 trials, 70913 <= n <= 17592207015937] The fitted
  exponentiation-call slope was 0.25001 with 95% within-size
  bootstrap interval [0.24610, 0.25351].

## Outcome

The bounded reproduction succeeded, but it did not generalize the attack or
prove a lower bound. The overall P2.3 target is recorded as **failed** at the
user's direction; A001 remains a validated baseline rather than evidence for
the unresolved general case.
