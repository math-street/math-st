---
attempt: A002
status: completed
---
# A002 — Exact small-parameter Weil and degree pipeline

## Idea

Represent $\mathbb F_{q^n}$ in a polynomial basis, keep factor-base equations as sparse polynomials over the extension, split coefficients into $\mathbb F_q$ coordinates, and measure first fall and solving degree with exact linear algebra.

## Prior art

[CITED] Petit and Quisquater (2012) and Kousidis and Wiemers (2019) obtain the factor-base system by expanding one Semaev equation in a basis of the extension field and then working in the finite-field function ring.

## Plan

1. Add and validate recursive evaluation through $f_6$.
2. Implement sparse summation-polynomial resultants and extension-field arithmetic.
3. Validate Weil restriction on decompositions constructed by elliptic-curve addition.
4. Compute exact first-fall and solving degrees with declared resource ceilings.
5. Search the resulting table for strict divergence.

## Execution log

Session 2 started after all 13 shared and 2 P1.3 tests passed.

- Added exact sparse extension-field arithmetic and recursive summation-polynomial resultants.
- Added a recursive $f_6$ evaluator and a six-point zero-sum regression test.
- Expanded generic $f_3,f_4,f_5$; stopped generic $f_6$ at a declared 30-second ceiling.
- Built coordinate Weil systems and checked constructed decompositions in every known-target case.
- Generalized first fall to the exact syzygy quotient and added exact regularity and closed-Macaulay solving-degree measurements.
- Ran the matrix through $q=23$, with per-case time and matrix-size ceilings recorded in every CSV row.

## Outcome

[EMPIRICAL: 34 canonical cases] The pipeline produced 32 complete rows and two stage-censored rows. It found a known-solution family pattern with $d_{\mathrm{ff}}=5$ and $\operatorname{sd}=q$ for $q\in\{7,11,13,17,19,23\}$, $n=m=2$.

[PROVED] The exact degree-5 first-fall witness and the absence of lower-degree syzygies for the quadratic $m=2$ shape are written in `NOTES.md`.

[EMPIRICAL: generic $f_6$] Full sparse expansion remains beyond the 30-second/250,000-term boundary; the evaluator itself is validated. This is a declared boundary, not a guessed statistic.
